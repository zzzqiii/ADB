<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
// 通用搜索
const generalSearch = ref('');
const loading = ref(false);
// 高级搜索
const advancedSearchVisible = ref(false);
const advancedQueries = ref([{ logic: '', field: 'algae_name', value: '' }]); // 设置默认字段为 algae_name

// 逻辑选项
const logicOptions = [
    { label: 'And', value: 'AND' },
    { label: 'Or', value: 'OR' }
];

// 字段选项
const fieldOptions = [
    { label: 'Algae Name', value: 'algae_name' },
    { label: 'Algae Taxonomy', value: 'algae_taxonomy' },
    { label: 'Algae Environment', value: 'algae_environment' },
    { label: 'Chemical Name', value: 'chemical_name' },
    { label: 'Chemical SMILES', value: 'chemical_smiles' },
    { label: 'Chemical CAS', value: 'chemical_cas' },
    { label: 'Chemical Source', value: 'chemical_source' },
    { label: 'Chemical Origin', value: 'chemical_origin' },
    { label: 'Chemical Classification', value: 'chemical_label' },
    { label: 'Endpoint', value: 'endpoint' },
    { label: 'Response', value: 'response' },
    { label: 'Author', value: 'author' },
    { label: 'Journal Name', value: 'journal_name' },
    { label: 'Publication Date', value: 'publication_date' }
];

// 切换高级搜索显示
const toggleAdvancedSearch = () => {
    advancedSearchVisible.value = !advancedSearchVisible.value;
};

// 添加和删除高级搜索行
const addQuery = () => {
    advancedQueries.value.push({ logic: 'AND', field: 'algae_name', value: '' }); // 默认字段为 algae_name
};
const removeQuery = (index) => {
    advancedQueries.value.splice(index, 1);
};

// 动态生成占位符
const getDynamicLabel = (field) => {
    switch (field) {
        case 'algae_name':
            return 'Example: Akashiwo sanguinea';
        case 'algae_taxonomy':
            return 'Example: Dinoflagellata';
        case 'algae_environment':
            return 'Example: Marine';
        case 'chemical_name':
            return 'Example: Sphinganine';
        case 'chemical_smiles':
            return 'Example: CCCCCCCCCCCCCCC[C@H]([C@H](CO)N)O';
        case 'chemical_cas':
            return 'Example: 3025-96-5';
        case 'chemical_origin':
            return 'Example: Plant';
        case 'chemical_source':
            return 'Example: Elodea nuttallii';
        case 'chemical_label':
            return 'Example: Alkaloid';
        case 'endpoint':
            return 'Example: EC50';
        case 'response':
            return 'Example: cell density';
        case 'author':
            return 'Example: Jing, Hu';
        case 'journal_name':
            return 'Example: Science of The Total Environment';
        case 'publication_date':
            return 'Example: 2022';
        default:
            return 'Search Query';
    }
};
const router = useRouter(); // 获取 Vue Router 实例
// const searchGeneral = () => {
//     if (!generalSearch.value.trim()) {
//         alert('Please enter a search term.');
//         return;
//     }

//     // 使用 router.push 来导航并传递 params 参数，而不是查询参数
//     router.push(
//         {
//             name: 'search-results',
//             query: {
//                 query: generalSearch.value.trim(), // 搜索关键词作为路由参数
//                 searchType: 'general' // 搜索类型作为路由参数
//             }
//         },
//         '/search/results'
//     );
// };

const store = useStore(); // 获取 Vuex store 实例

const searchGeneral = () => {
    if (!generalSearch.value.trim()) {
        alert('Please enter a search term.');
        return;
    }

    // 使用 store.dispatch 调用 Vuex 的 action
    store.dispatch('setSearchQuery', generalSearch.value.trim()); // 存储查询参数
    store.dispatch('setSearchType', 'general'); // 存储搜索类型

    // 使用 Vue Router 导航到结果页面
    router.push({ name: 'search-results' });
};

// 高级搜索
// const searchAdvanced = () => {
//     const validQueries = advancedQueries.value.filter((query) => query.field && query.value);
//     if (!validQueries.length) {
//         alert('Please provide at least one advanced search query.');
//         return;
//     }

//     sessionStorage.setItem('searchAdvancedQueries', JSON.stringify(validQueries));
//     sessionStorage.setItem('searchType', 'advanced'); // 指定搜索类型
//     window.open('/#/search/results', '_blank'); // 打开结果页面
// };

const searchAdvanced = () => {
    const validQueries = advancedQueries.value.filter((query) => query.field && query.value);
    if (!validQueries.length) {
        alert('Please provide at least one advanced search query.');
        return;
    }

    // 使用 Vuex 存储高级查询条件
    store.dispatch('setSearchAdvancedQueries', validQueries);
    store.dispatch('setSearchType', 'advanced'); // 存储搜索类型为 'advanced'

    // 使用 Vue Router 导航到结果页面
    router.push({ name: 'search-results' });
};
</script>

<template>
    <div class="max-w-7xl mx-auto p-6 bg-white rounded-lg shadow-md space-y-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Search Algicidal Records by Keyword</h1>

        <!-- User Instructions -->
        <div class="p-4 bg-gray-100 rounded-lg">
            <h2 class="text-xl font-semibold text-gray-800 mb-2">How to Use the Search Form</h2>
            <p class="text-gray-700 mb-2">You can perform a general search or an advanced search to find algicidal records.</p>
            <ul class="list-disc list-inside text-gray-700 mb-2">
                <li><strong>General Search:</strong> Enter a keyword in the search box and click the "Search" button. You can search by algae name, chemical name, chemical CAS, chemical SMILES, endpoint, or response.</li>
                <li>
                    <strong>Advanced Search:</strong> Click the "Advanced Search" button to expand the advanced search options. You can add multiple search criteria by clicking "Add Row". Select the logic (AND/OR), field, and enter the value for each
                    criterion. Click the "Search" button to perform the search.
                </li>
            </ul>
            <p class="text-gray-700">Note: At least one search criterion is required for both general and advanced searches.</p>
        </div>

        <!-- General Search -->
        <div class="mb-6 flex items-center space-x-4">
            <div class="flex-1">
                <FloatLabel>
                    <InputText v-model="generalSearch" id="general-search" class="w-full" />
                    <label for="general-search">Keyword Search by: algae name, chemical name, chemical cas, chemical smiles, endpoint, response</label>
                </FloatLabel>
            </div>
            <Button type="button" label="Search" icon="pi pi-search" :loading="loading" @click="searchGeneral" />
        </div>

        <!-- Advanced Search Toggle -->
        <div class="flex justify-center mb-4">
            <Button label="Advanced Search" :icon="advancedSearchVisible ? 'pi pi-angle-double-up' : 'pi pi-angle-double-down'" class="p-button-link text-green-500" @click="toggleAdvancedSearch" />
        </div>

        <!-- Advanced Search Section -->
        <div v-if="advancedSearchVisible" class="pt-4 space-y-6">
            <div v-for="(query, index) in advancedQueries" :key="index" class="flex items-center space-x-4">
                <!-- Logic Selector -->
                <div v-if="index !== 0" class="w-1/6">
                    <Select v-model="query.logic" :options="logicOptions" optionLabel="label" optionValue="value" placeholder="Select Logic" class="w-full" />
                </div>

                <!-- Field Selector -->
                <div class="w-1/4">
                    <Select v-model="query.field" :options="fieldOptions" optionLabel="label" optionValue="value" placeholder="Select Field" class="w-full" />
                </div>

                <!-- Value Input -->
                <div class="flex-1">
                    <FloatLabel>
                        <InputText v-model="query.value" id="advanced-input" class="w-full" />
                        <label for="advanced-input">{{ getDynamicLabel(query.field) }}</label>
                    </FloatLabel>
                </div>

                <!-- Remove Button -->
                <Button icon="pi pi-times" variant="text" raised rounded aria-label="Cancel" @click="removeQuery(index)" />
            </div>

            <!-- Add Row Button -->
            <div class="flex justify-end">
                <Button label="Add Row" icon="pi pi-plus" class="p-button-text text-green-500" @click="addQuery" />
            </div>

            <!-- Search Button -->
            <div class="flex justify-end mt-6 space-x-4">
                <Button label="Search" icon="pi pi-search" :loading="loading" @click="searchAdvanced" />
            </div>
        </div>
    </div>
</template>
