import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config'

import '@/assets/style.css'
import 'primeflex/primeflex.min.css'
import 'primeicons/primeicons.css'
import 'primevue/resources/themes/lara-dark-amber/theme.css'

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import InputGroup from 'primevue/inputgroup'
import Skeleton from 'primevue/skeleton'

const app = createApp(App)
app.use(PrimeVue)

app.component('Button', Button)
app.component('InputText', InputText)
app.component('InputGroup', InputGroup)
app.component('Skeleton', Skeleton)

app.mount('#app')
document.title = 'Starduck'