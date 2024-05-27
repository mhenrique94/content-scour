<template>
  <div>
    {{ answer.choices[0].message.content }}
  </div>
</template>

<script setup>
const props = defineProps({
  answer: Object
})
</script>