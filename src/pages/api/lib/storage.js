// Storage module: Vercel KV with in-memory fallback
let kvClient = null;
let kvInitialized = false;

// In-memory fallback store (resets on cold starts — only useful for local dev)
const memoryStore = new Map();

function getKV() {
  if (kvInitialized) return kvClient;
  kvInitialized = true;

  const url = process.env.KV_REST_API_URL;
  const token = process.env.KV_REST_API_TOKEN;

  if (!url || !token) {
    console.warn('KV credentials missing (need KV_REST_API_URL + KV_REST_API_TOKEN) — using in-memory storage');
    return null;
  }

  try {
    const vercelKv = require('@vercel/kv');
    if (typeof vercelKv.createClient === 'function') {
      kvClient = vercelKv.createClient({ url, token });
    } else {
      kvClient = vercelKv.kv || (vercelKv.default && vercelKv.default.kv) || null;
    }

    if (!kvClient) {
      console.error('Could not initialize @vercel/kv client — using in-memory storage');
      return null;
    }

    console.log('Vercel KV storage initialized successfully');
    return kvClient;
  } catch (err) {
    console.error('Failed to load @vercel/kv:', err.message, '— using in-memory storage');
    return null;
  }
}

// Generic get/set wrappers
async function kvGet(key) {
  const store = getKV();
  if (store) {
    return await store.get(key);
  }
  return memoryStore.get(key) || null;
}

async function kvSet(key, value) {
  const store = getKV();
  if (store) {
    await store.set(key, value);
  } else {
    memoryStore.set(key, value);
  }
}

// Store a conversation pair (customer message + bot reply)
async function storeConversation({ phone, customerName, customerMessage, botReply, messageType = 'text' }) {
  const timestamp = Date.now();
  const entry = {
    timestamp,
    phone,
    customerName: customerName || '',
    customerMessage,
    botReply,
    messageType,
    status: 'replied',
    date: new Date(timestamp).toISOString(),
  };

  // Get existing messages for this phone
  const messagesKey = `messages:${phone}`;
  const existing = (await kvGet(messagesKey)) || [];
  existing.push(entry);
  await kvSet(messagesKey, existing);

  // Update contacts list
  const contacts = (await kvGet('contacts')) || {};
  contacts[phone] = {
    phone,
    customerName: customerName || contacts[phone]?.customerName || '',
    lastMessageTime: timestamp,
    lastMessagePreview: customerMessage.substring(0, 80),
    messageCount: (contacts[phone]?.messageCount || 0) + 1,
  };
  await kvSet('contacts', contacts);

  return entry;
}

// Get all contacts sorted by most recent
async function getContacts() {
  const contacts = (await kvGet('contacts')) || {};
  return Object.values(contacts).sort((a, b) => b.lastMessageTime - a.lastMessageTime);
}

// Get messages for a specific phone number
async function getMessages(phone) {
  const messagesKey = `messages:${phone}`;
  return (await kvGet(messagesKey)) || [];
}

// Get all conversations (all phones, all messages)
async function getAllConversations({ days = null } = {}) {
  const contacts = (await kvGet('contacts')) || {};
  const phones = Object.keys(contacts);
  const cutoff = days ? Date.now() - days * 24 * 60 * 60 * 1000 : 0;

  const result = [];
  for (const phone of phones) {
    const messages = await getMessages(phone);
    const filtered = cutoff ? messages.filter((m) => m.timestamp >= cutoff) : messages;
    if (filtered.length > 0) {
      result.push({
        phone,
        contact: contacts[phone],
        messages: filtered,
      });
    }
  }

  result.sort((a, b) => b.contact.lastMessageTime - a.contact.lastMessageTime);
  return result;
}

// Get stats
async function getStats() {
  const contacts = (await kvGet('contacts')) || {};
  const phones = Object.keys(contacts);

  const now = Date.now();
  const todayStart = new Date().setHours(0, 0, 0, 0);
  const monthStart = new Date(new Date().getFullYear(), new Date().getMonth(), 1).getTime();

  let todayConversations = 0;
  let monthMessages = 0;
  let todayCustomers = new Set();

  for (const phone of phones) {
    const messages = await getMessages(phone);
    for (const msg of messages) {
      if (msg.timestamp >= todayStart) {
        todayConversations++;
        todayCustomers.add(phone);
      }
      if (msg.timestamp >= monthStart) {
        monthMessages++;
      }
    }
  }

  return {
    todayConversations,
    todayCustomers: todayCustomers.size,
    monthMessages,
    totalContacts: phones.length,
  };
}

module.exports = { storeConversation, getContacts, getMessages, getAllConversations, getStats };
