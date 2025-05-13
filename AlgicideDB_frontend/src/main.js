// import { createApp } from 'vue';
// import App from './App.vue';
// import router from './router';

// // import '@primevue/resources/primevue.min.css'; // PrimeVue基础样式文件
// import Aura from '@primevue/themes/aura';
// import PrimeVue from 'primevue/config';
// import ConfirmationService from 'primevue/confirmationservice';
// import ToastService from 'primevue/toastservice';

// import '@/assets/styles.scss';
// import '@/assets/tailwind.css';

// import axios from 'axios';
// axios.defaults.baseURL = 'http://127.0.0.1:8000';

// const app = createApp(App);

// app.use(router, axios);
// app.use(PrimeVue, {
//     theme: {
//         preset: Aura,
//         options: {
//             darkModeSelector: '.app-dark'
//         }
//     }
// });
// app.use(ToastService);
// app.use(ConfirmationService);

// app.mount('#app');

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import '@/assets/styles.scss';
import '@/assets/tailwind.css';
import { definePreset } from '@primevue/themes';
import Aura from '@primevue/themes/aura';
import axios from 'axios'; // 引入 Axios
import { createPinia } from 'pinia'; // 引入 Pinia
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import store from './store';
// 配置 Axios 的全局基础 URL
axios.defaults.baseURL = 'http://algicidedb.ocean-meta.com';
// axios.defaults.baseURL = 'http://47.96.137.15:8030';

// 创建 Vue 实例
const app = createApp(App);
const pinia = createPinia(); // 创建 Pinia 实例

// 注册 Pinia 和 Axios
app.use(pinia); // 注册 Pinia
app.use(router);
app.use(store);

const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{cyan.50}',
            100: '{cyan.100}',
            200: '{cyan.200}',
            300: '{cyan.300}',
            400: '{cyan.400}',
            500: '{cyan.500}',
            600: '{cyan.600}',
            700: '{cyan.700}',
            800: '{cyan.800}',
            900: '{cyan.900}',
            950: '{cyan.950}'
        }
    }
});

// { name: 'cyan', palette: { 50: '#f0f9ff', 100: '#e0f2fe', 200: '#bae6fd', 300: '#7dd3fc', 400: '#38bdf8', 500: '#0ea5e9', 600: '#0284c7', 700: '#0369a1', 800: '#075985', 900: '#0c4a6e', 950: '#082f49' } },

app.use(PrimeVue, {
    theme: {
        preset: MyPreset,
        options: {
            darkModeSelector: '.app-dark'
        }
    }
});
app.use(ToastService);
app.use(ConfirmationService);

// 注册 Axios 到 Vue 全局
app.config.globalProperties.$axios = axios;

// 挂载 Vue 实例
app.mount('#app');
