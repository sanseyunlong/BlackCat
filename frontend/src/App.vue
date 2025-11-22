<template>
  <v-app class="minimal-app">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <BottomNav v-if="isAuthed" />
  </v-app>
</template>

<style scoped>
.minimal-app {
  background-color: var(--bg-color) !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<script setup lang="ts">
import BottomNav from './components/BottomNav.vue'
import { useAuthStore } from './stores/auth'
const auth = useAuthStore()
const isAuthed = auth.isAuthed
</script>