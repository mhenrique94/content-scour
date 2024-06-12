<template>
  <div class="pa-4">
    <h3>Files</h3>
    <form @submit.prevent="onSubmit">
      <v-file-input multiple ref="filesInput" label="Select file" />
      <v-btn type="submit" :disabled="uploading">Send</v-btn>
    </form>

    <v-card class="mt-5 pa-3" color="grey">
      <h2>Documents</h2>
      <v-card color="black" class="documents-container">
        <div v-for="document in documents" :key="document.id">
          <div class="d-flex justify-space-between align-center pb-2">
            <span class="mr-2">{{ document.filename }} ({{ document.file_type }})</span>
            <div>
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
          <v-divider />
        </div>
      </v-card>
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
    const response = await coreStore.processDocument(id)
    documents.value = response.documents
  } catch (error) {
    console.error(error)
  } finally {
    processing.value = false
  }
}

</script>

<style scoped>
.documents-container {
  background-color: black;
  min-height: 200px;
  padding: 16px;
}
</style>