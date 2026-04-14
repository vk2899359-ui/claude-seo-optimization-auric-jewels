const { storeConversation } = require('./lib/storage');

// Environment variables expected:
//   WHATSAPP_VERIFY_TOKEN  — Meta webhook verification token
//   WHATSAPP_ACCESS_TOKEN  — Meta Graph API access token
//   WHATSAPP_PHONE_ID      — WhatsApp Business phone number ID
//   ANTHROPIC_API_KEY      — Claude API key (for AI replies)

const VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN || 'auric_verify_token';
const ACCESS_TOKEN = process.env.WHATSAPP_ACCESS_TOKEN;
const PHONE_ID = process.env.WHATSAPP_PHONE_ID;
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const BOT_PHONE_NUMBER = process.env.BOT_PHONE_NUMBER || '9012495941';

module.exports = async function handler(req, res) {
  // GET: Meta webhook verification
  if (req.method === 'GET') {
    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    const challenge = req.query['hub.challenge'];

    if (mode === 'subscribe' && token === VERIFY_TOKEN) {
      console.log('Webhook verified');
      return res.status(200).send(challenge);
    }
    return res.status(403).send('Forbidden');
  }

  // POST: Incoming WhatsApp messages
  if (req.method === 'POST') {
    try {
      const body = req.body;

      if (body?.object !== 'whatsapp_business_account') {
        return res.status(200).send('OK');
      }

      const entries = body.entry || [];
      for (const entry of entries) {
        const changes = entry.changes || [];
        for (const change of changes) {
          const value = change.value;

          // Skip status update webhooks (sent/delivered/read receipts)
          if (value?.statuses) {
            console.log('Skipping status update webhook');
            continue;
          }

          if (!value?.messages) continue;

          const messages = value.messages;
          const contacts = value.contacts || [];

          // Build a phone→name lookup from the contacts array
          const contactNames = {};
          for (const c of contacts) {
            if (c.wa_id && c.profile?.name) {
              contactNames[c.wa_id] = c.profile.name;
            }
          }

          for (const message of messages) {
            const from = message.from; // customer phone number
            const messageType = message.type || 'text';
            const customerName = contactNames[from] || '';

            // Skip messages from the bot's own number to prevent reply loops
            if (from === BOT_PHONE_NUMBER) {
              console.log('Skipping message from bot itself:', from);
              continue;
            }

            let customerMessage = '';

            // Extract message text based on type
            if (message.type === 'text') {
              customerMessage = message.text?.body || '';
            } else if (message.type === 'image') {
              customerMessage = '[Image]' + (message.image?.caption ? ': ' + message.image.caption : '');
            } else if (message.type === 'audio') {
              customerMessage = '[Audio message]';
            } else if (message.type === 'video') {
              customerMessage = '[Video]' + (message.video?.caption ? ': ' + message.video.caption : '');
            } else if (message.type === 'document') {
              customerMessage = '[Document: ' + (message.document?.filename || 'file') + ']';
            } else if (message.type === 'location') {
              customerMessage = '[Location]';
            } else {
              customerMessage = '[' + message.type + ' message]';
            }

            if (!customerMessage) continue;

            // Generate AI reply using Claude
            let botReply = '';
            try {
              botReply = await generateAIReply(customerMessage, from);
            } catch (err) {
              console.error('AI reply error:', err.message);
              botReply = 'Thank you for your message! Our team will get back to you shortly. For immediate assistance, please call us.';
            }

            // Send reply via WhatsApp
            try {
              await sendWhatsAppMessage(from, botReply);
            } catch (err) {
              console.error('WhatsApp send error:', err.message);
            }

            // Store conversation in KV (dashboard storage)
            try {
              await storeConversation({
                phone: from,
                customerName,
                customerMessage,
                botReply,
                messageType,
              });
              console.log('Conversation stored for', from, customerName ? `(${customerName})` : '');
            } catch (err) {
              console.error('Storage error:', err.message);
              // Don't fail the webhook if storage fails
            }
          }
        }
      }

      return res.status(200).send('OK');
    } catch (err) {
      console.error('Webhook error:', err);
      return res.status(200).send('OK'); // Always 200 to avoid Meta retries
    }
  }

  return res.status(405).send('Method not allowed');
};

// Generate AI reply using Claude API
async function generateAIReply(customerMessage, phone) {
  if (!ANTHROPIC_API_KEY) {
    return 'Thank you for contacting Auric Jewels! Our team will assist you shortly.';
  }

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 500,
      system: `You are the WhatsApp assistant for Auric Jewels, a premium jewellery showroom in Gurgaon, India.
You help customers with:
- Product inquiries (gold, diamond, platinum jewellery)
- Store location and timings (Sector 14, Gurgaon, 10 AM - 8 PM)
- Pricing information (guide them to visit store for exact pricing)
- Appointments and bookings
- Custom jewellery orders
Keep responses concise, friendly, and professional. Use simple language. Reply in the same language the customer uses (Hindi/English).`,
      messages: [{ role: 'user', content: customerMessage }],
    }),
  });

  if (!response.ok) {
    throw new Error('Claude API error: ' + response.status);
  }

  const data = await response.json();
  return data.content?.[0]?.text || 'Thank you for your message! Please visit our store for more details.';
}

// Send WhatsApp message via Meta Graph API
async function sendWhatsAppMessage(to, text) {
  if (!ACCESS_TOKEN || !PHONE_ID) {
    console.warn('WhatsApp credentials not configured, skipping send');
    return;
  }

  const response = await fetch(
    `https://graph.facebook.com/v19.0/${PHONE_ID}/messages`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${ACCESS_TOKEN}`,
      },
      body: JSON.stringify({
        messaging_product: 'whatsapp',
        to,
        type: 'text',
        text: { body: text },
      }),
    }
  );

  if (!response.ok) {
    const err = await response.text();
    throw new Error('WhatsApp API error: ' + err);
  }
}
