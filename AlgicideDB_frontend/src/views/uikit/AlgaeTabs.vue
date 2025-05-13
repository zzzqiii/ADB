<script setup>
import AlgaeGrid from '@/views/uikit/AlgaeGrid.vue';
import Table from '@/views/uikit/AlgaeTable.vue';
import axios from 'axios';
import { onMounted, ref } from 'vue';

// Variables for tabs and algae data
const tabs = ref([]);
const algaeSpeciesList = ref([]); // Updated to store AlgaeSpecies data

// Function to fetch AlgaeSpecies data
const fetchAlgaeSpeciesData = async () => {
    try {
        const response = await axios.get('/algaecide/algaespecies/');
        algaeSpeciesList.value = response.data;

        // Sort the AlgaeSpecies by name in alphabetical order
        algaeSpeciesList.value.sort((a, b) => a.name.localeCompare(b.name));

        // Extract unique phylum values for tab labels
        const uniqueTypes = [...new Set(algaeSpeciesList.value.map((species) => species.phylum))];

        // Create tabs with "All" as the first tab
        tabs.value = [
            { title: 'All', phylum: 'all', value: '0' },
            ...uniqueTypes.map((type, index) => ({
                title: type,
                phylum: type,
                value: `${index + 1}`
            }))
        ];
    } catch (error) {
        console.error('Error fetching AlgaeSpecies data:', error);
    }
};

// Fetch data when the component is mounted
onMounted(fetchAlgaeSpeciesData);
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
                        <!-- Load Table.vue when "All" tab is selected -->
                        <TabPanel v-for="tab in tabs" :key="tab.phylum" :value="tab.value">
                            <div v-if="tab.phylum === 'all'">
                                <Table />
                            </div>
                            <div v-else>
                                <AlgaeGrid :phylum="tab.phylum" />
                            </div>
                        </TabPanel>
                    </TabPanels>
                </Tabs>
            </div>
        </div>
    </div>
</template>
