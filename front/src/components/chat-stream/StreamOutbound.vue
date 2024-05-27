<template>
  <div>
    {{ query }}
  </div>
</template>

<script setup>
const props = defineProps({
  query: String
})
</script>