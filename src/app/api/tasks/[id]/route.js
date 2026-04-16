import { NextResponse } from "next/server";
import { getSession } from "@/lib/auth";
import { redis } from "@/lib/redis";

export async function PATCH(request, { params }) {
  const user = await getSession();
  if (!user) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  const { id } = await params;
  const task = await redis.hgetall(`task:${id}`);
  if (!task || !task.id) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }

  // Only admin or the assigned employee can toggle
  if (user.role !== "admin" && task.assignee !== user.id) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const newCompleted = task.completed === "true" ? "false" : "true";
  await redis.hset(`task:${id}`, { completed: newCompleted });

  return NextResponse.json({
    ok: true,
    task: { ...task, completed: newCompleted === "true" },
  });
}
