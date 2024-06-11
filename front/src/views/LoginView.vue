
<template>
  <v-container v-if="!authStore.loading" fluid fill-height>
    <v-row align="center" justify="center">
      <v-col sm="12" md="6">
        <v-card>
          <v-card-title>Login</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                label="Username"
                required
                type="username"
                v-model="loginForm.username"
              ></v-text-field>
              <v-text-field
                label="Password"
                required
                type="password"
                v-model="loginForm.password"
              ></v-text-field>
              <v-btn type="submit" color="primary">Proceed</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { reactive, ref, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)

watch(isAuthenticated, (isAuthenticated) => {
  if (isAuthenticated) {
    router.push({ path: '/' })
  }
})

const loginForm = reactive({
  username: '',
  password: '',
})


const login = async () => {
  try {
    await authStore.login(loginForm)
    router.push({ path: '/' })
  } catch (error) {
    console.error(error)
  }
}
</script>
