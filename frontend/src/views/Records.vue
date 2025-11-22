<template>
  <v-container class="fill-height align-start pa-0">
    <div class="w-100 h-100 d-flex flex-column">
      <div class="pa-6">
        <h1 class="text-h3 font-weight-bold mb-6">历史记录</h1>
        
        <!-- Search -->
        <div class="mb-6">
          <input
            v-model="date"
            type="date"
            class="minimal-input"
            @change="load"
          />
        </div>
      </div>

      <!-- List -->
      <div class="flex-grow-1 overflow-y-auto px-6 pb-16">
        <div v-if="rows.length === 0" class="text-center py-10 text-secondary">
          暂无记录
        </div>

        <div
          v-for="r in rows"
          :key="r.id"
          class="record-item mb-4 d-flex justify-between align-center"
        >
          <div>
            <h3 class="text-h3 mb-1">{{ r.label_en }}</h3>
            <p class="text-caption">{{ formatDate(r.created_at) }}</p>
          </div>
          <div class="confidence-badge">
            {{ (r.confidence * 100).toFixed(0) }}%
          </div>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'

const date = ref('')
const rows = ref<any[]>([])

async function load() {
  try {
    const res = await api.get('/records', { params: { date: date.value } })
    rows.value = res.data.items || []
  } catch (e) {
    console.error(e)
  }
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(load)
</script>

<style scoped>
.record-item {
  padding: 20px;
  border-radius: var(--radius-lg);
  background: var(--surface-color);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
}

.record-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.confidence-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  background: var(--surface-variant);
  color: var(--primary-color);
  border-radius: 12px;
}
</style>