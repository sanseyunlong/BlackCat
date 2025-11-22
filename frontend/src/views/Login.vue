<template>
  <v-container class="fill-height justify-center pa-0">
    <div class="auth-container w-100 h-100 d-flex flex-column justify-center pa-6" style="max-width: 480px">
      <div class="text-center mb-10">
        <img src="/logo.jpg" alt="BlackCat Logo" class="logo-img mb-6" />
        <h1 class="text-h2 font-weight-medium mb-2">BlackCat</h1>
        <p class="text-body text-medium-emphasis">欢迎回来</p>
      </div>

      <form @submit.prevent="doLogin" class="w-100">
        <div class="mb-6">
          <input
            v-model="email"
            type="email"
            placeholder="邮箱"
            class="minimal-input"
            required
          />
        </div>
        
        <div class="mb-8">
          <input
            v-model="password"
            type="password"
            placeholder="密码"
            class="minimal-input"
            required
          />
        </div>

        <button
          type="submit"
          class="minimal-btn w-100 mb-6"
          :disabled="loading"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>

        <div class="d-flex justify-between text-caption">
          <router-link to="/register" class="text-decoration-none text-secondary">
            注册账号
          </router-link>
          <router-link to="/reset" class="text-decoration-none text-secondary">
            忘记密码?
          </router-link>
        </div>
      </form>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import api from '../services/api'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

async function doLogin() {
  if (!email.value || !password.value) return
  loading.value = true
  try {
    const res = await api.post('/auth/login', { email: email.value, password: password.value })
    auth.setAuthed(true)
    auth.setCsrf(res.data.csrf_token)
    router.push('/home')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.logo-img {
  width: 120px;
  height: 120px;
  margin: 0 auto;
  display: block;
  object-fit: contain;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.text-secondary {
  color: var(--text-secondary);
  transition: color 0.2s;
}

.text-secondary:hover {
  color: var(--text-primary);
}
</style>