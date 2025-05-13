<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const dt = ref(); // 引用 DataTable
const taskId = useRoute().params.taskId; // 获取任务 ID
const predictResults = ref([]);
const loading = ref(true);
const error = ref(null);

// 导出 CSV 的方法
const exportCSV = () => {
    if (predictResults.value.length > 0) {
        dt.value.exportCSV();
    } else {
        console.warn('No data available to export.');
    }
};

// 加载预测结果
onMounted(async () => {
    try {
        console.log('Loading results for task:', taskId);
        const response = await axios.get(`/algaecide/predict/result/${taskId}/`);
        predictResults.value = response.data.results;
    } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load results.';
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="card">
        <!-- <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Results for Task: {{ taskId }}</h1> -->

        <div v-if="loading" class="text-center text-gray-500">Loading results...</div>
        <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
        <div v-else>
            <p class="text-gray-600 mb-4">Results for Task: {{ taskId }}</p>
            <!-- DataTable 展示结果 -->
            <DataTable :value="predictResults" tableStyle="min-width: 10rem" stripedRows scrollable ref="dt" :paginator="true" :rows="10">
                <Column field="smiles" header="SMILES" sortable style="width: 5%" frozen class="font-bold" />
                <Column field="QEF" header="Algicide-likeness" sortable />
                <Column field="MolWt" header="MolWt" sortable />
                <Column field="NumHAcceptors" header="NumHAcceptors" sortable />
                <Column field="NumHDonors" header="NumHDonors" sortable />
                <Column field="MolLogP" header="MolLogP" sortable />
                <Column field="NumRotatableBonds" header="NumRotatableBonds" sortable />
                <Column field="NumAromaticRings" header="NumAromaticRings" sortable />
                <template #header>
                    <div class="text-end pb-4">
                        <Button icon="pi pi-external-link" label="Export" @click="exportCSV" />
                    </div>
                </template>
            </DataTable>
        </div>
    </div>
</template>
