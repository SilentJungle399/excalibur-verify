const {createApp, ref} = Vue

createApp({
    setup() {
        const searchVal = ref('')
        const mode = ref('search')
        const dots = ref('')
        const resStatus = ref({
            message: ''
        })

        const search = () => {
            mode.value = 'processing'
            fetch("/api/text", {
                method: "POST",
                body: JSON.stringify({
                    "text": searchVal.value
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                        resStatus.value.message = data[0][0] > 0.5 ? "correct" : "fake";
                    mode.value = "result";
                })
        }

        setInterval(() => {
            if (dots.value.length === 3) {
                dots.value = ""
            } else {
                dots.value += "."
            }
        }, 500)

        return {
            searchVal, search, mode, resStatus, dots
        }
    }
}).mount('#app')
