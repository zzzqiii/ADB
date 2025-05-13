<script setup>
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';

// Get props (phylum) passed to this component
const props = defineProps({
    phylum: String
});

const algaeList = ref([]); // Store all algae data
const filteredAlgae = ref([]); // Store filtered algae data

// Filter algae data based on the provided phylum prop
const filterAlgae = () => {
    if (props.phylum) {
        filteredAlgae.value = algaeList.value.filter((algae) => algae.phylum === props.phylum);
    }
};

// Fetch algae data from the backend and remove duplicates based on the algae name
const fetchAlgaeData = async () => {
    try {
        // const response = await axios.get('http://127.0.0.1:8000/algaecide/algae/');
        // const allAlgae = response.data;

        // // Use Map to remove duplicates based on algae name
        // const uniqueAlgaeMap = new Map();
        // allAlgae.forEach((algae) => {
        //     if (!uniqueAlgaeMap.has(algae.name)) {
        //         uniqueAlgaeMap.set(algae.name, algae);
        //     }
        // });

        // // Convert the map back to an array
        // algaeList.value = Array.from(uniqueAlgaeMap.values());

        const response = await axios.get('/algaecide/algaespecies/');
        algaeList.value = response.data;
        algaeList.value.sort((a, b) => a.name.localeCompare(b.name));

        // Filter the data based on phylum after removing duplicates
        filterAlgae();
    } catch (error) {
        console.error('Error fetching algae data:', error);
    }
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
// Watch for changes to the phylum prop and filter algae data accordingly
watch(() => props.phylum, filterAlgae);

// Fetch data when the component is mounted
onMounted(fetchAlgaeData);
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <DataView :value="filteredAlgae" layout="grid" :paginator="false" :rows="3">
                <template #grid="slotProps">
                    <div v-if="slotProps.items.length > 0" class="grid grid-cols-12 gap-4">
                        <div v-for="(algae, index) in slotProps.items" :key="index" class="col-span-12 sm:col-span-6 md:col-span-4 xl:col-span-3 p-2">
                            <Card class="h-full rounded-lg shadow-md overflow-hidden">
                                <template #header>
                                    <!-- 固定图片区域高度 -->
                                    <div class="relative w-full h-48 md:h-56 lg:h-60 overflow-hidden">
                                        <router-link :to="{ path: `/algae/${algae.id}` }" target="_blank" rel="noopener noreferrer">
                                            <img v-if="algae.image" :src="algae.image" :alt="algae.name" class="w-full h-full object-cover" />
                                        </router-link>
                                        <!-- <a href="javascript:void(0)" @click="navigateToRecords(algae.name)" class="block">
                                            <img v-if="algae.image" :src="algae.image" :alt="algae.name" class="w-full h-full object-cover" />
                                        </a> -->
                                        <!-- Tags -->
                                        <span v-if="algae.risk">
                                            <Tag :value="algae.risk" :severity="getToxicitySeverity(algae.risk)" class="absolute dark:!bg-surface-900" style="right: 4px; top: 4px" />
                                        </span>
                                        <span v-if="algae.environment">
                                            <Tag :value="algae.environment" :severity="getSeverity(algae.environment)" class="absolute dark:!bg-surface-900" style="left: 4px; top: 4px" />
                                        </span>
                                    </div>
                                </template>
                                <template #title>
                                    <div class="pt-1 text-center p-1">
                                        <div class="text-lg font-medium">
                                            <router-link :to="{ path: `/algae/${algae.id}` }" class="text-primary" target="_blank" rel="noopener noreferrer">
                                                <em>{{ algae.name }}</em>
                                            </router-link>
                                        </div>
                                    </div>
                                </template>
                            </Card>
                        </div>
                    </div>
                    <p v-else>No algae found for the selected phylum.</p>
                </template>
            </DataView>
        </div>
    </div>
</template>
