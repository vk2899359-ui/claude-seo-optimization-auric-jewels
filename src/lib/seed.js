import { redis } from "./redis";
import { hashPassword } from "./auth";

const DEFAULT_USERS = [
  {
    id: "user_admin",
    username: "vinod",
    role: "admin",
    name: "Vinod Kumar",
  },
  {
    id: "user_employee",
    username: "employee",
    role: "employee",
    name: "Team Member",
  },
];

const DEFAULT_PASSWORDS = {
  vinod: "admin123",
  employee: "emp123",
};

const DEFAULT_TASKS = [
  { id: "t1", title: "Check and respond to customer inquiries", assignee: "user_employee", priority: "high" },
  { id: "t2", title: "Update inventory count for gold items", assignee: "user_employee", priority: "high" },
  { id: "t3", title: "Clean and arrange display counters", assignee: "user_employee", priority: "medium" },
  { id: "t4", title: "Process pending online orders", assignee: "user_employee", priority: "high" },
  { id: "t5", title: "Verify daily cash register balance", assignee: "user_employee", priority: "high" },
  { id: "t6", title: "Follow up with repair/alteration customers", assignee: "user_employee", priority: "medium" },
  { id: "t7", title: "Update product photos on website", assignee: "user_employee", priority: "low" },
  { id: "t8", title: "Prepare packaging for deliveries", assignee: "user_employee", priority: "medium" },
  { id: "t9", title: "Log new stock arrivals in system", assignee: "user_employee", priority: "high" },
  { id: "t10", title: "Review daily sales report", assignee: "user_admin", priority: "high" },
  { id: "t11", title: "Approve pending purchase orders", assignee: "user_admin", priority: "high" },
  { id: "t12", title: "Review employee attendance log", assignee: "user_admin", priority: "medium" },
  { id: "t13", title: "Check social media engagement metrics", assignee: "user_admin", priority: "low" },
  { id: "t14", title: "Update gold/diamond pricing board", assignee: "user_admin", priority: "high" },
  { id: "t15", title: "Coordinate with goldsmith for custom orders", assignee: "user_admin", priority: "medium" },
  { id: "t16", title: "Review and approve marketing creatives", assignee: "user_admin", priority: "medium" },
  { id: "t17", title: "Check CCTV and security system status", assignee: "user_admin", priority: "low" },
  { id: "t18", title: "Plan next week's promotional offers", assignee: "user_admin", priority: "low" },
];

export async function seedDatabase() {
  // Seed users
  for (const user of DEFAULT_USERS) {
    const password = DEFAULT_PASSWORDS[user.username];
    const hashed = hashPassword(password);
    await redis.hset(`user:${user.username}`, {
      ...user,
      password: hashed,
    });
  }

  // Seed tasks
  for (const task of DEFAULT_TASKS) {
    await redis.hset(`task:${task.id}`, {
      ...task,
      completed: "false",
      createdAt: new Date().toISOString(),
    });
  }

  // Store task index
  await redis.del("tasks:index");
  for (const task of DEFAULT_TASKS) {
    await redis.sadd("tasks:index", task.id);
  }

  return { users: DEFAULT_USERS.length, tasks: DEFAULT_TASKS.length };
}
