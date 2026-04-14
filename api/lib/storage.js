// Storage module: Vercel KV with in-memory fallback
let kv = null;
let useMemory = false;

// In-memory fallback store (resets on cold starts)
const memoryStore = new Map();

async function getKV() {
  if (kv) return kv;
  if (useMemory) return null;

  try {
    if (!process.env.KV_REST_API_URL) {
      console.warn('KV not configured, using in-memory storage');
      useMemory = true;
      return null;
    }
    const kvModule = await import('@vercel/kv');
    kv = kvModule.kv;
    return kv;
  } catch (err) {
    console.warn('KV not configured, using in-memory storage:', err.message);
    useMemory = true;
    return null;
  }
}

// Generic get/set wrappers
async function kvGet(key) {
  const store = await getKV();
  if (store) {
    return await store.get(key);
  }
  return memoryStore.get(key) || null;
}

async function kvSet(key, value) {
  const store = await getKV();
  if (store) {
    await store.set(key, value);
  } else {
    memoryStore.set(key, value);
  }
}

// Store a conversation pair (customer message + bot reply)
async function storeConversation({ phone, customerMessage, botReply, messageType = 'text' }) {
  const timestamp = Date.now();
  const entry = {
    timestamp,
    phone,
    customerMessage,
    botReply,
    messageType,
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
