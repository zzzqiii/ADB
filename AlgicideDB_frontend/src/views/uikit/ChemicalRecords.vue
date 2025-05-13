<script setup>
import axios from 'axios';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import MultiSelect from 'primevue/multiselect';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const chemicalId = route.params.id; // Get the id parameter from the route

const chemicalData = ref(null);
const loading = ref(true);
const ghsIcons = ref([]);
const records = ref([]);

const columns = ref([
    { field: 'initialDensity', header: 'Initial Density' },
    { field: 'time', header: 'Time' },
    { field: 'response_endpoint', header: 'Response Endpoint' }
]);
const selectedColumns = ref(columns.value);

const onToggle = (val) => {
    selectedColumns.value = columns.value.filter((col) => val.includes(col));
};
// console.log(chemicalId);
// Fetch Chemical details
const fetchChemicalData = async () => {
    try {
        // Fetch basic chemical information using chemical ID
        const chemicalResponse = await axios.get(`/algaecide/chemical/${chemicalId}/`);
        chemicalData.value = chemicalResponse.data;

        // console.log(chemicalData.value);

        // const recordsResponse = await axios.get(`/algaecide/record/?chemical=${chemicalId}/`);
        // records.value = recordsResponse.data;

        // Fetch chemical records using chemical ID
        const recordsResponse = await axios.get(`/algaecide/record/?chemical__id=${chemicalId}`);
        // console.log(recordsResponse.data);
        records.value = recordsResponse.data;
        loading.value = false;

        const safetyResponse = await axios.get(`https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/${chemicalData.value.pubchem_cid}/JSON?heading=Safety%20and%20Hazards`);
        const safetySections = safetyResponse.data?.Record?.Section;
        const pictogramSection = safetySections?.find((section) => section.Section?.[0]?.Section?.[0]?.Information?.find((info) => info.Name === 'Pictogram(s)'));

        if (pictogramSection) {
            const pictogramInfo = pictogramSection.Section[0].Section[0].Information.find((info) => info.Name === 'Pictogram(s)');
            if (pictogramInfo?.Value?.StringWithMarkup) {
                ghsIcons.value = pictogramInfo.Value.StringWithMarkup[0].Markup.map((item) => ({
                    url: item.URL,
                    label: item.Extra
                }));
            }
        }
    } catch (error) {
        console.error('Error fetching chemical data:', error);
        loading.value = false;
    }
};

onMounted(fetchChemicalData);
</script>

<template>
    <div class="container">
        <!-- Loading Section -->
        <div v-if="loading" class="text-center text-gray-500 text-lg">Loading chemical details...</div>

        <!-- Content Section -->
        <div v-else>
            <!-- Chemical Information Section -->
            <div class="top-section">
                <div class="left-content">
                    <h1>
                        {{ chemicalData?.name }}
                    </h1>
                    <div class="mt-4 text-lg text-gray-700 leading-7 space-y-2">
                        <!-- <div v-if="chemicalData?.label || chemicalData?.classification">
                            <p>
                                <strong class="font-semibold">
                                    {{ chemicalData?.label ? 'Structural Classification: ' : 'Chemical Ingredients: ' }}
                                </strong>
                                <span>{{ chemicalData?.label || chemicalData?.classification || 'Unknown' }}</span>
                            </p>
                        </div> -->

                        <div v-if="(chemicalData?.label && !chemicalData.label.toLowerCase().includes('extract')) || chemicalData?.classification">
                            <p>
                                <strong class="font-semibold">
                                    {{ chemicalData?.label ? 'Structural Classification: ' : 'Chemical Ingredients: ' }}
                                </strong>
                                <span>{{ chemicalData?.label || chemicalData?.classification || 'Unknown' }}</span>  
                            </p>
                        </div>

                        <div v-if="chemicalData?.source">
                            <p>
                                <strong class="font-semibold">Source: </strong>
                                <em>{{ chemicalData?.source }}</em>
                            </p>
                        </div>
                        <div v-if="chemicalData?.cas_number">
                            <p>
                                <strong class="font-semibold">CAS Number: </strong>
                                <span>{{ chemicalData?.cas_number }}</span>
                            </p>
                        </div>
                        <div v-if="chemicalData?.pubchem">
                            <p>
                                <strong class="font-semibold">PubChem Link: </strong>
                                <a v-if="chemicalData?.pubchem" :href="chemicalData?.pubchem" target="_blank" class="text-blue-500 hover:underline"> View on PubChem </a>
                            </p>
                        </div>
                        <div v-if="chemicalData?.smiles">
                            <p>
                                <strong class="font-semibold">SMILES: </strong>
                                <span>{{ chemicalData?.smiles || 'N/A' }}</span>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="relative right-image inline-block">
                    <img v-if="chemicalData?.image" :src="chemicalData?.image" :alt="chemicalData?.name" class="w-64 h-64 object-contain" />
                    <!-- i Icon for copyright (inside the image, bottom-left) -->
                    <div v-if="chemicalData?.image_copyright" class="absolute bottom-8 left-2 bg-white bg-opacity-80 w-5 h-5 rounded-full shadow-sm flex items-center justify-center">
                        <i class="pi pi-info-circle text-gray-600 text-lg cursor-pointer" v-tooltip="chemicalData.image_copyright"></i>
                    </div>
                    <!-- <div v-if="chemicalData?.image_source" class="mt-4">
                        
                        <small class="source">
                            <a :href="chemicalData?.image_source" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline">Image Source</a>
                        </small>
                    </div> -->
                </div>
            </div>

            <!-- Chemical Safety Section -->
            <div v-if="ghsIcons.length && chemicalData?.pubchem_cid" class="p-4 bg-gray-100 rounded-md shadow-sm">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Chemical Safety</h3>
                <!-- GHS Icons -->
                <div v-if="ghsIcons.length" class="flex gap-4">
                    <div v-for="(icon, index) in ghsIcons" :key="index" class="text-center">
                        <img :src="icon.url" :alt="icon.label" class="w-16 h-16" />
                        <p class="text-sm text-gray-600 mt-2">{{ icon.label }}</p>
                    </div>
                </div>

                <!-- PubChem LCSS Link -->
                <div class="mt-4">
                    <a :href="`https://pubchem.ncbi.nlm.nih.gov/compound/${chemicalData.pubchem_cid}#datasheet=LCSS`" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline flex items-center gap-1">
                        Laboratory Chemical Safety Summary (LCSS) Datasheet
                        <i class="pi pi-external-link"></i>
                    </a>
                </div>
            </div>

            <!-- Records Table Section -->
            <div class="records">
                <h3 class="record-title">{{ records.length }} algicide records for {{ chemicalData?.name }}</h3>
                <DataTable
                    :value="records"
                    paginator
                    :rows="10"
                    :rowsPerPageOptions="[5, 10, 20]"
                    responsiveLayout="scroll"
                    rowGroupMode="rowspan"
                    groupRowsBy="algae_strain.species_name"
                    sortMode="single"
                    sortField="algae_strain.species_name"
                    :sortOrder="1"
                >
                    <template #header>
                        <div style="text-align: left">
                            <MultiSelect
                                :modelValue="selectedColumns"
                                :options="columns"
                                optionLabel="header"
                                @update:modelValue="onToggle"
                                display="chip"
                                placeholder="Select Columns"
                                sortMode="single"
                                sortField="algae_strain.species_name"
                                :sortOrder="1"
                            />
                        </div>
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
                    <Column field="measurement" header="Measurement" />
                    <Column header="Effect">
                        <template #body="{ data }"> {{ data.effect }} {{ data.unit }} </template>
                    </Column>
                    <Column v-for="(col, index) in selectedColumns" :field="col.field" :header="col.header" :key="col.field + '_' + index" />
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
                            <a :href="data.reference.url" target="_blank" class="text-blue-500 hover:underline">
                                <i class="pi pi-external-link"></i>
                            </a>
                        </template>
                    </Column>
                </DataTable>
                <div v-if="records.length === 0" class="text-center text-gray-500 mt-4">No records found for this chemical.</div>
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
    /* margin-bottom: 20px; */
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
