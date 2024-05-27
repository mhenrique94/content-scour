<template>
  <div class="history-entry">
    <span class="date">{{ formatedDate }}</span>
    <div class="he-speech-bubble">
      <p>
        {{ answer.choices[0].message.content }}
      </p>
    </div>
  </div>
</template>

<script setup>
import dayjs from 'dayjs'
import { computed } from 'vue';

const props = defineProps({
  answer: Object
})

const formatedDate = computed(() => {
	return dayjs(props?.answer?.created * 1000).format('DD/MM/YYYY HH:mm')
})
</script>

<style scoped>
.history-entry {
	display: flex;
	flex-direction: column;
	align-items: flex-end;
	margin: 16px 16px 0  16px;
}
.he-speech-bubble {
  display: flex;
  justify-content: flex-start;
}

p {
	position: relative;
	background-color: #242323;
	padding: 1.125em 1.5em;
	font-size: 1.25em;
	border-radius: 1rem;
  box-shadow:	0 0.125rem 0.5rem rgba(0, 0, 0, .3), 0 0.0625rem 0.125rem rgba(0, 0, 0, .2);
  margin-bottom: 24px;
}

p::before {
	content: '';
	position: absolute;
	width: 0;
	height: 0;
	bottom: 100%;
	left: 1.5em;
	border: .75rem solid transparent;
	border-top: none;
	border-bottom-color: #585757;
	filter: drop-shadow(0 -0.0625rem 0.0625rem rgba(0, 0, 0, .1));
}
</style>