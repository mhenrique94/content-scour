<template>
  <div class="speech-bubble">
    <p>
      {{ query }}
    </p>
  </div>
</template>

<script setup>
const props = defineProps({
  query: String
})
</script>

<style scoped>
.speech-bubble {
  display: flex;
  justify-content: flex-end;
  margin: 16px;
}

p {
	position: relative;
	background-color: #c0c0c0;
	padding: 1.125em 1.5em;
	font-size: 1.25em;
	border-radius: 1rem;
  box-shadow:	0 0.125rem 0.5rem rgba(0, 0, 0, .3), 0 0.0625rem 0.125rem rgba(0, 0, 0, .2);
  margin-bottom: 24px;
  color: black;
  max-width: 90%;
}

p::before {
	content: '';
	position: absolute;
	width: 0;
	height: 0;
	top: 100%;
	right: 1.5em;
	border: .75rem solid transparent;
	border-bottom: none;
	border-top-color: #c0c0c0;
	filter: drop-shadow(0 -0.0625rem 0.0625rem rgba(0, 0, 0, .1));
}
</style>