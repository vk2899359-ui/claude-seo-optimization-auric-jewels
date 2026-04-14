const PASSWORD = 'auric2026';

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).send('Method not allowed');
  }

  const pass = req.query.pass;
  if (pass !== PASSWORD) {
    res.setHeader('Content-Type', 'text/html');
    return res.status(401).send(`<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Unauthorized</title><style>body{background:#111;color:#C5A54E;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;font-family:system-ui,-apple-system,sans-serif;}.box{text-align:center;}.box h1{font-size:2rem;margin-bottom:0.5rem;}.box p{color:#888;}</style></head><body><div class="box"><h1>AURIC JEWELS</h1><p>Unauthorized. Please provide the correct password.</p></div></body></html>`);
  }

  res.setHeader('Content-Type', 'text/html');
  res.status(200).send(getDashboardHTML(pass));
};

function getDashboardHTML(pass) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Auric Jewels — WhatsApp Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{--gold:#C5A54E;--gold-dim:#a8893a;--bg:#0d0d0d;--surface:#1a1a1a;--surface2:#242424;--border:#333;--text:#e0e0e0;--text-dim:#888;--customer-bg:#2a2a2a;--bot-bg:#3d3520;}
body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:14px;height:100vh;overflow:hidden;}

/* Header */
.header{background:var(--surface);border-bottom:1px solid var(--border);padding:12px 20px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}
.header-left{display:flex;align-items:center;gap:12px;}
.logo{color:var(--gold);font-size:1.2rem;font-weight:700;letter-spacing:2px;}
.logo-sub{color:var(--text-dim);font-size:0.75rem;letter-spacing:1px;}
.header-right{display:flex;align-items:center;gap:10px;}
.refresh-indicator{color:var(--text-dim);font-size:0.7rem;}
.btn{background:var(--gold);color:#111;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:0.8rem;font-weight:600;letter-spacing:0.5px;}
.btn:hover{background:var(--gold-dim);}

/* Stats bar */
.stats-bar{display:flex;gap:0;border-bottom:1px solid var(--border);flex-shrink:0;}
.stat-card{flex:1;padding:14px 20px;background:var(--surface);border-right:1px solid var(--border);text-align:center;}
.stat-card:last-child{border-right:none;}
.stat-value{color:var(--gold);font-size:1.5rem;font-weight:700;}
.stat-label{color:var(--text-dim);font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;margin-top:2px;}

/* Main layout */
.main{display:flex;flex:1;overflow:hidden;height:calc(100vh - 110px);}

/* Contact list panel */
.contacts-panel{width:360px;min-width:300px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;flex-shrink:0;}
.panel-header{padding:12px;border-bottom:1px solid var(--border);display:flex;flex-direction:column;gap:8px;}
.search-box{width:100%;padding:8px 12px;background:var(--surface2);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:0.85rem;outline:none;}
.search-box:focus{border-color:var(--gold);}
.filter-row{display:flex;gap:4px;}
.filter-btn{flex:1;padding:6px 4px;background:var(--surface2);border:1px solid var(--border);border-radius:4px;color:var(--text-dim);cursor:pointer;font-size:0.7rem;text-align:center;}
.filter-btn.active{background:var(--gold);color:#111;border-color:var(--gold);font-weight:600;}
.contact-list{flex:1;overflow-y:auto;}
.contact-item{padding:12px 16px;border-bottom:1px solid var(--border);cursor:pointer;transition:background 0.15s;}
.contact-item:hover{background:var(--surface2);}
.contact-item.active{background:var(--surface2);border-left:3px solid var(--gold);}
.contact-phone{font-weight:600;font-size:0.9rem;color:var(--text);}
.contact-preview{color:var(--text-dim);font-size:0.8rem;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:280px;}
.contact-meta{display:flex;justify-content:space-between;align-items:center;margin-top:4px;}
.contact-time{color:var(--text-dim);font-size:0.7rem;}
.contact-count{background:var(--gold);color:#111;font-size:0.65rem;font-weight:700;padding:2px 6px;border-radius:10px;}

/* Chat panel */
.chat-panel{flex:1;display:flex;flex-direction:column;background:var(--bg);}
.chat-header{padding:14px 20px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;}
.chat-header-phone{font-weight:600;font-size:1rem;}
.chat-header-info{color:var(--text-dim);font-size:0.75rem;}
.chat-messages{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:8px;}
.chat-empty{flex:1;display:flex;align-items:center;justify-content:center;color:var(--text-dim);font-size:0.9rem;}

/* Chat bubbles */
.msg-group{display:flex;flex-direction:column;gap:4px;margin-bottom:8px;}
.msg-time-divider{text-align:center;color:var(--text-dim);font-size:0.7rem;margin:12px 0;padding:4px 12px;background:var(--surface);border-radius:10px;display:inline-block;align-self:center;}
.bubble{max-width:70%;padding:10px 14px;border-radius:12px;font-size:0.85rem;line-height:1.5;word-wrap:break-word;position:relative;}
.bubble-customer{background:var(--customer-bg);align-self:flex-start;border-bottom-left-radius:4px;}
.bubble-bot{background:var(--bot-bg);align-self:flex-end;border-bottom-right-radius:4px;border:1px solid rgba(197,165,78,0.2);}
.bubble-label{font-size:0.65rem;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:3px;font-weight:600;}
.bubble-customer .bubble-label{color:var(--text-dim);}
.bubble-bot .bubble-label{color:var(--gold);}
.bubble-time{font-size:0.65rem;color:var(--text-dim);margin-top:4px;text-align:right;}

/* Mobile */
.back-btn{display:none;background:none;border:none;color:var(--gold);font-size:1.2rem;cursor:pointer;padding:4px 8px;margin-right:8px;}

/* Scrollbar */
::-webkit-scrollbar{width:6px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:var(--text-dim);}

/* Loading */
.loading{text-align:center;padding:40px;color:var(--text-dim);}
.spinner{display:inline-block;width:24px;height:24px;border:2px solid var(--border);border-top-color:var(--gold);border-radius:50%;animation:spin 0.8s linear infinite;}
@keyframes spin{to{transform:rotate(360deg);}}

/* No data */
.no-data{text-align:center;padding:40px;color:var(--text-dim);}
.no-data h3{color:var(--gold);margin-bottom:8px;}

/* App wrapper */
.app{display:flex;flex-direction:column;height:100vh;}

/* Mobile responsive */
@media(max-width:768px){
  .contacts-panel{width:100%;position:absolute;top:0;left:0;right:0;bottom:0;z-index:10;display:flex;}
  .chat-panel{width:100%;position:absolute;top:0;left:0;right:0;bottom:0;z-index:20;display:none;}
  .chat-panel.visible{display:flex;}
  .main{position:relative;}
  .back-btn{display:inline-block;}
  .stat-card{padding:10px 8px;}
  .stat-value{font-size:1.1rem;}
  .stat-label{font-size:0.6rem;}
  .bubble{max-width:85%;}
  .header{padding:10px 14px;}
  .logo{font-size:1rem;}
}
</style>
</head>
<body>
<div class="app">
  <div class="header">
    <div class="header-left">
      <div>
        <div class="logo">AURIC JEWELS</div>
        <div class="logo-sub">WhatsApp Dashboard</div>
      </div>
    </div>
    <div class="header-right">
      <span class="refresh-indicator" id="refreshTimer">Auto-refresh in 60s</span>
      <button class="btn" id="csvBtn" onclick="downloadCSV()">Download CSV</button>
    </div>
  </div>

  <div class="stats-bar">
    <div class="stat-card"><div class="stat-value" id="statToday">—</div><div class="stat-label">Conversations Today</div></div>
    <div class="stat-card"><div class="stat-value" id="statCustomers">—</div><div class="stat-label">Unique Customers Today</div></div>
    <div class="stat-card"><div class="stat-value" id="statMonth">—</div><div class="stat-label">Messages This Month</div></div>
    <div class="stat-card"><div class="stat-value" id="statTotal">—</div><div class="stat-label">Total Contacts</div></div>
  </div>

  <div class="main">
    <div class="contacts-panel">
      <div class="panel-header">
        <input type="text" class="search-box" id="searchBox" placeholder="Search by phone number..." oninput="filterContacts()">
        <div class="filter-row">
          <button class="filter-btn active" data-days="" onclick="setFilter(this)">All Time</button>
          <button class="filter-btn" data-days="1" onclick="setFilter(this)">Today</button>
          <button class="filter-btn" data-days="7" onclick="setFilter(this)">7 Days</button>
          <button class="filter-btn" data-days="30" onclick="setFilter(this)">30 Days</button>
        </div>
      </div>
      <div class="contact-list" id="contactList">
        <div class="loading"><div class="spinner"></div><p style="margin-top:8px;">Loading conversations...</p></div>
      </div>
    </div>

    <div class="chat-panel" id="chatPanel">
      <div class="chat-header">
        <div style="display:flex;align-items:center;">
          <button class="back-btn" onclick="goBack()">&larr;</button>
          <div>
            <div class="chat-header-phone" id="chatPhone">Select a conversation</div>
            <div class="chat-header-info" id="chatInfo"></div>
          </div>
        </div>
      </div>
      <div class="chat-messages" id="chatMessages">
        <div class="chat-empty">Select a customer from the list to view their conversation</div>
      </div>
    </div>
  </div>
</div>

<script>
const PASS = '${pass}';
const API_URL = '/api/conversations?pass=' + PASS;
let allData = null;
let currentFilter = '';
let currentPhone = null;
let refreshInterval = null;
let refreshCountdown = 60;

// Format phone for display
function formatPhone(phone) {
  if (!phone) return '';
  const s = String(phone);
  if (s.length === 12 && s.startsWith('91')) {
    return '+91 ' + s.slice(2,7) + ' ' + s.slice(7);
  }
  return '+' + s;
}

// Format timestamp
function formatTime(ts) {
  const d = new Date(ts);
  const now = new Date();
  const isToday = d.toDateString() === now.toDateString();
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  const isYesterday = d.toDateString() === yesterday.toDateString();
  const time = d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true });
  if (isToday) return time;
  if (isYesterday) return 'Yesterday ' + time;
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' }) + ' ' + time;
}

// Format date divider
function formatDateDivider(ts) {
  const d = new Date(ts);
  const now = new Date();
  if (d.toDateString() === now.toDateString()) return 'Today';
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  if (d.toDateString() === yesterday.toDateString()) return 'Yesterday';
  return d.toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
}

// Escape HTML
function esc(str) {
  const d = document.createElement('div');
  d.textContent = str || '';
  return d.innerHTML;
}

// Fetch data
async function fetchData() {
  try {
    let url = API_URL;
    if (currentFilter) url += '&days=' + currentFilter;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    allData = await resp.json();
    renderStats(allData.stats);
    renderContacts(allData.conversations);
    if (currentPhone) {
      const conv = allData.conversations.find(c => c.phone === currentPhone);
      if (conv) renderChat(conv);
    }
  } catch (err) {
    console.error('Fetch error:', err);
    document.getElementById('contactList').innerHTML = '<div class="no-data"><h3>Connection Error</h3><p>Could not load conversations. Retrying...</p></div>';
  }
}

// Render stats
function renderStats(stats) {
  if (!stats) return;
  document.getElementById('statToday').textContent = stats.todayConversations || 0;
  document.getElementById('statCustomers').textContent = stats.todayCustomers || 0;
  document.getElementById('statMonth').textContent = stats.monthMessages || 0;
  document.getElementById('statTotal').textContent = stats.totalContacts || 0;
}

// Render contact list
function renderContacts(conversations) {
  const list = document.getElementById('contactList');
  const searchTerm = document.getElementById('searchBox').value.trim().toLowerCase();

  if (!conversations || conversations.length === 0) {
    list.innerHTML = '<div class="no-data"><h3>No Conversations Yet</h3><p>When customers message the WhatsApp bot, their conversations will appear here.</p></div>';
    return;
  }

  let filtered = conversations;
  if (searchTerm) {
    filtered = conversations.filter(c => String(c.phone).includes(searchTerm));
  }

  if (filtered.length === 0) {
    list.innerHTML = '<div class="no-data"><p>No matches for "' + esc(searchTerm) + '"</p></div>';
    return;
  }

  list.innerHTML = filtered.map(c => {
    const isActive = currentPhone === c.phone ? ' active' : '';
    const displayName = c.contact.customerName ? esc(c.contact.customerName) : esc(formatPhone(c.phone));
    const subtitle = c.contact.customerName ? '<span style="color:var(--text-dim);font-size:0.75rem;">' + esc(formatPhone(c.phone)) + '</span><br>' : '';
    return '<div class="contact-item' + isActive + '" onclick="selectContact(\\'' + c.phone + '\\')">' +
      '<div class="contact-phone">' + displayName + '</div>' +
      subtitle +
      '<div class="contact-preview">' + esc(c.contact.lastMessagePreview) + '</div>' +
      '<div class="contact-meta">' +
        '<span class="contact-time">' + formatTime(c.contact.lastMessageTime) + '</span>' +
        '<span class="contact-count">' + c.contact.messageCount + ' msgs</span>' +
      '</div></div>';
  }).join('');
}

// Select a contact
function selectContact(phone) {
  currentPhone = phone;
  const conv = allData.conversations.find(c => c.phone === phone);
  if (conv) renderChat(conv);
  renderContacts(allData.conversations);
  // Mobile: show chat panel
  document.getElementById('chatPanel').classList.add('visible');
}

// Render chat messages
function renderChat(conv) {
  document.getElementById('chatPhone').textContent = formatPhone(conv.phone);
  document.getElementById('chatInfo').textContent = conv.messages.length + ' messages';

  const container = document.getElementById('chatMessages');
  if (!conv.messages || conv.messages.length === 0) {
    container.innerHTML = '<div class="chat-empty">No messages found</div>';
    return;
  }

  let html = '';
  let lastDate = '';

  conv.messages.forEach(msg => {
    const msgDate = formatDateDivider(msg.timestamp);
    if (msgDate !== lastDate) {
      html += '<div class="msg-time-divider">' + msgDate + '</div>';
      lastDate = msgDate;
    }

    const time = new Date(msg.timestamp).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true });

    // Customer message
    if (msg.customerMessage) {
      html += '<div class="bubble bubble-customer">' +
        '<div class="bubble-label">Customer</div>' +
        esc(msg.customerMessage) +
        '<div class="bubble-time">' + time + '</div></div>';
    }

    // Bot reply
    if (msg.botReply) {
      html += '<div class="bubble bubble-bot">' +
        '<div class="bubble-label">Auric Bot</div>' +
        esc(msg.botReply) +
        '<div class="bubble-time">' + time + '</div></div>';
    }
  });

  container.innerHTML = html;
  container.scrollTop = container.scrollHeight;
}

// Go back (mobile)
function goBack() {
  document.getElementById('chatPanel').classList.remove('visible');
  currentPhone = null;
}

// Filter contacts by search
function filterContacts() {
  if (allData) renderContacts(allData.conversations);
}

// Set date filter
function setFilter(el) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  currentFilter = el.dataset.days;
  fetchData();
}

// Download CSV
function downloadCSV() {
  if (!allData || !allData.conversations || allData.conversations.length === 0) {
    alert('No data to export');
    return;
  }

  const rows = [['Date', 'Time', 'Phone', 'Customer Message', 'Bot Reply']];

  allData.conversations.forEach(conv => {
    conv.messages.forEach(msg => {
      const d = new Date(msg.timestamp);
      const date = d.toLocaleDateString('en-IN');
      const time = d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true });
      const csvEsc = (s) => '"' + String(s || '').replace(/"/g, '""') + '"';
      rows.push([date, time, conv.phone, csvEsc(msg.customerMessage), csvEsc(msg.botReply)]);
    });
  });

  const csv = rows.map(r => r.join(',')).join('\\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'auric-whatsapp-conversations-' + new Date().toISOString().slice(0,10) + '.csv';
  a.click();
  URL.revokeObjectURL(url);
}

// Auto-refresh
function startRefresh() {
  refreshCountdown = 60;
  clearInterval(refreshInterval);
  refreshInterval = setInterval(() => {
    refreshCountdown--;
    document.getElementById('refreshTimer').textContent = 'Auto-refresh in ' + refreshCountdown + 's';
    if (refreshCountdown <= 0) {
      refreshCountdown = 60;
      fetchData();
    }
  }, 1000);
}

// Init
fetchData();
startRefresh();
</script>
</body>
</html>`;
}
