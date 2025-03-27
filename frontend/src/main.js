import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './assets/css/fonts.css'
import './assets/css/colors.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

router.afterEach((to) => {
  console.log('переход')
  document.title = to.meta.metaTitle || 'TimeFlow';
});

app.mount('#app')
