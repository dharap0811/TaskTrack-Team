
const taskList = document.getElementById("task-list");
const taskForm = document.getElementById("task-form");
const taskInput = document.getElementById("task-input");
const message = document.getElementById("message");

let tasks = [];
let currentFilter = "all";

document.getElementById("today").textContent =
  new Date().toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric"
  });

function showError(text) {
  message.textContent = text;
}

async function loadTasks() {
  try {
    const response = await fetch("/tasks");
    if (!response.ok) throw new Error("Unable to load tasks");

    tasks = await response.json();
    showError("");
    renderTasks();
  } catch (error) {
    showError(error.message);
  }
}

function renderTasks() {
  const completed = tasks.filter(task => task.completed).length;

  document.getElementById("total").textContent = tasks.length;
  document.getElementById("completed").textContent = completed;
  document.getElementById("pending").textContent =
    tasks.length - completed;

  document.getElementById("task-count").textContent =
    `${tasks.length} ${tasks.length === 1 ? "task" : "tasks"}`;

  const filtered = tasks.filter(task => {
    if (currentFilter === "completed") return task.completed;
    if (currentFilter === "pending") return !task.completed;
    return true;
  });

  taskList.replaceChildren();

  if (filtered.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty";
    empty.textContent = "No tasks here yet. Add your first task!";
    taskList.appendChild(empty);
    return;
  }

  filtered.forEach(task => {
    const row = document.createElement("div");
    row.className = `task-item ${task.completed ? "done" : ""}`;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.disabled = task.completed;
    checkbox.setAttribute("aria-label", `Complete ${task.title}`);

    checkbox.addEventListener("change", async () => {
      try {
        const response = await fetch(
          `/tasks/${encodeURIComponent(task.id)}/complete`,
          { method: "PATCH" }
        );

        if (!response.ok) throw new Error("Could not complete task");

        await loadTasks();
      } catch (error) {
        checkbox.checked = false;
        showError(error.message);
      }
    });

    const title = document.createElement("span");
    title.className = "task-title";
    title.textContent = task.title;

    const status = document.createElement("span");
    status.className = "status";
    status.textContent = task.completed ? "Completed" : "Pending";

    row.append(checkbox, title, status);
    taskList.appendChild(row);
  });
}

taskForm.addEventListener("submit", async event => {
  event.preventDefault();

  const title = taskInput.value.trim();
  if (!title) return;

  try {
    const response = await fetch("/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });

    if (!response.ok) throw new Error("Could not create task");

    taskInput.value = "";
    currentFilter = "all";
    updateFilters();
    await loadTasks();
  } catch (error) {
    showError(error.message);
  }
});

function updateFilters() {
  document.querySelectorAll(".filter").forEach(button => {
    button.classList.toggle(
      "active",
      button.dataset.filter === currentFilter
    );
  });
}

document.querySelectorAll(".filter").forEach(button => {
  button.addEventListener("click", () => {
    currentFilter = button.dataset.filter;
    updateFilters();
    renderTasks();
  });
});

loadTasks();
