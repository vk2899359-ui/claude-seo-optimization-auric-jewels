import { NextResponse } from "next/server";
import { seedDatabase } from "@/lib/seed";

export async function POST(request) {
  const { searchParams } = new URL(request.url);
  const key = searchParams.get("key");

  const secret = process.env.SESSION_SECRET || "";
  const expectedKey = secret.slice(0, 10);

  if (!key || key !== expectedKey) {
    return NextResponse.json({ error: "Invalid key" }, { status: 403 });
  }

  try {
    const result = await seedDatabase();
    return NextResponse.json({
      ok: true,
      seeded: ["users", "tasks"],
      counts: result,
    });
  } catch (err) {
    console.error("Seed error:", err);
    return NextResponse.json({ error: "Seed failed" }, { status: 500 });
  }
}

// Also support GET for easier browser-based seeding
export async function GET(request) {
  return POST(request);
}
