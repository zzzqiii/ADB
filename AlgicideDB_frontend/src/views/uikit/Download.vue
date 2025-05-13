<script setup>
import { ProductService } from '@/service/ProductService';
import { onMounted, ref } from 'vue';

const products = ref(null);
const picklistProducts = ref(null);
const orderlistProducts = ref(null);
const layout = ref('list');

const exampleFiles = [
    { name: 'Algicide Information', url: 'http://algicidedb.ocean-meta.com/algaecide/download/Algicide_Information.csv' },
    { name: 'Algae Information', url: 'http://algicidedb.ocean-meta.com/algaecide/download/Algae_Information.csv' },
    { name: 'Reference Information for Algicide', url: 'http://algicidedb.ocean-meta.com/algaecide/download/References_Information_Algicide.csv' },
    { name: 'Reference Information for Algae', url: 'http://algicidedb.ocean-meta.com/algaecide/download/Reference_information_RAG.csv' }
];
const dataviewValue = ref(
    exampleFiles.map((file) => ({
        name: file.name,
        url: file.url,
        description: 'Downloadable file'
    }))
);
const downloadFile = (url) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = url.split('/').pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};
onMounted(() => {
    ProductService.getProductsSmall().then((data) => {
        products.value = data.slice(0, 6);
        picklistProducts.value = [data, []];
        orderlistProducts.value = data;
    });
});
</script>

<template>
    <div class="max-w-7xl mx-auto p-6 bg-white rounded-lg shadow-md space-y-6">
        <div class="font-semibold text-xl">Datasets</div>
        <DataView :value="dataviewValue" :layout="layout">
            <template #list="slotProps">
                <div class="flex flex-col">
                    <div v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex flex-col sm:flex-row sm:items-center p-6 gap-4" :class="{ 'border-t border-surface': index !== 0 }">
                            <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6">
                                <div class="flex flex-row md:flex-col justify-between items-start gap-2">
                                    <div>
                                        <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">{{ item.category }}</span>
                                        <div class="text-lg font-medium mt-2">{{ item.name }}</div>
                                        <div class="text-sm text-surface-500 dark:text-surface-400">{{ item.description }}</div>
                                        <!-- <div v-if="slotProps.data" class="mb-3">{{ slotProps.data.description }}</div> -->
                                    </div>
                                </div>
                                <div class="flex flex-col md:items-end gap-8">
                                    <div class="flex flex-row-reverse md:flex-row gap-2">
                                        <!-- <Button icon="pi pi-heart" outlined></Button> -->
                                        <Button label="Download" @click="downloadFile(item.url)" class="flex-auto md:flex-initial whitespace-nowrap"></Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </DataView>
    </div>
</template>
