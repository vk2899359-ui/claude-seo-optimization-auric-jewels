"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const fetchTasks = useCallback(async () => {
    const res = await fetch("/api/tasks");
    if (res.ok) {
      const data = await res.json();
      setTasks(data.tasks);
    }
  }, []);

  useEffect(() => {
    async function init() {
      const res = await fetch("/api/me");
      if (!res.ok) {
        router.push("/");
        return;
      }
      const data = await res.json();
      setUser(data.user);
      await fetchTasks();
      setLoading(false);
    }
    init();
  }, [router, fetchTasks]);

  async function toggleTask(taskId) {
    const res = await fetch(`/api/tasks/${taskId}`, { method: "PATCH" });
    if (res.ok) {
      setTasks((prev) =>
        prev.map((t) =>
          t.id === taskId ? { ...t, completed: !t.completed } : t
        )
      );
    }
  }

  async function handleLogout() {
    await fetch("/api/auth/logout", { method: "POST" });
    router.push("/");
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner" />
        <p>Loading...</p>
      </div>
    );
  }

  const completedCount = tasks.filter((t) => t.completed).length;
  const totalCount = tasks.length;
  const progressPercent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-left">
          <h1>Auric Task Portal</h1>
          <span className="user-badge">
            {user?.name} ({user?.role})
          </span>
        </div>
        <button onClick={handleLogout} className="logout-button">
          Sign Out
        </button>
      </header>

      <div className="progress-section">
        <div className="progress-text">
          <span>{completedCount} of {totalCount} tasks completed</span>
          <span className="progress-percent">{progressPercent}%</span>
        </div>
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      <div className="task-list">
        {tasks.length === 0 ? (
          <div className="empty-state">
            <p>No tasks found. Ask the admin to initialize the database.</p>
          </div>
        ) : (
          tasks.map((task) => (
            <div
              key={task.id}
              className={`task-item ${task.completed ? "completed" : ""}`}
            >
              <button
                className="task-checkbox"
                onClick={() => toggleTask(task.id)}
                aria-label={task.completed ? "Mark incomplete" : "Mark complete"}
              >
                {task.completed ? "\u2705" : "\u2B1C"}
              </button>
              <div className="task-content">
                <span className="task-title">{task.title}</span>
                <div className="task-meta">
                  <span className={`priority priority-${task.priority}`}>
                    {task.priority}
                  </span>
                  {user?.role === "admin" && (
                    <span className="task-assignee">
                      {task.assignee === "user_admin" ? "You" : "Employee"}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
