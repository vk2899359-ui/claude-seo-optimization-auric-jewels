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
  return m.includes('ring') || m.includes('diamond ring');
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
  return m.includes('catalogue') || m.includes('catalog') || m.includes('collection dikhao') ||
    m.includes('collection') && (m.includes('dikhao') || m.includes('show'));
}

function isAddressQuery(msg) {
  const m = msg.toLowerCase();
  return m.includes('address') || m.includes('showroom kahan') || m.includes('location') ||
    m.includes('kahan hai') || m.includes('where') && m.includes('shop');
}

function isTimingQuery(msg) {
  const m = msg.toLowerCase();
  return m.includes('timing') || m.includes(' open') || m.includes('kab khulta') ||
    m.includes('kab band') || m.includes('hours') || m.includes('time');
}

// ── Live gold rate scraper ────────────────────────────────────────────────────

async function fetchLiveGoldRates() {
  const url = 'https://www.goodreturns.in/gold-rates-in-gurgaon.html';
  const res = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36',
      'Accept': 'text/html',
    },
  });
  if (!res.ok) throw new Error('GoodReturns fetch failed: ' + res.status);
  const html = await res.text();

  // Parse rates from table rows — GoodReturns uses patterns like "24K Gold" ... "₹XX,XXX"
  const rates = { '24K': null, '22K': null, '18K': null };

  // Try to match rows containing karat labels and rupee amounts
  const rowRe = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
  let rowMatch;
  while ((rowMatch = rowRe.exec(html)) !== null) {
    const row = rowMatch[1];
    const karat = /24\s*K/i.test(row) ? '24K' : /22\s*K/i.test(row) ? '22K' : /18\s*K/i.test(row) ? '18K' : null;
    if (!karat) continue;
    // Find a rupee amount like ₹70,000 or 70,000
    const priceMatch = row.match(/[₹Rs.]*\s*([\d,]{5,})/);
    if (priceMatch && !rates[karat]) {
      rates[karat] = priceMatch[1].replace(/,/g, '');
    }
  }

  // Fallback: scan entire HTML for karat+price proximity
  if (!rates['24K'] || !rates['22K'] || !rates['18K']) {
    const flatRe = /(?:24|22|18)\s*K[^₹\d]{0,80}[₹Rs.]*\s*([\d,]{5,})/gi;
    let fm;
    while ((fm = flatRe.exec(html)) !== null) {
      const karatStr = fm[0].match(/(\d+)\s*K/i)?.[1];
      if (!karatStr) continue;
      const key = karatStr + 'K';
      if (!rates[key]) rates[key] = fm[1].replace(/,/g, '');
    }
  }

  return rates;
}

function formatGoldRateMessage(rates) {
  const now = new Date();
  const dateStr = `${now.getDate()} ${MONTHS[now.getMonth()]} ${now.getFullYear()}`;

  const fmt = (val) => val ? `₹${Number(val).toLocaleString('en-IN')}/10g` : 'N/A';

  return (
    `📈 *Aaj ka Gold Rate — Gurgaon*\n` +
    `_(Date: ${dateStr})_\n\n` +
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

// Returns { text, imageUrl, imageCaption, followUpText } or null (fall through to AI)
async function keywordRouter(msg, from) {
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
        '📍 *Auric Jewels*\nShop No. 45, Sector 45\nGurugram, Haryana 122003\n\n📞 +91 90124 95941\n🌐 www.auricjewels.com\n\nGoogle Maps: https://maps.app.goo.gl/auricjewels',
    };
  }

  if (isTimingQuery(msg)) {
    return {
      text: '🕙 *Store Timings*\n10 AM – 8 PM, 7 days a week\n\n📍 Sector 45, Gurugram\n📞 +91 90124 95941',
    };
  }

  return null; // fall through to AI
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
          if (!value?.messages) continue;

          const messages = value.messages;

          for (const message of messages) {
            const from = message.from;
            const messageType = message.type || 'text';
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
            const kwResult = await keywordRouter(customerMessage, from);

            if (kwResult) {
              // Send image if present
              if (kwResult.imageUrl) {
                try {
                  await sendWhatsAppImage(from, kwResult.imageUrl, kwResult.imageCaption || '');
                } catch (err) {
                  console.error('Image send error:', err.message);
                }
              }
              // Send main text if present
              if (kwResult.text) {
                try {
                  await sendWhatsAppMessage(from, kwResult.text);
                } catch (err) {
                  console.error('Text send error:', err.message);
                }
                botReply = kwResult.text;
              }
              // Send follow-up text if present (e.g. catalogue link)
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
            try {
              await storeConversation({ phone: from, customerMessage, botReply, messageType });
            } catch (err) {
              console.error('Storage error:', err.message);
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
