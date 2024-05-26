<script setup>
import WelcomeItem from './WelcomeItem.vue'
import WelcomeSearch from './WelcomeSearch.vue'
</script>

<template>
  <WelcomeItem>
    <template #heading>Content-Scour</template>
    <h1>Scour the web.</h1>
  </WelcomeItem>
  <WelcomeSearch />

</template>
