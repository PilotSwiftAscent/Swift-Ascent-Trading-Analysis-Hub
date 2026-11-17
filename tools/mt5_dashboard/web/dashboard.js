const fields = Object.fromEntries(Array.from(document.querySelectorAll('[id]'), (node) => [node.id, node]));
const dash = '—';
const refreshInterval = 2000;
const localClock = new Intl.DateTimeFormat(undefined, {hour: '2-digit', minute: '2-digit', second: '2-digit'});
const shortDate = new Intl.DateTimeFormat(undefined, {month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'});
const labels = {
  positions: ['Symbol', 'Side', 'Lots', 'Entry', 'Current', 'Stop loss', 'Take profit', 'Floating P/L'],
  orders: ['Symbol', 'Order type', 'Lots', 'Order price', 'Stop loss', 'Take profit'],
};

let snapshot = null;
let selectedTab = 'positions';
let renderHeaderFor;
let busy = false;
let nextPoll;

function number(value, digits = 2, options = {}) {
  if (!Number.isFinite(value)) return dash;
  const places = Number.isInteger(digits) && digits >= 0 && digits <= 12 ? digits : 2;
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: places, maximumFractionDigits: places, ...options,
  }).format(value);
}

function money(value, currency, signed = false) {
  if (!Number.isFinite(value)) return dash;
  const signDisplay = signed ? 'exceptZero' : 'auto';
  if (currency && /^[A-Z]{3}$/.test(currency)) {
    return new Intl.NumberFormat('en-US', {style: 'currency', currency, signDisplay}).format(value);
  }
  return [number(value, 2, {signDisplay}), currency].filter(Boolean).join(' ');
}

function signedClass(value) {
  return value > 0 ? 'positive' : value < 0 ? 'negative' : '';
}

function textCell(row, value, className = '') {
  const cell = row.insertCell();
  cell.textContent = value;
  if (className) cell.className = className;
  return cell;
}

function updateAccount() {
  const account = snapshot?.account;
  const currency = account?.currency;
  fields.equity.textContent = money(account?.equity, currency);
  fields.balance.textContent = money(account?.balance, currency);
  fields.floating.textContent = money(account?.floating_pnl, currency, true);
  fields.floating.className = signedClass(account?.floating_pnl);
  fields.margin.textContent = money(account?.free_margin, currency);
  fields.currency.textContent = currency ?? '';
  fields.currency.hidden = !currency;
  fields['margin-level'].hidden = !Number.isFinite(account?.margin_level);
  fields['margin-level'].textContent = `Margin level ${number(account?.margin_level, 1)}%`;
}

function updateQuotes() {
  const quotes = snapshot?.quotes ?? [];
  const rows = document.createDocumentFragment();
  for (const quote of quotes) {
    const row = document.createElement('tr');
    const label = textCell(row, '');
    const symbol = document.createElement('span');
    const time = document.createElement('time');
    symbol.className = 'quote-symbol';
    symbol.textContent = quote.symbol;
    time.className = 'quote-time';
    time.textContent = 'No tick';
    if (Number.isFinite(quote.timestamp) && quote.timestamp > 0) {
      const instant = new Date(quote.timestamp);
      time.dateTime = instant.toISOString();
      time.title = `Last tick ${instant.toLocaleString()}`;
      time.textContent = instant.toDateString() === new Date().toDateString() ? localClock.format(instant) : shortDate.format(instant);
    }
    label.append(symbol, time);
    textCell(row, number(quote.bid, quote.digits));
    textCell(row, number(quote.ask, quote.digits));
    rows.append(row);
  }
  fields['quote-body'].replaceChildren(rows);
  fields['quote-empty'].hidden = quotes.length > 0;
  fields['quote-count'].textContent = quotes.length ? `${quotes.length} ${quotes.length === 1 ? 'symbol' : 'symbols'}` : '';
}

function updateSymbolFilter(symbols) {
  const filter = fields['symbol-filter'];
  const previous = filter.value;
  const values = ['', ...symbols];
  const current = Array.from(filter.options, (option) => option.value);
  if (current.length === values.length && current.every((value, index) => value === values[index])) return;
  filter.replaceChildren(...values.map((value) => new Option(value || 'All symbols', value)));
  filter.value = symbols.includes(previous) ? previous : '';
}

function updateTrades() {
  const positions = snapshot?.positions ?? [];
  const orders = snapshot?.orders ?? [];
  const records = selectedTab === 'positions' ? positions : orders;
  const currency = snapshot?.account?.currency;
  fields['positions-count'].textContent = positions.length;
  fields['orders-count'].textContent = orders.length;
  const symbols = [...new Set([...positions, ...orders].map((record) => record.symbol))].sort();
  updateSymbolFilter(symbols);
  const filter = fields['symbol-filter'].value;
  const visible = filter ? records.filter((record) => record.symbol === filter) : records;

  if (renderHeaderFor !== selectedTab) {
    renderHeaderFor = selectedTab;
    fields['trade-table'].setAttribute('aria-label', selectedTab === 'positions' ? 'Open positions' : 'Pending orders');
    fields['trade-head'].replaceChildren();
    const header = fields['trade-head'].insertRow();
    for (const title of labels[selectedTab]) {
      const cell = document.createElement('th');
      cell.scope = 'col';
      cell.textContent = title;
      header.append(cell);
    }
  }

  const rows = document.createDocumentFragment();
  for (const trade of visible) {
    const row = document.createElement('tr');
    textCell(row, trade.symbol, 'position-symbol');
    const tone = trade.side.startsWith('Buy') ? 'side-buy' : trade.side.startsWith('Sell') ? 'side-sell' : '';
    textCell(row, trade.side, `side ${tone}`.trim());
    textCell(row, number(trade.volume, 4, {minimumFractionDigits: 2}));
    if (selectedTab === 'positions') textCell(row, number(trade.entry, trade.digits));
    textCell(row, number(trade.price, trade.digits));
    textCell(row, number(trade.stop_loss, trade.digits));
    textCell(row, number(trade.take_profit, trade.digits));
    if (selectedTab === 'positions') textCell(row, money(trade.pnl, currency, true), signedClass(trade.pnl));
    rows.append(row);
  }
  fields['trade-body'].replaceChildren(rows);
  const subject = selectedTab === 'positions' ? 'open positions' : 'pending orders';
  fields['trade-empty'].hidden = visible.length > 0;
  fields['trade-empty'].textContent = snapshot?.status === 'connected'
    ? `No ${subject}${filter ? ` for ${filter}` : ''}.`
    : 'Waiting for account data.';
}

function selectTab(tab, focus = false) {
  selectedTab = tab;
  for (const key of Object.keys(labels)) {
    const control = fields[`${key}-tab`];
    control.setAttribute('aria-selected', String(key === tab));
    control.tabIndex = key === tab ? 0 : -1;
  }
  fields['trades-panel'].setAttribute('aria-labelledby', `${tab}-tab`);
  if (focus) fields[`${tab}-tab`].focus();
  updateTrades();
}

function drawChart() {
  const canvas = fields['equity-chart'];
  const points = (snapshot?.equity_history ?? []).filter(([time, equity]) => Number.isFinite(time) && Number.isFinite(equity));
  const {width, height} = canvas.getBoundingClientRect();
  if (width < 140 || !height) return;
  const scale = window.devicePixelRatio || 1;
  canvas.width = Math.round(width * scale);
  canvas.height = Math.round(height * scale);
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  ctx.scale(scale, scale);

  const first = points.at(0);
  const last = points.at(-1);
  const canPlot = Boolean(first && last && last[0] > first[0]);
  fields['chart-empty'].hidden = canPlot;
  fields['chart-empty'].textContent = points.length ? 'Collecting equity samples' : 'Waiting for equity samples';
  fields['chart-context'].textContent = canPlot ? `${points.length} samples in view` : 'Sampled as the monitor updates';
  if (!canPlot) {
    canvas.setAttribute('aria-label', 'Session equity chart, waiting for data');
    return;
  }

  const currency = snapshot.account?.currency;
  const minimum = Math.min(...points.map((point) => point[1]));
  const maximum = Math.max(...points.map((point) => point[1]));
  const pad = Math.max((maximum - minimum) * .14, Math.abs(maximum) * .000025, .01);
  const low = minimum - pad;
  const high = maximum + pad;
  const left = width < 370 ? 62 : 85;
  const right = width - 11;
  const top = 12;
  const bottom = height - 29;
  const x = (time) => left + (time - first[0]) / (last[0] - first[0]) * (right - left);
  const y = (equity) => bottom - (equity - low) / (high - low) * (bottom - top);
  canvas.setAttribute('aria-label', `Session equity chart, low ${money(minimum, currency)}, high ${money(maximum, currency)}, latest ${money(last[1], currency)}`);

  ctx.font = '11px Consolas, monospace';
  ctx.strokeStyle = '#373b36';
  ctx.fillStyle = '#a6aba4';
  ctx.textAlign = 'right';
  ctx.textBaseline = 'middle';
  for (let index = 0; index < 4; index++) {
    const lineY = top + index / 3 * (bottom - top);
    ctx.beginPath();
    ctx.moveTo(left, lineY);
    ctx.lineTo(right, lineY);
    ctx.stroke();
    ctx.fillText(number(high - index / 3 * (high - low), high - low >= 10 ? 0 : 2), left - 8, lineY, left - 10);
  }
  const line = new Path2D();
  line.moveTo(x(first[0]), y(first[1]));
  for (const [time, equity] of points.slice(1)) line.lineTo(x(time), y(equity));
  const area = new Path2D(line);
  area.lineTo(right, bottom);
  area.lineTo(left, bottom);
  area.closePath();
  const gradient = ctx.createLinearGradient(0, top, 0, bottom);
  gradient.addColorStop(0, 'rgba(55, 144, 109, .36)');
  gradient.addColorStop(1, 'rgba(30, 107, 82, .08)');
  ctx.fillStyle = gradient;
  ctx.fill(area);
  ctx.strokeStyle = '#8ad6b2';
  ctx.lineWidth = 2;
  ctx.stroke(line);
  ctx.fillStyle = '#edbd64';
  ctx.beginPath();
  ctx.arc(right, y(last[1]), 3.2, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#a6aba4';
  ctx.textAlign = 'left';
  ctx.fillText(localClock.format(first[0]), left, height - 11);
  ctx.textAlign = 'right';
  ctx.fillText(localClock.format(last[0]), right, height - 11);
}

function render() {
  const connected = snapshot.status === 'connected';
  const demo = snapshot.mode === 'demo';
  fields.feed.dataset.state = connected ? demo ? 'demo' : 'connected' : 'unavailable';
  fields['feed-label'].textContent = connected ? demo ? 'Demo feed' : 'MT5 connected' : 'Feed unavailable';
  fields.updated.textContent = connected && Number.isFinite(snapshot.timestamp)
    ? `Updated ${localClock.format(snapshot.timestamp)}` : 'Waiting for account data';
  fields.notice.hidden = !snapshot.message;
  fields.notice.textContent = snapshot.message || '';
  updateAccount();
  updateQuotes();
  updateTrades();
  drawChart();
}

async function refresh() {
  if (busy) return;
  clearTimeout(nextPoll);
  busy = true;
  fields.refresh.disabled = true;
  try {
    const response = await fetch('/api/snapshot', {cache: 'no-store', signal: AbortSignal.timeout(7000)});
    if (!response.ok) throw new Error('Snapshot request failed');
    snapshot = await response.json();
    render();
  } catch {
    snapshot = {status: 'unavailable', message: 'The local dashboard did not respond. Check that the dashboard server is running.'};
    render();
  } finally {
    fields.refresh.disabled = false;
    busy = false;
    nextPoll = setTimeout(refresh, refreshInterval);
  }
}

for (const key of Object.keys(labels)) {
  fields[`${key}-tab`].addEventListener('click', () => selectTab(key));
  fields[`${key}-tab`].addEventListener('keydown', (event) => {
    if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) {
      event.preventDefault();
      const tab = event.key === 'Home' ? 'positions' : event.key === 'End' ? 'orders' : key === 'positions' ? 'orders' : 'positions';
      selectTab(tab, true);
    }
  });
}
fields['symbol-filter'].addEventListener('change', updateTrades);
fields.refresh.addEventListener('click', refresh);
new ResizeObserver(drawChart).observe(fields['equity-chart']);
refresh();
