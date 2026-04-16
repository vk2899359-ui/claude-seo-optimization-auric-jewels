import { NextResponse } from "next/server";
import { redis } from "@/lib/redis";
import { createSession, hashPassword } from "@/lib/auth";

export async function POST(request) {
  try {
    const { username, password } = await request.json();

    if (!username || !password) {
      return NextResponse.json(
        { error: "Username and password are required" },
        { status: 400 }
      );
    }

    const user = await redis.hgetall(`user:${username}`);
    if (!user || !user.password) {
      return NextResponse.json(
        { error: "Invalid username or password" },
        { status: 401 }
      );
    }

    const hashed = hashPassword(password);
    if (hashed !== user.password) {
      return NextResponse.json(
        { error: "Invalid username or password" },
        { status: 401 }
      );
    }

    const { password: _, ...safeUser } = user;
    await createSession(safeUser);

    return NextResponse.json({ ok: true, user: safeUser });
  } catch (err) {
    console.error("Login error:", err);
    return NextResponse.json({ error: "Server error" }, { status: 500 });
  }
}
