import AppLayout from '@/layout/AppLayout.vue';
// import { createRouter } from 'vue-router';
import { createRouter, createWebHashHistory } from 'vue-router';
const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },

                {
                    path: '/search',
                    name: 'search',
                    component: () => import('@/views/uikit/SearchForm.vue')
                },
                // {
                //     path: '/search/results',
                //     name: 'SearchResultList',
                //     component: () => import('@/views/uikit/SearchResultList.vue')
                // },

                {
                    path: '/search/results',
                    name: 'search-results',
                    component: () => import('@/views/uikit/SearchResultList.vue')
                    // props: true
                    // props: (route) => ({
                    //     query: route.query.query, // 传递搜索关键词
                    //     searchType: route.query.searchType // 传递搜索类型
                    // })
                },
                {
                    path: '/download',
                    name: 'download',
                    component: () => import('@/views/uikit/Download.vue')
                },
                {
                    path: '/submit',
                    name: 'submit',
                    component: () => import('@/views/uikit/SubmitPage.vue')
                },
                {
                    path: '/predict',
                    name: 'predict',
                    component: () => import('@/views/uikit/PredictPage.vue')
                },
                {
                    path: '/predict/result/:taskId',
                    component: () => import('@/views/uikit/PredictResultPage.vue')
                },

                {
                    path: '/algae',
                    name: 'AlgaeTabs',
                    component: () => import('@/views/uikit/AlgaeTabs.vue')
                },
                {
                    path: '/algae/:id',
                    name: 'AlgaeRecords',
                    component: () => import('@/views/uikit/AlgaeRecords.vue'), // The new page to display records
                    props: true // Pass the route params as props
                },
                {
                    path: '/algicides/:id',
                    name: 'ChemicalRecords',
                    component: () => import('@/views/uikit/ChemicalRecords.vue'), // The new page to display records
                    props: true // Pass the route params as props
                },
                {
                    path: '/algicides',
                    name: 'ChemicalTabs',
                    component: () => import('@/views/uikit/ChemicalTabs.vue')
                },
                {
                    path: '/algicides/:id',
                    name: 'ChemicalList',
                    component: () => import('@/views/uikit/ChemicalTable.vue')
                },
                {
                    path: '/references',
                    name: 'references',
                    component: () => import('@/views/uikit/Reference.vue')
                },
                {
                    path: '/chat',
                    name: 'chat',
                    component: () => import('@/views/uikit/GptHelp.vue')
                }
                // {
                //     path: '/documentation',
                //     name: 'documentation',
                //     component: () => import('@/views/uikit/Documentation.vue')
                // }
            ]
        }
    ]
});

export default router;
