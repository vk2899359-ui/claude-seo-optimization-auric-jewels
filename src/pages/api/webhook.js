const VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN || "auric_verify";
const WHATSAPP_TOKEN = process.env.WHATSAPP_TOKEN;
const PHONE_NUMBER_ID = process.env.WHATSAPP_PHONE_NUMBER_ID;

async function logToSheet(from, userText, reply) {
  const GOOGLE_SHEET_WEBHOOK = process.env.GOOGLE_SHEET_WEBHOOK;
  if (!GOOGLE_SHEET_WEBHOOK) {
    console.log("GOOGLE_SHEET_WEBHOOK not set, skipping sheet logging");
    return;
  }
  try {
    const res = await fetch(GOOGLE_SHEET_WEBHOOK, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        timestamp: new Date().toISOString(),
        phone: from,
        message: userText,
        reply: reply,
      }),
    });
    console.log("Sheet log status:", res.status);
  } catch (e) {
    console.log("Sheet log error:", e.message);
  }
}

async function sendWhatsAppMessage(to, text) {
  if (!WHATSAPP_TOKEN || !PHONE_NUMBER_ID) {
    console.log("WhatsApp credentials not set, skipping send");
    return;
  }
  const url = `https://graph.facebook.com/v18.0/${PHONE_NUMBER_ID}/messages`;
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${WHATSAPP_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messaging_product: "whatsapp",
        to: to,
        text: { body: text },
      }),
    });
    console.log("WhatsApp send status:", res.status);
  } catch (e) {
    console.log("WhatsApp send error:", e.message);
  }
}

export default async function handler(req, res) {
  // GET — WhatsApp webhook verification
  if (req.method === "GET") {
    const mode = req.query["hub.mode"];
    const token = req.query["hub.verify_token"];
    const challenge = req.query["hub.challenge"];

    if (mode === "subscribe" && token === VERIFY_TOKEN) {
      console.log("Webhook verified");
      return res.status(200).send(challenge);
    }
    return res.status(403).json({ error: "Verification failed" });
  }

  // POST — incoming WhatsApp messages
  if (req.method === "POST") {
    try {
      const body = req.body;
      const entry = body?.entry?.[0];
      const changes = entry?.changes?.[0];
      const value = changes?.value;
      const messages = value?.messages;

      if (!messages || messages.length === 0) {
        return res.status(200).json({ status: "no messages" });
      }

      const msg = messages[0];
      const from = msg.from;
      const userText =
        msg.type === "text" ? msg.text?.body : `[${msg.type} message]`;

      console.log(`Message from ${from}: ${userText}`);

      // Default reply — customize as needed or integrate AI
      const reply = `Thank you for contacting Auric Jewels! We received your message: "${userText}". Our team will get back to you shortly.`;

      await sendWhatsAppMessage(from, reply);
      await logToSheet(from, userText, reply);

      return res.status(200).json({ status: "ok" });
    } catch (err) {
      console.error("Webhook error:", err);
      return res.status(500).json({ error: "Internal server error" });
    }
  }

  return res.status(405).json({ error: "Method not allowed" });
}
