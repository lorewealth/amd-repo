<script setup>

import { uploadRun } from '@/api/runs'
import { useRouter } from 'vue-router'
import { useRunsStore } from '@/stores/runs'
import { ref } from 'vue'

const file = ref(null)
const error = ref('')
const router = useRouter()
const runsStore = useRunsStore()
const loading = ref(false)

const isDragging = ref(false)

function onDrop(e){
  isDragging.value = false
  file.value = e.dataTransfer.files[0] ?? null
  error.value = ''
}

function removeFile(){
  file.value = null
  error.value = ''
}

async function onSubmit(){
  error.value = ''
  loading.value = true
  try {
    const run = await uploadRun(file.value)
    await runsStore.fetchRuns()
    router.push({name: 'run-detail', params: {id: run.id}})
  }
  catch (e) {error.value = e.response?.data?.detail || 'Upload esuat'}
  finally { loading.value = false }
}

function onFileChange(e){
  error.value = ''
  file.value = e.target.files[0] ?? null
}

</script>

<template>
  <div class="wrapper">
    <div>
      <label for="file-input" class="btn">Adauga log</label>
      <input id="file-input" class="hidden-input" :disabled="loading" type='file' accept=".txt" @change="onFileChange"/>
      <button :disabled="!file || loading" @click="onSubmit" type='button' class="btn">
        <span v-if="loading" class="spinner"></span>
        {{loading ? 'Se incarca...' : 'Incarca Fisier'}}
      </button>
      <button :disabled="!file || loading" @click="removeFile" type='button' class="btn">
        Scoate Fisier
      </button>
    </div>
    <div class="dropzone"
      :class="{ dragging: isDragging }"
      @dragover.prevent="isDragging = true"
      @dragleave="isDragging = false"
      @drop.prevent="onDrop">
    <p v-if="file">{{ file.name }}</p>
    <p v-else> Trage log-ul aici sau apasa "Adauga Log"</p>
    </div>
    <p v-if="error">{{error}}</p>
  </div>
</template>

<style scoped>

.spinner{
  display:inline-block;
  width:1em;
  height:1em;
  border:2px solid transparent;
  border-top-color:currentColor;
  border-radius:50%;
  animation:spin 0.6s linear infinite;
  vertical-align:-0.15em;
}
@keyframes spin{
  to {transform: rotate(360deg);}
}

.hidden-input{
  display: none;
}

.wrapper{
  max-width:1250px;
  margin: 0 auto;
  margin-top:15px;
  display:flex;
  flex-direction: column;
  align-items:center;
}

.dropzone{
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 48px 24px;
  text-align: center;
  display:flex;
  align-items:center;
  justify-content:center;
  color: rgba(255, 255, 255, 0.6);
  width: 100%;
  max-width:1200px;
  min-height:40vh;
}
.dropzone.dragging{
  border-color: #3fb950;
  background: rgba(46, 160, 67, 0.15);
}
</style>
