from flask import Flask, request, redirect, url_for
from datetime import datetime
import json
import os
 
app = Flask(__name__)
 
DATA_FILE = "todos.json"
 
def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []
 
def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)
 
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Python To-Do App</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', sans-serif;
      background: #f0f2f5;
      min-height: 100vh;
      padding: 2rem 1rem;
    }}
    .container {{ max-width: 600px; margin: 0 auto; }}
    h1 {{
      text-align: center;
      font-size: 2rem;
      font-weight: 700;
      color: #1a1a2e;
      margin-bottom: 0.25rem;
    }}
    .subtitle {{
      text-align: center;
      color: #888;
      font-size: 0.85rem;
      margin-bottom: 2rem;
    }}
    .stats {{
      display: flex;
      gap: 1rem;
      margin-bottom: 1.5rem;
    }}
    .stat {{
      flex: 1;
      background: #fff;
      border-radius: 10px;
      padding: 0.85rem;
      text-align: center;
      box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }}
    .stat-num {{ font-size: 1.6rem; font-weight: 700; }}
    .stat-label {{ font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #999; margin-top: 2px; }}
    .add-form {{
      display: flex;
      gap: 0.6rem;
      margin-bottom: 1.5rem;
    }}
    .add-form input {{
      flex: 1;
      padding: 0.75rem 1rem;
      border: 1px solid #ddd;
      border-radius: 8px;
      font-size: 0.9rem;
      outline: none;
    }}
    .add-form input:focus {{ border-color: #4f46e5; box-shadow: 0 0 0 3px rgba(79,70,229,0.1); }}
    .btn-add {{
      background: #4f46e5;
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 0.75rem 1.25rem;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
    }}
    .btn-add:hover {{ background: #4338ca; }}
    .task-list {{ display: flex; flex-direction: column; gap: 0.5rem; }}
    .task {{
      background: #fff;
      border-radius: 10px;
      padding: 0.85rem 1rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.07);
      border-left: 4px solid #4f46e5;
    }}
    .task.completed {{ border-left-color: #d1d5db; opacity: 0.65; }}
    .task-text {{ flex: 1; font-size: 0.9rem; color: #1a1a2e; }}
    .task.completed .task-text {{ text-decoration: line-through; color: #9ca3af; }}
    .task-date {{ font-size: 0.7rem; color: #aaa; white-space: nowrap; }}
    .btn-toggle {{
      background: #f3f4f6;
      border: 1px solid #d1d5db;
      border-radius: 6px;
      padding: 4px 10px;
      font-size: 0.75rem;
      cursor: pointer;
      color: #374151;
    }}
    .btn-toggle:hover {{ background: #e5e7eb; }}
    .task.completed .btn-toggle {{ background: #d1fae5; border-color: #6ee7b7; color: #065f46; }}
    .btn-delete {{
      background: transparent;
      border: 1px solid #fca5a5;
      border-radius: 6px;
      padding: 4px 10px;
      font-size: 0.75rem;
      cursor: pointer;
      color: #ef4444;
    }}
    .btn-delete:hover {{ background: #fef2f2; }}
    .empty {{
      text-align: center;
      padding: 3rem 1rem;
      color: #aaa;
      font-size: 0.9rem;
    }}
    .empty-icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>📋 To-Do App</h1>
    <p class="subtitle">Built with Python Flask &amp; Docker</p>
 
    <div class="stats">
      <div class="stat">
        <div class="stat-num" style="color:#4f46e5">{total}</div>
        <div class="stat-label">Total</div>
      </div>
      <div class="stat">
        <div class="stat-num" style="color:#f59e0b">{pending}</div>
        <div class="stat-label">Pending</div>
      </div>
      <div class="stat">
        <div class="stat-num" style="color:#10b981">{done}</div>
        <div class="stat-label">Done</div>
      </div>
    </div>
 
    <form class="add-form" method="POST" action="/add">
      <input type="text" name="task" placeholder="Add a new task..." required autocomplete="off"/>
      <button class="btn-add" type="submit">+ Add</button>
    </form>
 
    <div class="task-list">
      {task_html}
    </div>
  </div>
</body>
</html>
"""
 
TASK_HTML = """
<div class="task {completed_class}">
  <span class="task-text">{text}</span>
  <span class="task-date">{created_at}</span>
  <form method="POST" action="/toggle/{id}" style="display:inline">
    <button class="btn-toggle" type="submit">{toggle_label}</button>
  </form>
  <form method="POST" action="/delete/{id}" style="display:inline">
    <button class="btn-delete" type="submit">Delete</button>
  </form>
</div>
"""
 
EMPTY_HTML = """
<div class="empty">
  <div class="empty-icon">🗒️</div>
  <p>No tasks yet. Add one above!</p>
</div>
"""
 
@app.route("/")
def index():
    todos = load_todos()
    total   = len(todos)
    done    = sum(1 for t in todos if t["completed"])
    pending = total - done
 
    task_html = ""
    for todo in reversed(todos):
        task_html += TASK_HTML.format(
            id            = todo["id"],
            text          = todo["text"],
            created_at    = todo["created_at"],
            completed_class = "completed" if todo["completed"] else "",
            toggle_label  = "✓ Done" if todo["completed"] else "Mark Done",
        )
 
    if not task_html:
        task_html = EMPTY_HTML
 
    html = HTML_TEMPLATE.format(
        total   = total,
        done    = done,
        pending = pending,
        task_html = task_html,
    )
    return html
 
@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form.get("task", "").strip()
    if task_text:
        todos = load_todos()
        todos.append({
            "id":         int(datetime.now().timestamp() * 1000),
            "text":       task_text,
            "completed":  False,
            "created_at": datetime.now().strftime("%b %d, %Y"),
        })
        save_todos(todos)
    return redirect(url_for("index"))
 
@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == task_id:
            todo["completed"] = not todo["completed"]
            break
    save_todos(todos)
    return redirect(url_for("index"))
 
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    todos = load_todos()
    todos = [t for t in todos if t["id"] != task_id]
    save_todos(todos)
    return redirect(url_for("index"))
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)