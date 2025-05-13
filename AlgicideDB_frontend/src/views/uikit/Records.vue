<script setup>
import { onMounted, ref } from 'vue';

const records = ref([]); // 存储表格数据
const loading = ref(true); // 加载状态

// 模拟从 API 或 sessionStorage 获取数据
onMounted(() => {
    setTimeout(() => {
        const storedRecords = JSON.parse(sessionStorage.getItem('searchResults') || '[]');
        if (storedRecords.length > 0) {
            records.value = storedRecords;
        } else {
            alert('No records found. Please start a new search.');
        }
        loading.value = false; // 停止加载状态
    }, 1000);
});
</script>

<template>
    <div class="container mx-auto p-6 bg-white rounded-lg shadow-md">
        <!-- 显示加载状态 -->
        <div v-if="loading" class="text-center py-6 text-lg text-gray-500">Loading records...</div>

        <!-- 显示表格 -->
        <div v-else>
            <h1 class="text-2xl font-bold text-gray-800 mb-6 text-center">Search Results</h1>

            <!-- 使用 PrimeVue 的 DataTable -->
            <DataTable :value="records" class="p-datatable-gridlines shadow-md rounded-md" responsiveLayout="scroll" :rows="10" :paginator="true">
                <!-- 化学品名称 -->
                <Column field="chemical.name" header="Chemical" />

                <!-- 藻类 -->
                <Column field="algae_strain" header="Algae">
                    <template #body="{ data }">
                        {{ data.algae_strain || 'N/A' }}
                    </template>
                </Column>

                <!-- 效应（包含单位） -->
                <Column header="Effect">
                    <template #body="{ data }"> {{ data.effect || 'N/A' }} {{ data.unit || '' }} </template>
                </Column>

                <!-- 测量值 -->
                <Column field="measurement" header="Measurement" />

                <!-- 初始密度 -->
                <Column field="initialDensity" header="Initial Density" />

                <!-- 时间 -->
                <Column field="time" header="Time" />

                <!-- 响应端点 -->
                <Column field="response_endpoint" header="Response Endpoint" />

                <!-- 其他测量值 -->
                <Column field="other_measurements" header="Other Measurements" />

                <!-- 参考文献 -->
                <Column header="Reference">
                    <template #body="{ data }">
                        <a v-if="data.reference?.url" :href="data.reference.url" target="_blank" class="text-blue-500 hover:underline"> Reference → </a>
                        <span v-else>N/A</span>
                    </template>
                </Column>
            </DataTable>

            <!-- 无数据提示 -->
            <div v-if="records.length === 0" class="text-gray-500 text-center mt-6">No records found for this query.</div>
        </div>
    </div>
</template>
