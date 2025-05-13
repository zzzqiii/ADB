<script setup>
import { FilterMatchMode } from '@primevue/core/api';
import axios from 'axios';
import Tag from 'primevue/tag'; // Import Tag component
import { onBeforeMount, ref } from 'vue';

const algaeList = ref([]); // To store algae data
const filters1 = ref(null);
const loading1 = ref(false);
const options = ref({
    phylum: [],
    class_name: [],
    order: [],
    family: [],
    environment: [], //['marine', 'freshwater'], // Static environment options
    risk: [] //['Toxic', 'Harmful', 'Toxic/Harmful'] // Static toxicity type options
});

// Fetch algae data and ensure uniqueness
const fetchAlgaeData = async () => {
    try {
        const response = await axios.get('/algaecide/algaespecies/');
        // const allAlgae = response.data;

        // // Ensure only unique algae are displayed by name
        // const uniqueAlgaeMap = new Map();
        // allAlgae.forEach((algae) => {
        //     if (!uniqueAlgaeMap.has(algae.name)) {
        //         uniqueAlgaeMap.set(algae.name, algae); // Use name as unique key
        //     }
        // });

        // Convert unique algae into array and sort by name alphabetically
        // algaeList.value = Array.from(uniqueAlgaeMap.values()).sort((a, b) => a.name.localeCompare(b.name));

        algaeList.value = response.data;
        // Sort algaeList by name alphabetically
        algaeList.value.sort((a, b) => a.name.localeCompare(b.name));

        loading1.value = false; // Data loaded
        generateOptions(); // Generate dynamic options
    } catch (error) {
        console.error('Error fetching algae data:', error);
        loading1.value = false;
    }
};

// Generate unique values for each filterable field
const generateOptions = () => {
    const fields = ['phylum', 'class_name', 'order', 'family', 'environment', 'risk']; // Fields to generate options for
    fields.forEach((field) => {
        const uniqueValues = [...new Set(algaeList.value.map((algae) => algae[field]).filter((value) => value))];
        options.value[field] = uniqueValues; // Dynamically generate options
    });
};

// Initialize filters
const initFilters1 = () => {
    filters1.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS }, // Global search
        name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
        phylum: { value: null, matchMode: FilterMatchMode.IN },
        class_name: { value: null, matchMode: FilterMatchMode.IN },
        order: { value: null, matchMode: FilterMatchMode.IN },
        family: { value: null, matchMode: FilterMatchMode.IN },
        environment: { value: null, matchMode: FilterMatchMode.IN },
        risk: { value: null, matchMode: FilterMatchMode.IN }
    };
};

// Clear filters
const clearFilter = () => {
    initFilters1();
};

// Return color based on environment
const getSeverity = (environment) => {
    switch (environment) {
        case 'marine':
            return 'info';
        case 'freshwater':
            return 'success';
        case 'brackish':
            return 'warn';
        case 'freshwater/marine':
            return 'secondary';
        default:
            return null;
    }
};

// Return color based on toxicity type
const getToxicitySeverity = (toxicityType) => {
    switch (toxicityType) {
        case 'Toxic':
            return 'danger';
        case 'Harmful':
            return 'warn';
        case 'Fouling':
            return 'success';
        default:
            return null;
    }
};

// Debug: log filter changes
const onFilterChange = () => {
    console.log('Filter applied:', filters1.value);
};

// Load data before mounting the component
onBeforeMount(() => {
    loading1.value = true;
    fetchAlgaeData(); // Fetch data
    initFilters1(); // Initialize filters
});
</script>

<template>
    <div class="grid">
        <div class="flex justify-between mb-4">
            <IconField>
                <InputIcon>
                    <i class="pi pi-search" />
                </InputIcon>
                <InputText v-model="filters1.global.value" placeholder="Search" />
            </IconField>
            <Button type="button" icon="pi pi-filter-slash" label="Clear" outlined @click="clearFilter" />
        </div>

        <DataTable :value="algaeList" :filters="filters1" filterDisplay="menu" :paginator="true" :rows="10" v-model:filters="filters1" @filter="onFilterChange" sortMode="single" sortField="name" :sortOrder="1">
            <!-- Name column with click navigation -->
            <!-- Name column with click navigation -->
            <!-- Name column with click navigation and filter icon positioned tightly -->
            <Column field="name" header="Name" style="min-width: 12rem">
                <template #body="{ data }">
                    <!-- <a href="javascript:void(0)" @click="navigateToRecords(data.name)" style="font-style: italic; text-decoration: underline; cursor: pointer; color: #555555; font-weight: bold">
                        {{ data.name }}
                    </a> -->

                    <router-link :to="{ path: `/algae/${data.id}` }" class="text-cyan-600 hover:underline" target="_blank" rel="noopener noreferrer">
                        <em>{{ data.name }}</em>
                    </router-link>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" class="p-column-filter" placeholder="Search by name" />
                </template>
            </Column>

            <!-- Phylum filter -->
            <Column field="phylum" header="Phylum" :showFilterMatchModes="false">
                <template #body="{ data }">
                    <span>{{ data.phylum }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <MultiSelect v-model="filterModel.value" :options="options.phylum" placeholder="Any" />
                </template>
            </Column>

            <!-- Class filter -->
            <Column field="class_name" header="Class" :showFilterMatchModes="false">
                <template #body="{ data }">
                    <span>{{ data.class_name }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <MultiSelect v-model="filterModel.value" :options="options.class_name" placeholder="Any" />
                </template>
            </Column>

            <!-- Order filter -->
            <Column field="order" header="Order" :showFilterMatchModes="false">
                <template #body="{ data }">
                    <span>{{ data.order }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <MultiSelect v-model="filterModel.value" :options="options.order" placeholder="Any" />
                </template>
            </Column>

            <!-- Family filter -->
            <Column field="family" header="Family" :showFilterMatchModes="false">
                <template #body="{ data }">
                    <span>{{ data.family }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <MultiSelect v-model="filterModel.value" :options="options.family" placeholder="Any" />
                </template>
            </Column>

            <!-- Environment filter with severity -->
            <Column field="environment" header="Environment" :showFilterMatchModes="false">
                <template #body="{ data }">
                    <span v-if="data.environment">
                        <Tag :value="data.environment" :severity="getSeverity(data.environment)" />
                    </span>
                </template>
                <template #filter="{ filterModel }">
                    <MultiSelect v-model="filterModel.value" :options="options.environment" placeholder="Any" />
                </template>
            </Column>

            <!-- Toxicity type filter with severity -->
            <Column field="risk" header="Risk" :showFilterMatchModes="false">
                <template #body="{ data }">
                    <span v-if="data.risk">
                        <Tag :value="data.risk" :severity="getToxicitySeverity(data.risk)" />
                    </span>
                </template>
                <template #filter="{ filterModel }">
                    <MultiSelect v-model="filterModel.value" :options="options.risk" placeholder="Any" />
                </template>
            </Column>
        </DataTable>
    </div>
</template>
