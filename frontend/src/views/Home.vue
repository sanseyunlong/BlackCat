<template>
  <v-container class="fill-height align-start pa-0">
    <div 
      class="home-content w-100 h-100 d-flex flex-column"
      @touchstart="onTouchStart"
      @touchend="onTouchEnd"
    >
      <!-- Header -->
      <div class="pa-6 d-flex justify-between align-center">
        <h1 class="text-h3 font-weight-bold">BlackCat</h1>
        <div class="d-flex align-center gap-4">
          <div class="status-dot" :class="{ active: result }"></div>
          <div class="avatar-btn" @click="router.push('/me')">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=User" alt="Avatar" />
          </div>
        </div>
      </div>

      <!-- Main Area -->
      <div class="flex-grow-1 d-flex flex-column justify-center align-center position-relative pa-4">
        <!-- Upload/Camera Trigger -->
        <div 
          v-if="!previewUrl" 
          class="upload-trigger d-flex flex-column align-center"
          @click="triggerUpload"
        >
          <div class="camera-btn-wrapper mb-4">
            <div class="pulse-ring"></div>
            <div class="camera-btn">
              <v-icon icon="mdi-camera" size="48" color="white" />
            </div>
          </div>
          <p class="text-h6 font-weight-medium text-primary">点击拍摄</p>
          <p class="text-caption text-secondary mb-8">或从相册上传</p>
          
          <div class="swipe-hint d-flex flex-column align-center">
             <v-icon icon="mdi-chevron-up" color="grey-lighten-1" class="animate-bounce" />
             <span class="text-caption text-disabled">上滑查看历史</span>
          </div>
        </div>

        <!-- Preview & Crop -->
        <div v-else class="preview-container w-100 h-100 d-flex flex-column align-center justify-center">
          <div class="image-wrapper mb-6">
            <img ref="cropImg" :src="previewUrl" class="preview-img" />
          </div>
          
          <div class="controls d-flex gap-4 mb-6">
            <button class="minimal-btn outline" @click="initCrop">裁剪</button>
            <button class="minimal-btn" @click="applyCrop">应用</button>
            <button class="minimal-btn text" @click="clearFile">取消</button>
          </div>
        </div>

        <!-- Hidden Input -->
        <input
          ref="fileInput"
          type="file"
          accept="image/*;capture=camera"
          class="d-none"
          @change="onFile"
        />
      </div>

      <!-- Action/Result Area -->
      <div class="action-area pa-6" v-if="file || result">
        <div v-if="result" class="result-display mb-6 text-center">
          <p class="text-caption text-uppercase mb-2">识别结果</p>
          
          <!-- 中文名称 -->
          <h2 class="text-h2 mb-2" v-if="result.label_zh">{{ result.label_zh }}</h2>
          
          <!-- 英文名称和音标 -->
          <div class="mb-2">
            <h3 class="text-h4 d-inline">{{ result.label_en }}</h3>
            <span v-if="result.phonetic" class="text-body-2 text-secondary ml-2">{{ result.phonetic }}</span>
          </div>
          
          <p class="text-caption text-secondary mb-4">置信度: {{ (result.confidence * 100).toFixed(0) }}%</p>
          
          <button class="minimal-btn outline w-100" @click="speak">
            <v-icon icon="mdi-volume-high" start />
            朗读
          </button>
        </div>

        <button
          v-if="file && !result"
          class="minimal-btn w-100"
          :disabled="loading"
          @click="uploadAndRecognize"
        >
          {{ loading ? '分析中...' : '开始识别' }}
        </button>
      </div>
    </div>

    <!-- History Drawer -->
    <v-bottom-sheet v-model="showHistory">
      <div class="history-sheet d-flex flex-column">
        <!-- Header with Swipe Handler -->
        <div 
          class="pa-6 pb-2 d-flex justify-between align-center flex-shrink-0"
          @touchstart="onHeaderTouchStart"
          @touchend="onHeaderTouchEnd"
        >
          <h2 class="text-h4 font-weight-bold">历史记录</h2>
          <v-btn icon="mdi-chevron-down" variant="text" size="large" @click="showHistory = false" />
        </div>
        
        <div class="history-list flex-grow-1 px-6 pb-6 overflow-y-auto">
          <div v-if="records.length === 0" class="text-center py-8 text-secondary">
            暂无记录
          </div>
          <div
            v-for="r in records"
            :key="r.id"
            class="record-item mb-4 d-flex align-center"
            @click="speakRecord(r)"
          >
            <!-- 缩略图 -->
            <div class="record-thumb mr-3">
              <img :src="`/api/images/${r.image_id}`" alt="thumbnail" />
            </div>
            
            <!-- 内容 -->
            <div class="flex-grow-1">
              <h3 class="text-body font-weight-bold mb-1">
                {{ r.label_zh || r.label_en }}
              </h3>
              <p class="text-caption text-secondary mb-1">
                {{ r.label_en }}
                <span v-if="r.phonetic" class="ml-1">{{ r.phonetic }}</span>
              </p>
              <p class="text-caption text-tertiary">{{ formatDate(r.created_at) }}</p>
            </div>
            
            <!-- 右侧操作 -->
            <div class="d-flex align-center gap-3">
              <div class="confidence-badge">
                {{ (r.confidence * 100).toFixed(0) }}%
              </div>
              <v-btn 
                icon="mdi-delete-outline" 
                size="small" 
                variant="text" 
                color="error"
                @click.stop="deleteRecord(r.id)"
              />
            </div>
          </div>
        </div>
      </div>
    </v-bottom-sheet>
  </v-container>
</template>

<script setup lang="ts">
import api from '../services/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'

const router = useRouter()
const file = ref<File|null>(null)
const previewUrl = ref<string>('')
const result = ref<{label_en:string, label_zh?:string, phonetic?:string, confidence:number} | null>(null)
const cropImg = ref<HTMLImageElement | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const loading = ref(false)
let cropper: Cropper | null = null

// History Drawer State
const showHistory = ref(false)
const records = ref<any[]>([])
const touchStartY = ref(0)
const headerTouchStartY = ref(0)

function onTouchStart(e: TouchEvent) {
  touchStartY.value = e.changedTouches[0].screenY
}

function onTouchEnd(e: TouchEvent) {
  const touchEndY = e.changedTouches[0].screenY
  // Swipe up threshold
  if (touchStartY.value - touchEndY > 50) {
    openHistory()
  }
}

function onHeaderTouchStart(e: TouchEvent) {
  headerTouchStartY.value = e.changedTouches[0].screenY
}

function onHeaderTouchEnd(e: TouchEvent) {
  const touchEndY = e.changedTouches[0].screenY
  // Swipe down threshold to close
  if (touchEndY - headerTouchStartY.value > 50) {
    showHistory.value = false
  }
}

async function openHistory() {
  showHistory.value = true
  await loadRecords()
}

async function loadRecords() {
  try {
    const res = await api.get('/records')
    records.value = res.data.items || []
  } catch (e) {
    console.error(e)
  }
}

async function deleteRecord(id: number) {
  if (!confirm('确定要删除这条记录吗？')) return
  try {
    await api.delete(`/records/${id}`)
    // 重新加载记录列表
    await loadRecords()
  } catch (e) {
    console.error(e)
    alert('删除失败')
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

function triggerUpload() {
  fileInput.value?.click()
}

function onFile(e: any) {
  const f = e.target?.files?.[0] || null
  if (f) {
    // 统一转换为 JPEG 格式（支持所有格式包括 MPO、HEIC 等）
    convertToJPEG(f).then(converted => {
      file.value = converted
      previewUrl.value = URL.createObjectURL(converted)
      result.value = null
    })
  }
}

// 将任何格式的图片转换为 JPEG（包括 MPO、HEIC 等）
function convertToJPEG(imageFile: File): Promise<File> {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const maxSize = 1920
        let width = img.width
        let height = img.height
        
        // 如果图片太大，等比缩放
        if (width > height && width > maxSize) {
          height = (height * maxSize) / width
          width = maxSize
        } else if (height > maxSize) {
          width = (width * maxSize) / height
          height = maxSize
        }
        
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        
        // 白色背景（防止透明图片转换后有问题）
        if (ctx) {
          ctx.fillStyle = '#FFFFFF'
          ctx.fillRect(0, 0, width, height)
          ctx.drawImage(img, 0, 0, width, height)
        }
        
        canvas.toBlob((blob) => {
          if (blob) {
            const converted = new File([blob], 'image.jpg', {
              type: 'image/jpeg',
              lastModified: Date.now()
            })
            resolve(converted)
          }
        }, 'image/jpeg', 0.90)
      }
      
      img.onerror = () => {
        // 如果图片加载失败，尝试直接使用原文件
        console.error('Image conversion failed, using original file')
        resolve(imageFile)
      }
      
      img.src = e.target?.result as string
    }
    reader.readAsDataURL(imageFile)
  })
}

function clearFile() {
  file.value = null
  previewUrl.value = ''
  result.value = null
  if (cropper) {
    cropper.destroy()
    cropper = null
  }
  if (fileInput.value) fileInput.value.value = ''
}

function initCrop() {
  if (cropImg.value) {
    cropper?.destroy()
    cropper = new Cropper(cropImg.value, { 
      aspectRatio: 1, 
      viewMode: 1,
      background: false,
      modal: true,
      guides: false,
      highlight: false,
      autoCropArea: 0.8
    })
  }
}

function applyCrop() {
  if (!cropper) return
  cropper.getCroppedCanvas({ width: 512, height: 512 }).toBlob(b => {
    if (b) {
      file.value = new File([b], 'crop.jpg', { type: 'image/jpeg' })
      previewUrl.value = URL.createObjectURL(b)
      cropper?.destroy()
      cropper = null
    }
  }, 'image/jpeg', 0.9)
}

async function uploadAndRecognize() {
  if (!file.value) return
  loading.value = true
  try {
    const form = new FormData()
    form.append('file', file.value)
    const up = await api.post('/images', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    const imgId = up.data.image_id
    const rec = await api.post(`/recognitions/${imgId}`)
    result.value = rec.data
  } catch (e: any) {
    console.error(e)
    if (e.response?.status === 401) {
      // 401 错误会被拦截器处理，自动跳转到登录页
      alert('请先登录')
    } else if (e.response?.status === 413) {
      alert('图片太大，请选择小一些的图片')
    } else {
      alert('识别失败，请重试')
    }
  } finally {
    loading.value = false
  }
}

function speak() {
  if (!result.value) return
  const utter = new SpeechSynthesisUtterance(result.value.label_en)
  utter.rate = 0.9
  utter.pitch = 1.0
  speechSynthesis.speak(utter)
}

function speakRecord(record: any) {
  const utter = new SpeechSynthesisUtterance(record.label_en)
  utter.rate = 0.9
  utter.pitch = 1.0
  speechSynthesis.speak(utter)
}
</script>

<style scoped>
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--border-color);
  transition: background-color 0.3s;
}

.status-dot.active {
  background-color: var(--success-color);
  box-shadow: 0 0 8px var(--success-color);
}

.avatar-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-fast);
}

.avatar-btn:active {
  transform: scale(0.95);
}

.avatar-btn img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-trigger {
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-trigger:active .camera-btn {
  transform: scale(0.9);
}

.camera-btn-wrapper {
  position: relative;
  width: 148px;
  height: 148px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-btn {
  width: 118px;
  height: 118px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  box-shadow: 0 10px 30px rgba(79, 70, 229, 0.4);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.pulse-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 1px solid var(--primary-color);
  opacity: 0.3;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.8); opacity: 0.5; }
  100% { transform: scale(1.4); opacity: 0; }
}

.animate-bounce {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-6px); }
  60% { transform: translateY(-3px); }
}

.preview-img {
  max-width: 100%;
  max-height: 50vh;
  object-fit: contain;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}

.gap-4 {
  gap: 16px;
}

.action-area {
  background: var(--surface-color);
  border-top: 1px solid var(--border-light);
  border-radius: 32px 32px 0 0;
  padding-bottom: 100px !important; /* Space for bottom nav */
  box-shadow: 0 -8px 32px rgba(0,0,0,0.03);
}

.history-sheet {
  background: var(--bg-color);
  height: 100vh;
  max-height: 100vh;
  display: flex;
  flex-direction: column;
  border-radius: 24px 24px 0 0;
}

.record-item {
  padding: 12px;
  border-radius: var(--radius-md);
  background: var(--surface-color);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: all 0.2s;
}

.record-item:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.record-thumb {
  width: 60px;
  height: 60px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--border-color);
  flex-shrink: 0;
}

.record-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.confidence-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  background: var(--surface-variant);
  color: var(--primary-color);
  border-radius: 12px;
  white-space: nowrap;
}
</style>