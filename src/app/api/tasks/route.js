import { NextResponse } from "next/server";
import { getSession } from "@/lib/auth";
import { redis } from "@/lib/redis";

export async function GET() {
  const user = await getSession();
  if (!user) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  const taskIds = await redis.smembers("tasks:index");
  if (!taskIds || taskIds.length === 0) {
    return NextResponse.json({ tasks: [] });
  }

  const tasks = [];
  for (const id of taskIds) {
    const task = await redis.hgetall(`task:${id}`);
    if (task && task.id) {
      task.completed = task.completed === "true";
      // Admin sees all tasks; employee sees only their own
      if (user.role === "admin" || task.assignee === user.id) {
        tasks.push(task);
      }
    }
  }

  // Sort by priority (high > medium > low), then by id
  const priorityOrder = { high: 0, medium: 1, low: 2 };
  tasks.sort((a, b) => {
    const pa = priorityOrder[a.priority] ?? 3;
    const pb = priorityOrder[b.priority] ?? 3;
    if (pa !== pb) return pa - pb;
    return a.id.localeCompare(b.id, undefined, { numeric: true });
  });

  return NextResponse.json({ tasks });
}
