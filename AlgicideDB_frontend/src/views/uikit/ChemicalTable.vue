<script setup>
import { FilterMatchMode } from '@primevue/core/api';
import axios from 'axios';
import { onBeforeMount, ref } from 'vue';

const chemicalList = ref([]); // To store chemical data
const filters1 = ref(null);
const loading1 = ref(false);
const options = ref({
    source: ['Plant', 'Microorganism', 'Animal', 'Synthetic', 'Commercial', 'Plant/Microorganism'] // Static source options
});

// Fetch chemical data
const fetchChemicalData = async () => {
    try {
        const response = await axios.get('/algaecide/chemical/');
        chemicalList.value = response.data;
        loading1.value = false; // Data loading complete
    } catch (error) {
        console.error('Error fetching chemical data:', error);
        loading1.value = false;
    }
};

// Initialize filters
const initFilters1 = () => {
    filters1.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS }, // Global search
        name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
        classification: { value: null, matchMode: FilterMatchMode.IN },
        source: { value: null, matchMode: FilterMatchMode.IN },
        casNumber: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
        isnp: { value: null, matchMode: FilterMatchMode.EQUALS },
        origin: { value: null, matchMode: FilterMatchMode.IN }
    };
};

// Clear filters
const clearFilter = () => {
    initFilters1();
};

// Fetch data and initialize filters
onBeforeMount(() => {
    loading1.value = true;
    fetchChemicalData(); // Fetch chemical data
    initFilters1(); // Initialize filters
});
</script>

<template>
    <div class="grid">
        <!-- Add global search feature -->
        <div class="flex justify-between mb-4">
            <IconField>
                <InputIcon>
                    <i class="pi pi-search" />
                </InputIcon>
                <InputText v-model="filters1.global.value" placeholder="Search" />
            </IconField>
            <Button type="button" icon="pi pi-filter-slash" label="Clear" outlined @click="clearFilter" />
        </div>

        <DataTable :value="chemicalList" :filters="filters1" filterDisplay="menu" :paginator="true" :rows="10" v-model:filters="filters1">
            <!-- Name field -->
            <Column field="name" header="Name" style="min-width: 12rem">
                <template #body="{ data }">
                    <router-link :to="{ path: `/algicides/${data.id}` }" class="text-cyan-600 hover:underline" target="_blank" rel="noopener noreferrer">
                        {{ data.name }}
                    </router-link>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" class="p-column-filter" placeholder="Search by name" />
                </template>
            </Column>

            <!-- Origin field with dropdown options -->
            <Column field="origin" header="Origin" style="min-width: 12rem" :showFilterMatchModes="false">
                <template #body="{ data }">
                    <span>{{ data.origin }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <MultiSelect v-model="filterModel.value" :options="options.source" placeholder="Select origin" />
                </template>
            </Column>

            <!-- Classification field -->
            <Column field="classification" header="Classification" style="min-width: 12rem">
                <template #body="{ data }">
                    <span>{{ data.label || data.classification }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" class="p-column-filter" placeholder="Search by classification" />
                </template>
            </Column>

            <!-- Source field with dropdown options -->
            <Column field="source" header="Source" style="min-width: 12rem" :showFilterMatchModes="false">
                <template #body="{ data }">
                    <span>{{ data.source }}</span>
                </template>
                <!-- <template #filter="{ filterModel }">
                    <MultiSelect v-model="filterModel.value" :options="options.source" placeholder="Select source" />
                </template> -->
            </Column>

            <!-- CAS Number field -->
            <Column field="casNumber" header="CAS Number" style="min-width: 10rem">
                <template #body="{ data }">
                    <span>{{ data.casNumber }}</span>
                </template>
                <!-- <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" class="p-column-filter" placeholder="Search by CAS number" />
                </template> -->
            </Column>

            <!-- IsNP field (True/False) -->
            <!-- <Column field="isnp" header="Is Natural Product" style="min-width: 10rem">
                <template #body="{ data }">
                    <span>{{ data.isnp ? 'Yes' : 'No' }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <Dropdown
                        v-model="filterModel.value"
                        :options="[
                            { label: 'Yes', value: true },
                            { label: 'No', value: false }
                        ]"
                        placeholder="Select"
                    />
                </template>
            </Column> -->

            <!-- PubChem link with icon -->
            <Column field="pubchem" header="PubChem Link" style="min-width: 8rem">
                <template #body="{ data }">
                    <span v-if="data.pubchem">
                        <a :href="data.pubchem" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline">
                            <i class="pi pi-external-link"></i>
                        </a>
                    </span>
                </template>
            </Column>
        </DataTable>
    </div>
</template>
