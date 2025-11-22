<template>
  <v-container class="fill-height justify-center pa-0">
    <div class="auth-container w-100 h-100 d-flex flex-column justify-center pa-6" style="max-width: 480px">
      <div class="text-center mb-10">
        <h1 class="text-h2 font-weight-medium mb-2">创建账号</h1>
        <p class="text-body text-medium-emphasis">立即加入 BlackCat</p>
      </div>

      <form @submit.prevent="handleRegister" class="w-100">
        <div class="mb-6">
          <input
            v-model="email"
            type="email"
            placeholder="邮箱"
            class="minimal-input"
            required
            :disabled="step > 1"
          />
        </div>
        
        <div v-if="step === 1" class="mb-8">
          <input
            v-model="password"
            type="password"
            placeholder="设置密码"
            class="minimal-input"
            required
          />
        </div>

        <div v-if="step === 2" class="mb-8">
          <input
            v-model="code"
            type="text"
            placeholder="验证码"
            class="minimal-input"
            required
          />
        </div>

        <button
          type="submit"
          class="minimal-btn w-100 mb-6"
          :disabled="loading"
        >
          {{ loading ? '处理中...' : (step === 1 ? '发送验证码' : '验证并注册') }}
        </button>

        <div class="text-center text-caption">
          <router-link to="/login" class="text-decoration-none text-secondary">
            已有账号？去登录
          </router-link>
        </div>
      </form>
    </div>
    
    <v-snackbar v-model="snackbar" :color="snackbarColor" variant="tonal">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import api from '../services/api'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const code = ref('')
const step = ref(1)
const loading = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

function showMsg(msg: string, color = 'success') {
  snackbarText.value = msg
  snackbarColor.value = color
  snackbar.value = true
}

async function handleRegister() {
  if (step.value === 1) {
    await sendCode()
  } else {
    await verify()
  }
}

async function sendCode() {
  if (!email.value || !password.value) return
  loading.value = true
  try {
    await api.post('/auth/register', { email: email.value, password: password.value })
    showMsg('验证码已发送')
    step.value = 2
  } catch (e) {
    showMsg('发送失败', 'error')
  } finally {
    loading.value = false
  }
}

async function verify() {
  if (!code.value) return
  loading.value = true
  try {
    await api.post('/auth/verify-email', { email: email.value, code: code.value, password: password.value })
    showMsg('注册成功')
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    showMsg('验证失败', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.text-secondary {
  color: var(--text-secondary);
  transition: color 0.2s;
}

.text-secondary:hover {
  color: var(--text-primary);
}
</style>