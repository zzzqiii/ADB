<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useStore } from 'vuex'; // 引入 Vuex
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrfToken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
axios.defaults.withCredentials = true; // 确保跨域请求附带 Cookie

const store = useStore();

// 获取 Vuex 中存储的查询参数
const query = store.getters.getSearchQuery;
const searchType = store.getters.getSearchType;
const advancedQueries = store.getters.getSearchAdvancedQueries;

const searchResults = ref([]);
const loading = ref(false);

const dt = ref();
// 导出 CSV 的方法
const exportCSV = () => {
    if (searchResults.value.length > 0) {
        dt.value.exportCSV();
    } else {
        console.warn('No data available to export.');
    }
};

// 获取搜索结果
const fetchSearchResults = async () => {
    loading.value = true;

    try {
        const endpoint = searchType === 'general' ? '/algaecide/search/general/' : '/algaecide/search/advanced/';

        const payload = searchType === 'general' ? { generalSearch: query } : { advancedQueries };
        console.log('Payload:', payload);
        console.log('Endpoint:', endpoint);

        const response = await axios.post(endpoint, payload);

        // 更新搜索结果
        searchResults.value = response.data || [];
    } catch (error) {
        console.error('Error fetching search results:', error);
        alert('An error occurred while fetching search results.');
    } finally {
        loading.value = false;
    }
};

// 初次加载
onMounted(() => {
    fetchSearchResults();
});
</script>

<template>
    <div class="card shadow-md">
        <div class="card-header flex justify-between items-center">
            <h5 class="card-title text-lg text-primary font-bold">Search Results</h5>
            <!-- <Tag v-if="searchType === 'general'" severity="info"> General Search: "{{ query }}" </Tag> -->
            <!-- <Tag v-else severity="info"> Advanced Search: "{{ advancedQueries.length ? advancedQueries.join(', ') : 'No conditions specified' }}" </Tag> -->
        </div>

        <div v-if="loading" class="text-center py-6 text-lg text-gray-500">Loading search results...</div>

        <div v-else>
            <p v-if="searchResults.length > 0" class="text-gray-600 mb-4">
                Found <strong>{{ searchResults.length }}</strong> records matching your search.
            </p>
            <p v-else class="text-gray-500 mb-4">No records found for the specified query.</p>

            <DataTable v-if="searchResults.length > 0" :value="searchResults" :paginator="true" :rows="10" responsiveLayout="scroll" class="p-datatable-gridlines shadow-md rounded-md text-sm" ref="dt">
                <!-- <Column field="algae_strain.species_name" header="Target" /> -->
                <template #header>
                    <div class="text-end pb-4">
                        <Button icon="pi pi-external-link" label="Export" @click="exportCSV" />
                    </div>
                    <!-- <div class="text-end pb-4" style="position: absolute; top: 10px; right: 10px">
                        <Button icon="pi pi-external-link" label="Export" @click="exportCSV" />
                    </div> -->
                </template>
                <Column field="algae_strain.species_name" header="Target">
                    <template #body="{ data }">
                        <span>
                            <router-link :to="{ path: `/algae/${data.algae_strain.species_id}` }" class="text-cyan-600 hover:underline">
                                <em>{{ data.algae_strain.species_name }}</em>
                            </router-link>
                            <p v-if="data.algae_strain.strain" class="text-sm text-gray-500">{{ data.algae_strain.strain }}</p>
                        </span>
                    </template>
                </Column>
                <!-- <Column field="chemical.name" header="Chemical" /> -->
                <Column field="chemical.name" header="Chemical">
                    <template #body="{ data }">
                        <router-link :to="{ path: `/algicides/${data.chemical.id}` }" class="text-cyan-600 hover:underline">
                            {{ data.chemical.name }}
                        </router-link>
                    </template>
                </Column>
                <Column field="measurement" header="Measurement" />
                <Column field="effect" header="Effect">
                    <template #body="{ data }"> {{ data.effect }} {{ data.unit }} </template>
                </Column>
                <Column field="initialDensity" header="Initial Density" />
                <Column field="time" header="Time" />
                <Column field="response_endpoint" header="Response" />
            </DataTable>
        </div>
    </div>
</template>
