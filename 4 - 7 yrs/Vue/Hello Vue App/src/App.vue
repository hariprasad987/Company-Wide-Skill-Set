<script setup>
const message = "Hello from Vue!";
</script>

<template>
  <main class="page-shell">
    <section class="greeting-card">
      <div class="vue-mark" aria-hidden="true">V</div>
      <p class="eyebrow">My first Vue app</p>
      <h1>{{ message }}</h1>
      <p class="description">
        This component is rendered with Vue 3 and served by Vite.
      </p>
    </section>
  </main>
</template>
