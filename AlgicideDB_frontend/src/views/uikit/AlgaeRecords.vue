<script setup>
import axios from 'axios';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
// const speciesName = route.params.name;
const algaeId = route.params.id; // Get the id parameter from the route

const speciesData = ref(null);
const records = ref([]);
const loading = ref(true);

const columns = ref([
    // { field: 'chemical.name', header: 'Chemical' },
    // { field: 'algae_strain', header: 'Target' },
    // { field: 'measurement', header: 'Measurement' },
    // { field: 'effect', header: 'Effect' },
    { field: 'initialDensity', header: 'Initial Density' },
    { field: 'time', header: 'Time' },
    { field: 'response_endpoint', header: 'Response' }
]);
const selectedColumns = ref(columns.value);
const onToggle = (val) => {
    selectedColumns.value = columns.value.filter((col) => val.includes(col));
};

// Fetch AlgaeSpecies details and records
const fetchAlgaeData = async () => {
    try {
        // const speciesResponse = await axios.get(`http://127.0.0.1:8000/algaecide/algaespecies/?name=${speciesName}`);
        // if (speciesResponse.data.length > 0) {
        //     speciesData.value = speciesResponse.data[0];
        // }

        const speciesResponse = await axios.get(`/algaecide/algaespecies/${algaeId}/`);
        speciesData.value = speciesResponse.data;

        const recordsResponse = await axios.get(`/algaecide/record/?algae_strain__species__id=${algaeId}`);
        records.value = recordsResponse.data;

        loading.value = false;
    } catch (error) {
        console.error('Error fetching data:', error);
        loading.value = false;
    }
};

onMounted(fetchAlgaeData);
</script>

<template>
    <div class="container">
        <div v-if="loading" class="loading">Loading species details...</div>

        <div v-else>
            <!-- Top section with name, classification, description, and image -->
            <div class="top-section">
                <div class="left-content">
                    <h1>
                        <em>{{ speciesData?.name }}</em>
                    </h1>
                    <p class="classification"><strong>Classification:</strong> {{ speciesData?.phylum }} (Phylum) > {{ speciesData?.class_name }} (Class) > {{ speciesData?.order }} (Order) > {{ speciesData?.family }} (Family)</p>
                    <hr class="divider" />
                    <p class="description"><strong>Description:</strong> {{ speciesData?.description }}</p>
                    <small class="source"> <a :href="speciesData?.description_source" target="_blank" rel="noopener noreferrer">Information Source</a> </small>
                </div>
                <div class="relative right-image inline-block">
                    <!-- Image -->
                    <img v-if="speciesData?.image" :src="speciesData.image" alt="Algae image" class="rounded-md shadow-md" />

                    <!-- i Icon for copyright (inside the image, bottom-left) -->
                    <div v-if="speciesData?.image_copyright" class="absolute bottom-8 left-2 bg-white bg-opacity-80 w-5 h-5 rounded-full shadow-sm flex items-center justify-center">
                        <i class="pi pi-info-circle text-gray-600 text-lg cursor-pointer" v-tooltip="speciesData.image_copyright"></i>
                    </div>

                    <!-- Image Source -->
                    <small class="source">
                        <a :href="speciesData?.image_source" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline">Image Source</a>
                    </small>
                </div>
            </div>

            <!-- Algicide Records Table -->
            <div class="records">
                <h3 class="record-title">
                    {{ records.length }} algicide records for <em>{{ speciesData?.name }}</em>
                </h3>
                <DataTable :value="records" responsiveLayout="scroll" paginator :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]" rowGroupMode="rowspan" groupRowsBy="chemical.name" sortMode="single" sortField="chemical.name" :sortOrder="1">
                    <template #header>
                        <div style="text-align: left">
                            <MultiSelect :modelValue="selectedColumns" :options="columns" optionLabel="header" @update:modelValue="onToggle" display="chip" placeholder="Select Columns" />
                        </div>
                    </template>
                    <Column field="chemical.name" header="Chemical">
                        <template #body="{ data }">
                            <router-link :to="{ path: `/algicides/${data.chemical.id}` }" class="text-cyan-600 hover:underline">
                                {{ data.chemical.name }}
                            </router-link>
                        </template>
                    </Column>
                    <Column field="algae_strain" header="Strain">
                        <template #body="{ data }">
                            <span>
                                <!-- <em>{{ data.algae_strain.species_name }}</em> -->
                                <span v-if="data.algae_strain.strain"
                                    ><p></p>
                                    {{ data.algae_strain.strain }}</span
                                >
                            </span>
                        </template>
                    </Column>
                    <Column field="measurement" header="Measurement" />
                    <Column header="Effect">
                        <template #body="{ data }"> {{ data.effect }} {{ data.unit }} </template>
                    </Column>

                    <Column v-for="(col, index) of selectedColumns" :field="col.field" :header="col.header" :key="col.field + '_' + index"></Column>

                    <Column header="Test Conditions">
                        <template #body="{ data }">
                            <i
                                class="pi pi-info-circle"
                                v-tooltip="`Cultivation System: ${data.cultivationSystem || 'N/A'}\nIrradiance: ${data.irradiance || 'N/A'}\nTemperature: ${data.temperature || 'N/A'}\nCulture Medium: ${data.cultureMedium || 'N/A'}`"
                                style="cursor: pointer; color: #007ad9"
                            ></i>
                        </template>
                    </Column>

                    <Column header="Mechanism">
                        <template #body="{ data }">
                            <i v-if="data.mechanism" class="pi pi-question-circle" v-tooltip="`Mechanism: ${data.mechanism}`" style="cursor: pointer; color: #007ad9"></i>
                        </template>
                    </Column>

                    <Column header="Reference">
                        <template #body="{ data }">
                            <a :href="data.reference.url" target="_blank" style="text-decoration: none">
                                <i class="pi pi-external-link"></i>
                            </a>
                            <!-- {{ data.reference.doi }} -->
                        </template>
                    </Column>
                </DataTable>
                <div v-if="records.length === 0">No records found for this species.</div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.p-tooltip .p-tooltip-text {
    max-width: 200px;
    white-space: pre-wrap;
}
.container {
    padding: 50px;
    background-color: #ffffff;
    font-family: 'Roboto', sans-serif;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

.loading {
    text-align: center;
    font-size: 1.2rem;
    color: #757575;
}

.top-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
}

.left-content {
    flex: 3;
    padding-right: 20px;
}

.left-content h1 {
    font-size: 1.8rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
}

.classification {
    font-size: 1rem;
    color: #555;
    margin-bottom: 15px;
}

.divider {
    margin: 15px 0;
    border-top: 1px solid #ddd;
}

.description {
    font-size: 1rem;
    color: #555;
    line-height: 1.6;
    margin-bottom: 5px;
}

.right-image {
    flex: 1;
    max-width: 250px;
    text-align: center;
}

.right-image img {
    width: 100%;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.records {
    margin-top: 30px;
}

.source {
    font-size: 0.9rem;
    color: #888;
    display: block;
    margin-top: 5px;
    text-align: left;
}

.source a {
    color: #1a0dab;
    text-decoration: underline;
}

.record-title {
    margin-bottom: 20px;
    color: #333;
}
</style>
