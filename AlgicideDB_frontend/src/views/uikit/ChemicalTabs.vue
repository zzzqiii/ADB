<script setup>
import ChemicalGrid from '@/views/uikit/ChemicalGrid.vue'; // Import the ChemicalGrid component
import ChemicalTable from '@/views/uikit/ChemicalTable.vue';
import axios from 'axios';
import { onMounted, ref } from 'vue';

const tabs = ref([
    { title: 'All', origin: 'all', value: '0' },
    { title: 'Plant Source', origin: 'Plant', value: '1' },
    { title: 'Microbe Source', origin: 'Microorganism', value: '2' },
    { title: 'Sythetic', origin: 'Synthetic', value: '3' },
    { title: 'Commercial', origin: 'Commercial', value: '4' }
]);

// 在 'All' 标签下显示所有化合物
const chemicalList = ref([]); // Store the complete list of chemicals

const fetchChemicalData = async () => {
    try {
        const response = await axios.get('/algaecide/chemical/');
        chemicalList.value = response.data.sort((a, b) => a.name.localeCompare(b.name)); // Sort by name
    } catch (error) {
        console.error('Error fetching chemical data:', error);
    }
};

onMounted(fetchChemicalData);
</script>

<template>
    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card card-w-title">
                <Tabs value="0" scrollable>
                    <TabList>
                        <Tab v-for="tab in tabs" :key="tab.title" :value="tab.value">
                            {{ tab.title }}
                        </Tab>
                    </TabList>
                    <TabPanels>
                        <!-- 加载化合物的网格或者表格 -->
                        <TabPanel v-for="tab in tabs" :key="tab.origin" :value="tab.value">
                            <!-- 当 Tab 为 "All" 时，加载 ChemicalTable.vue -->
                            <div v-if="tab.origin === 'all'">
                                <ChemicalTable :chemicals="chemicalList" />
                            </div>
                            <!-- 其他 tab 显示网格化合物数据 -->
                            <div v-else>
                                <ChemicalGrid :origin="tab.origin" />
                            </div>
                        </TabPanel>
                    </TabPanels>
                </Tabs>
            </div>
        </div>
    </div>
</template>
