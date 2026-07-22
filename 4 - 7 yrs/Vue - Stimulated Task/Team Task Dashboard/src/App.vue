<script setup>
import { computed, ref } from "vue";

const filters = ["All", "Active", "Completed"];
const activeFilter = ref("All");
const newTask = ref("");
const nextId = ref(5);
const tasks = ref([
  { id: 1, title: "Review product requirements", owner: "Maya", completed: true },
  { id: 2, title: "Build dashboard components", owner: "Noah", completed: false },
  { id: 3, title: "Prepare usability test", owner: "Isha", completed: false },
  { id: 4, title: "Publish release notes", owner: "Leo", completed: true },
]);

const completedCount = computed(() => tasks.value.filter((task) => task.completed).length);
const activeCount = computed(() => tasks.value.length - completedCount.value);
const progress = computed(() =>
  tasks.value.length ? Math.round((completedCount.value / tasks.value.length) * 100) : 0,
);
const visibleTasks = computed(() => {
  if (activeFilter.value === "Active") return tasks.value.filter((task) => !task.completed);
  if (activeFilter.value === "Completed") return tasks.value.filter((task) => task.completed);
  return tasks.value;
});

function addTask() {
  const title = newTask.value.trim();
  if (!title) return;
  tasks.value.push({ id: nextId.value++, title, owner: "You", completed: false });
  newTask.value = "";
  activeFilter.value = "All";
}

function removeTask(id) {
  tasks.value = tasks.value.filter((task) => task.id !== id);
}
</script>

<template>
  <main class="app-shell">
    <section class="dashboard">
      <header>
        <div>
          <p class="eyebrow">Vue stimulated task</p>
          <h1>Team Task Dashboard</h1>
          <p class="subtitle">Keep the sprint focused and moving forward.</p>
        </div>
        <div class="date-card">
          <span>Today</span>
          <strong>22 Jul</strong>
        </div>
      </header>

      <div class="metrics">
        <article><span>Total tasks</span><strong>{{ tasks.length }}</strong></article>
        <article><span>In progress</span><strong>{{ activeCount }}</strong></article>
        <article><span>Completed</span><strong>{{ completedCount }}</strong></article>
        <article class="progress-card">
          <div><span>Progress</span><strong>{{ progress }}%</strong></div>
          <div class="progress-track"><div :style="{ width: `${progress}%` }"></div></div>
        </article>
      </div>

      <form class="task-form" @submit.prevent="addTask">
        <input v-model="newTask" aria-label="New task title" placeholder="Add a new task…" />
        <button type="submit">Add task</button>
      </form>

      <div class="toolbar">
        <h2>Tasks</h2>
        <div class="filters" aria-label="Task filters">
          <button
            v-for="filter in filters"
            :key="filter"
            type="button"
            :class="{ active: activeFilter === filter }"
            @click="activeFilter = filter"
          >
            {{ filter }}
          </button>
        </div>
      </div>

      <ul class="task-list">
        <li v-for="task in visibleTasks" :key="task.id" :class="{ done: task.completed }">
          <label>
            <input v-model="task.completed" type="checkbox" />
            <span class="checkmark">✓</span>
            <span class="task-copy">
              <strong>{{ task.title }}</strong>
              <small>Assigned to {{ task.owner }}</small>
            </span>
          </label>
          <button class="delete" type="button" :aria-label="`Delete ${task.title}`" @click="removeTask(task.id)">×</button>
        </li>
        <li v-if="visibleTasks.length === 0" class="empty">No tasks in this view.</li>
      </ul>
    </section>
  </main>
</template>
