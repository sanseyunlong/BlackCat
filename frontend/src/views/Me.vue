<template>
  <v-container class="fill-height align-start pa-0">
    <div class="w-100 h-100 d-flex flex-column">
      <!-- Close Button -->
      <div class="pa-4 d-flex justify-end">
        <button class="close-btn" @click="router.back()">
          <v-icon icon="mdi-close" size="24" />
        </button>
      </div>

      <div class="pa-6 text-center">
        <div class="avatar-container mb-4">
          <img
            src="https://api.dicebear.com/7.x/avataaars/svg?seed=User"
            alt="Avatar"
            class="avatar-img"
          />
        </div>
        <h2 class="text-h2 font-weight-bold mb-1">我的账户</h2>
        <p class="text-caption text-secondary">管理个人偏好</p>
      </div>

      <div class="px-6 mt-6">
        <div class="setting-item d-flex justify-between align-center py-4" @click="logout">
          <span class="text-body text-error">退出登录</span>
          <v-icon icon="mdi-chevron-right" size="20" color="grey" />
        </div>
      </div>
      
      <div class="mt-auto mb-16 pb-6 text-center">
        <p class="text-caption text-secondary">BlackCat v0.1.0</p>
      </div>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const dark = ref(true)

watch(dark, (v) => {
  // Toggle theme logic
})

function logout() {
  auth.setAuthed(false)
  auth.setCsrf('')
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.avatar-container {
  width: 100px;
  height: 100px;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid var(--surface-color);
  box-shadow: var(--shadow-lg);
  position: relative;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: var(--surface-variant);
}

.setting-item {
  border-radius: var(--radius-lg);
  background: var(--surface-color);
  border: 1px solid var(--border-light);
  margin-bottom: 12px;
  padding: 16px 20px;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
}

.setting-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.setting-item:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}

.text-error {
  color: var(--error-color);
  font-weight: 500;
}

.close-btn {
  background: var(--surface-color);
  border: 1px solid var(--border-light);
  color: var(--text-secondary);
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
}

.close-btn:hover {
  background: var(--surface-variant);
  color: var(--text-primary);
  transform: rotate(90deg);
}

.close-btn:active {
  transform: scale(0.95);
}
</style>