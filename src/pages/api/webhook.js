const { storeConversation } = require('./lib/storage');

// Environment variables expected:
//   WHATSAPP_VERIFY_TOKEN  — Meta webhook verification token
//   WHATSAPP_ACCESS_TOKEN  — Meta Graph API access token
//   WHATSAPP_PHONE_ID      — WhatsApp Business phone number ID
//   ANTHROPIC_API_KEY      — Claude API key (for AI replies)
//   BOT_PHONE_NUMBER       — Bot's own number (to prevent reply loops)
//   GOLDAPI_KEY            — goldapi.io key for live gold rates (optional)

const VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN || 'auric_verify_token';
const ACCESS_TOKEN = process.env.WHATSAPP_ACCESS_TOKEN;
const PHONE_ID = process.env.WHATSAPP_PHONE_ID;
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const BOT_PHONE_NUMBER = process.env.BOT_PHONE_NUMBER || '9012495941';

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

// ── Keyword matchers ──────────────────────────────────────────────────────────

function isGoldRateQuery(msg) {
  const m = msg.toLowerCase();
  return m.includes('gold rate') || m.includes('gold ka rate') ||
    m.includes('sone ka bhav') || m.includes('aaj ka gold') ||
    m.includes('gold price') || m.includes('sona rate') || m.includes('gold bhav');
}

function isRingsQuery(msg) {
  const m = msg.toLowerCase();
  return m.includes('ring') || m.includes('rings dikhao') || m.includes('diamond ring');
}

function isNecklaceQuery(msg) {
  const m = msg.toLowerCase();
  return m.includes('necklace') || m.includes('haar');
}

function isEarringsQuery(msg) {
  const m = msg.toLowerCase();
  return m.includes('earring');
}

function isCatalogueQuery(msg) {
  const m = msg.toLowerCase();
  return m.includes('catalogue') || m.includes('catalog') ||
    (m.includes('collection') && (m.includes('dikhao') || m.includes('show')));
}

function isAddressQuery(msg) {
  const m = msg.toLowerCase();
  return m.includes('address') || m.includes('showroom kahan') ||
    m.includes('location') || m.includes('kahan hai');
}

function isTimingQuery(msg) {
  const m = msg.toLowerCase();
  return m.includes('timing') || m.includes(' open') || m.includes('kab khulta') ||
    m.includes('kab band') || m.includes('hours');
}

// ── Live gold rate fetcher ────────────────────────────────────────────────────
// Strategy: 1) goldapi.io (if GOLDAPI_KEY set)  2) hardcoded fallback

const GOLD_FALLBACK = { '24K': '97500', '22K': '89375', '18K': '73125', fallback: true };

async function fetchLiveGoldRates() {
  const goldApiKey = process.env.GOLDAPI_KEY;
  if (goldApiKey) {
    try {
      const res = await fetch('https://www.goldapi.io/api/XAU/INR', {
        headers: { 'x-access-token': goldApiKey, 'Content-Type': 'application/json' },
      });
      if (res.ok) {
        const data = await res.json();
        // data.price is per troy oz in INR; convert to per 10g
        // 1 troy oz = 31.1035g → price_per_10g = (price / 31.1035) * 10
        const per10g_24k = Math.round((data.price / 31.1035) * 10);
        return {
          '24K': String(per10g_24k),
          '22K': String(Math.round(per10g_24k * 22 / 24)),
          '18K': String(Math.round(per10g_24k * 18 / 24)),
        };
      }
      console.warn('[Gold] goldapi.io responded', res.status, '— using fallback');
    } catch (e) {
      console.warn('[Gold] goldapi.io error:', e.message, '— using fallback');
    }
  }
  // Return hardcoded fallback with a flag so message can note it
  return GOLD_FALLBACK;
}

function formatGoldRateMessage(rates) {
  const now = new Date();
  const dateStr = `${now.getDate()} ${MONTHS[now.getMonth()]} ${now.getFullYear()}`;
  const fmt = (val) => val ? `₹${Number(val).toLocaleString('en-IN')}/10g` : 'N/A';
  const note = rates.fallback
    ? `_(Rates updated daily — call for exact price)_`
    : `_(Date: ${dateStr} — Live rate)_`;

  return (
    `📈 *Aaj ka Gold Rate — Gurgaon*\n` +
    `${note}\n\n` +
    `- 24K — ${fmt(rates['24K'])}\n` +
    `- 22K — ${fmt(rates['22K'])}\n` +
    `- 18K — ${fmt(rates['18K'])}\n\n` +
    `💎 *Auric Jewels — Sector 45, Gurugram*\n` +
    `BIS Hallmarked Gold | IGI Certified Diamonds\n` +
    `📞 +91 90124 95941\n` +
    `🌐 www.auricjewels.com`
  );
}

// ── WhatsApp senders ──────────────────────────────────────────────────────────

async function sendWhatsAppMessage(to, text) {
  if (!ACCESS_TOKEN || !PHONE_ID) {
    console.warn('WhatsApp credentials not configured, skipping send');
    return;
  }

  const response = await fetch(
    `https://graph.facebook.com/v18.0/${PHONE_ID}/messages`,
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

async function sendWhatsAppImage(to, imageUrl, caption) {
  if (!ACCESS_TOKEN || !PHONE_ID) {
    console.warn('WhatsApp credentials not configured, skipping image send');
    return;
  }

  const response = await fetch(
    `https://graph.facebook.com/v18.0/${PHONE_ID}/messages`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${ACCESS_TOKEN}`,
      },
      body: JSON.stringify({
        messaging_product: 'whatsapp',
        to,
        type: 'image',
        image: { link: imageUrl, caption },
      }),
    }
  );

  if (!response.ok) {
    const err = await response.text();
    throw new Error('WhatsApp image API error: ' + err);
  }
}

// ── Keyword-based response router ─────────────────────────────────────────────

async function keywordRouter(msg) {
  if (isGoldRateQuery(msg)) {
    try {
      const rates = await fetchLiveGoldRates();
      return { text: formatGoldRateMessage(rates) };
    } catch (err) {
      console.error('Gold rate fetch error:', err.message);
      return { text: 'Sorry, live gold rate is temporarily unavailable. Please call us at +91 90124 95941 for the latest rates.\n\n💎 *Auric Jewels — Sector 45, Gurugram*' };
    }
  }

  if (isRingsQuery(msg)) {
    return {
      imageUrl: 'https://www.auricjewels.com/og-image.jpg',
      imageCaption: '💍 Auric Jewels — Diamond Rings Collection\nVisit: www.auricjewels.com\nCall: +91 90124 95941',
      text: '💍 Check out our stunning diamond and gold rings collection!\nVisit us at Sector 45, Gurugram or browse: www.auricjewels.com',
    };
  }

  if (isNecklaceQuery(msg)) {
    return {
      imageUrl: 'https://www.auricjewels.com/og-image.jpg',
      imageCaption: '📿 Auric Jewels — Necklace Collection\nVisit: www.auricjewels.com\nCall: +91 90124 95941',
      text: '📿 Explore our exquisite necklace & haar collection!\nVisit us at Sector 45, Gurugram or browse: www.auricjewels.com',
    };
  }

  if (isEarringsQuery(msg)) {
    return {
      imageUrl: 'https://www.auricjewels.com/og-image.jpg',
      imageCaption: '✨ Auric Jewels — Earrings Collection\nVisit: www.auricjewels.com\nCall: +91 90124 95941',
      text: '✨ Discover our beautiful earrings collection!\nVisit us at Sector 45, Gurugram or browse: www.auricjewels.com',
    };
  }

  if (isCatalogueQuery(msg)) {
    return {
      imageUrl: 'https://www.auricjewels.com/og-image.jpg',
      imageCaption: '💍 Auric Jewels Collection\nVisit: www.auricjewels.com\nCall: +91 90124 95941',
      followUpText: 'Browse our full collection: https://www.auricjewels.com',
    };
  }

  if (isAddressQuery(msg)) {
    return {
      text:
        '📍 *Auric Jewels*\nShop No. 45, Sector 45\nGurugram, Haryana 122003\n\n📞 +91 90124 95941\n🌐 www.auricjewels.com',
    };
  }

  if (isTimingQuery(msg)) {
    return {
      text: '🕙 *Store Timings*\n10 AM – 8 PM, 7 days a week\n\n📍 Sector 45, Gurugram\n📞 +91 90124 95941',
    };
  }

  return null;
}

// ── Main handler ──────────────────────────────────────────────────────────────

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
    console.log('[Webhook] POST received');
    try {
      const body = req.body;

      if (body?.object !== 'whatsapp_business_account') {
        console.log('[Webhook] Ignoring non-whatsapp object:', body?.object);
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

          // Build phone→name lookup
          const contactNames = {};
          for (const c of contacts) {
            if (c.wa_id && c.profile?.name) {
              contactNames[c.wa_id] = c.profile.name;
            }
          }

          for (const message of messages) {
            const from = message.from;
            const messageType = message.type || 'text';
            const customerName = contactNames[from] || '';

            // Skip messages from the bot's own number to prevent reply loops
            if (from === BOT_PHONE_NUMBER) {
              console.log('Skipping message from bot itself:', from);
              continue;
            }

            let customerMessage = '';

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

            let botReply = '';

            // Try keyword router first
            const kwResult = await keywordRouter(customerMessage);

            if (kwResult) {
              if (kwResult.imageUrl) {
                try {
                  console.log('[Image] Sending image to', from, '—', kwResult.imageUrl);
                  await sendWhatsAppImage(from, kwResult.imageUrl, kwResult.imageCaption || '');
                  console.log('[Image] Sent successfully');
                } catch (err) {
                  console.error('[Image] Send FAILED:', err.message, '— sending text fallback');
                  // Text fallback if image fails
                  const fallback = (kwResult.imageCaption || '') + '\nVisit: www.auricjewels.com | Call: +91 90124 95941';
                  try { await sendWhatsAppMessage(from, fallback); } catch (_) {}
                }
              }
              if (kwResult.text) {
                try {
                  await sendWhatsAppMessage(from, kwResult.text);
                } catch (err) {
                  console.error('Text send error:', err.message);
                }
                botReply = kwResult.text;
              }
              if (kwResult.followUpText) {
                try {
                  await sendWhatsAppMessage(from, kwResult.followUpText);
                } catch (err) {
                  console.error('Follow-up send error:', err.message);
                }
                botReply += '\n' + kwResult.followUpText;
              }
            } else {
              // Fall back to AI reply
              try {
                botReply = await generateAIReply(customerMessage, from);
              } catch (err) {
                console.error('AI reply error:', err.message);
                botReply = 'Thank you for your message! Our team will get back to you shortly. For immediate assistance, please call us at +91 90124 95941.';
              }

              try {
                await sendWhatsAppMessage(from, botReply);
              } catch (err) {
                console.error('WhatsApp send error:', err.message);
              }
            }

            // Store conversation
            console.log('[Webhook] Storing conversation for:', from);
            try {
              const stored = await storeConversation({
                phone: from,
                customerName,
                customerMessage,
                botReply,
                messageType,
              });
              console.log('[Webhook] Stored successfully:', JSON.stringify({ phone: from, timestamp: stored?.timestamp }));
            } catch (err) {
              console.error('[Webhook] STORAGE FAILED:', err.message, err.stack);
            }
          }
        }
      }

      return res.status(200).send('OK');
    } catch (err) {
      console.error('Webhook error:', err);
      return res.status(200).send('OK');
    }
  }

  return res.status(405).send('Method not allowed');
};

// ── AI reply (Claude) ─────────────────────────────────────────────────────────

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
- Store location and timings (Sector 45, Gurugram, 10 AM - 8 PM, 7 days)
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
