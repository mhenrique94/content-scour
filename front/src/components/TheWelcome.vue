<script setup>
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import UserBar from '@/components/UserBar.vue'

const router = useRouter()
const routeName = computed(() => router.currentRoute.value.name)

</script>

<template>
  <v-layout row wrap class="justify-space-between">
    <div class="pa-4">
      <h1>Content Scour</h1>
      <h2>Scour the web.</h2>
    </div>
    <div class="pa-4">
      <h2>{{ routeName }}</h2>
    </div>
    <UserBar />
  </v-layout>
</template>
