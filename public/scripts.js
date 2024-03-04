const { createApp, ref } = Vue

  createApp({
    setup() {
      const searchMode = ref('text')
      return {
        searchMode
      }
    }
  }).mount('#app')