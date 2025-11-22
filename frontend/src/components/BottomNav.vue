<template>
  <div class="bottom-nav-wrapper">
    <div class="minimal-nav">
      <router-link to="/home" class="nav-link" active-class="active">
        <v-icon icon="mdi-camera" size="24" />
      </router-link>
      
      <router-link to="/records" class="nav-link" active-class="active">
        <v-icon icon="mdi-format-list-bulleted" size="24" />
      </router-link>
      
      <router-link to="/me" class="nav-link" active-class="active">
        <v-icon icon="mdi-account" size="24" />
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.bottom-nav-wrapper {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-top: 1px solid rgba(255, 255, 255, 0.5);
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 100;
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.04);
}

.minimal-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 72px; /* Slightly taller for better touch targets */
  max-width: 600px;
  margin: 0 auto;
  padding: 0 16px;
}

.nav-link {
  color: var(--text-tertiary);
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 48px;
  border-radius: var(--radius-xl);
  position: relative;
}

.nav-link:hover {
  color: var(--primary-color);
  background: var(--surface-variant);
}

.nav-link.active {
  color: var(--primary-color);
  background: rgba(79, 70, 229, 0.08); /* Primary with low opacity */
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -12px; /* Adjust based on height */
  width: 4px;
  height: 4px;
  background: var(--primary-color);
  border-radius: 50%;
  opacity: 0; /* Hidden for now, maybe too cluttered */
}
</style>