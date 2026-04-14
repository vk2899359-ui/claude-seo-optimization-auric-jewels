const { getContacts, getMessages, getAllConversations, getStats } = require('./lib/storage');

const PASSWORD = 'auric2026';

module.exports = async function handler(req, res) {
  // CORS headers for dashboard AJAX calls
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Auth check
  const pass = req.query.pass;
  if (pass !== PASSWORD) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const { phone, days } = req.query;

    // If specific phone requested, return that conversation
    if (phone) {
      const messages = await getMessages(phone);
      return res.status(200).json({ phone, messages });
    }

    // Get stats
    const stats = await getStats();

    // Get all conversations with optional days filter
    const daysNum = days ? parseInt(days, 10) : null;
    const conversations = await getAllConversations({ days: daysNum });

    return res.status(200).json({
      stats,
      conversations,
    });
  } catch (err) {
    console.error('Conversations API error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
};
