<template>
  <div class="pa-4">
    <h3>Document upload</h3>
    <h4>Formats accepted: .TXT, .PDF, .CSV</h4>
    <form @submit.prevent="onSubmit">
      <v-file-input
        ref="filesInput"
        clear-on-submit
        multiple
        label="Select file"
        accept="text/plain, application/pdf, .csv"
      />
      <v-btn type="submit" :disabled="uploading">Send</v-btn>
    </form>

    <v-card class="mt-5 pa-3 documents-card" color="grey">
      <h2 class="text-black">Documents</h2>
      <v-card v-if="documents.length" class="documents-container">
        <div v-for="document in documents" :key="document.id">
          <div class="d-flex justify-space-between align-center pb-2">
            <span class="mr-2 text-white">
              {{ new Date(document.uploaded_at) }} {{ document.filename }}.{{ document.file_type }}
            </span>
            <div class="text-white">
              <v-btn
                v-if="!document.processed" @click="processDocument(document.id)"
                class="mr-2"
              >
                <v-icon color="black">mdi-orbit-variant</v-icon>
              </v-btn>
              <span v-else class="mr-2">Processed</span>
              <v-btn @click="deleteDocument(document.id)" class="mr-2">
                <v-icon color="black">mdi-delete</v-icon>
              </v-btn>
            </div>
          </div>
          <v-divider class="text-white"/>
        </div>
      </v-card>
      <div v-else class="documents-container">Nothing here, YET!</div>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCoreStore } from '@/stores/core'

const coreStore = useCoreStore()

const documents = ref([])
const uploading = ref(false)
const loadingFiles = ref(false)
const deleting = ref(false)
const processing = ref(false)
const filesInput = ref(null)

onMounted( async() => {
  try {
    loadingFiles.value = true
    documents.value = await coreStore.listDocuments()
  } catch (error) {
    console.error(error)
  } finally {
    loadingFiles.value = false
  }
})

const onSubmit = async () => {
  uploading.value = true
  const formData = new FormData()
  
  for (const file of filesInput.value.files) {
    formData.append('files', file)
  }

  try {
    documents.value = await coreStore.submitDocuments(formData)
  } catch (error) {
    console.error(error)
  } finally {
    uploading.value = false
  }
}

const deleteDocument = async (id) => {
  deleting.value = true
  try {
    documents.value = await coreStore.deleteDocument(id)
  } catch (error) {
    console.error(error)
  } finally {
    deleting.value = false
  }
}

const processDocument = async (id) => {
  processing.value = true
  try {
    documents.value = await coreStore.processDocument(id)
  } catch (error) {
    console.error(error)
  } finally {
    processing.value = false
  }
}

</script>

<style scoped>
.documents-card {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 260px;
}

.documents-container {
  background-color: var(--color-background);
  height: 100%;
  padding: 16px;
}
</style>