import { cookies } from "next/headers";
import crypto from "crypto";
import { redis } from "./redis";

const SESSION_TTL = 60 * 60 * 24; // 24 hours

export async function createSession(user) {
  const sessionId = crypto.randomBytes(32).toString("hex");
  await redis.set(`session:${sessionId}`, JSON.stringify(user), {
    ex: SESSION_TTL,
  });
  const cookieStore = await cookies();
  cookieStore.set("session", sessionId, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: SESSION_TTL,
    path: "/",
  });
  return sessionId;
}

export async function getSession() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get("session")?.value;
  if (!sessionId) return null;
  const data = await redis.get(`session:${sessionId}`);
  if (!data) return null;
  return typeof data === "string" ? JSON.parse(data) : data;
}

export async function destroySession() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get("session")?.value;
  if (sessionId) {
    await redis.del(`session:${sessionId}`);
    cookieStore.set("session", "", { maxAge: 0, path: "/" });
  }
}

export function hashPassword(password) {
  const secret = process.env.SESSION_SECRET || "fallback";
  return crypto.createHmac("sha256", secret).update(password).digest("hex");
}
