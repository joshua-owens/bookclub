<template>
  <div class="bg-gray-199 min-h-screen">
    <div class="min-h-screen flex items-center justify-center bg-gray-200 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-7">
        <div>
          <img class="mx-auto h-12 w-auto" src="https://tailwindui.com/img/logos/workflow-mark-indigo-600.svg" alt="Workflow">
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in with Discord
          </h2>
        </div>
        <div>
          <button @click="loginWithDiscord" class="mt-4 w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Login with Discord
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

const props = defineProps({
  discordAuthUrl: {
    type: String,
    required: true,
  }
})

console.log({ props })
function loginWithDiscord() {
  window.location.href = props.discordAuthUrl;
}
</script>
