<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

// Store the counts from the backend
const stats = ref({
    algae_count: 0,
    record_count: 0,
    reference_count: 0,
    chemical_count: 0
});

// Fetch stats data from the backend
const fetchStats = async () => {
    try {
        const response = await axios.get('/algaecide/stats/');
        stats.value = response.data; // Store the stats in the reactive `stats`
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
};

// Fetch stats when the component is mounted
onMounted(fetchStats);

// Store for carousel items (images and metadata)
const carouselItems = ref([]);

// Carousel responsive options for different screen sizes
const carouselResponsiveOptions = ref([
    {
        breakpoint: '1024px',
        numVisible: 3,
        numScroll: 3
    },
    {
        breakpoint: '768px',
        numVisible: 2,
        numScroll: 2
    },
    {
        breakpoint: '1020px',
        numVisible: 1,
        numScroll: 1
    }
]);

// Dummy data for carousel images
const imageData = [
    { id: '1005', image: 'abstract.svg' },
    { id: '1003', image: 'figure2.svg' },
    { id: '1004', image: 'figure3.png' }

    // { id: '1005', image: 'Snipaste_2024-02-29_11-18-48.jpg' }
];

// Initialize and load carousel items on component mount
onMounted(() => {
    carouselItems.value = imageData;
});
</script>

<template>
    <!-- <div class="col-span-12 xl:col-span-6 flex items-center">
        <Carousel :value="carouselItems" :numVisible="1" :numScroll="1" circular :responsiveOptions="carouselResponsiveOptions" :autoplayInterval="4000" :showNavigators="false" :showIndicators="false">
            <template #item="carouselItem">
                <img :src="'images/homepage/' + carouselItem.data.image" :alt="carouselItem.data.id" class="img-responsive center-block img-circle img-fluid rounded shadow-lg" />
            </template>
        </Carousel>
    </div>
    

    </div> -->
    <div class="relative bg-[url('/images/homepage/4.jpg')] bg-cover h-96 bg-center flex items-center justify-center rounded-lg overflow-hidden">
        <div class="text-center bg-black bg-opacity-50 p-6 rounded-lg">
            <h1 class="text-4xl font-bold text-white mb-4">Welcome to AlgicideDB!</h1>
            <p class="text-white text-lg">Providing comprehensive algicide data to support global water resource safety.</p>
        </div>
    </div>
    <div class="mt-4"></div>
    <div class="card p-0 m-0">
        <div class="card-body p-0 m-0">
            <div class="grid grid-cols-12 gap-0 h-full">
                <div class="col-span-12 xl:col-span-8 flex items-center h-full">
                    <section class="p-8 m-0">
                        <div class="text-6xl text-primary font-bold mb-3">Algicide Database</div>
                        <p class="mt-0 mb-2 text-lg leading-relaxed text-gray-700">
                            Harmful algal blooms (HABs) are becoming more frequent and intense worldwide, posing serious threats to aquatic ecosystems, fisheries, and human health. While chemical algicides are widely used to control HABs due to their
                            fast-acting nature, concerns about their environmental toxicity and the lack of comprehensive data integration limit their broader use.
                        </p>
                        <p class="mt-0 mb-0 text-lg leading-relaxed text-gray-700">
                            To address these challenges, we developed AlgicideDB, a manually curated database containing 1,672 algicidal records from 204 publications, covering 542 algicides targeting 110 algal species. These records are primarily
                            based on laboratory studies, and actual field applications may require adjustments considering environmental factors like water temperature and flow conditions.
                        </p>
                        <p class="mt-0 mb-0 text-lg leading-relaxed text-gray-700">
                            In addition, we introduced an algicide-likeness scoring system to help identify compounds with potential antialgal properties. The platform also integrates a large language model powered by the HABs knowledge base,
                            assisting users with HAB-related queries.
                        </p>
                    </section>
                </div>
                <div class="col-span-12 xl:col-span-4">
                    <img src="/images/homepage/abstract1217.svg" alt="algae" class="w-full max-w-md h-auto rounded-lg object-contain mx-auto" />
                    <!-- <Carousel :value="carouselItems" :numVisible="1" :numScroll="1" circular :responsiveOptions="carouselResponsiveOptions" :autoplayInterval="7000" :showNavigators="false" :showIndicators="false">
                        <template #item="carouselItem">
                            <img :src="'images/homepage/iloveimg-resized/' + carouselItem.data.image" :alt="carouselItem.data.id" class="w-full max-w-md h-auto rounded-lg object-contain mx-auto" />
                        </template>
                    </Carousel> -->
                </div>
            </div>
        </div>
    </div>
    <div class="mt-4"></div>
    <div class="grid grid-cols-12 gap-8">
        <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Algae</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ stats.algae_count }}</div>
                    </div>
                    <div class="flex items-center justify-center bg-blue-100 dark:bg-blue-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-fw pi-eye text-blue-500 !text-xl"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Algicides</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ stats.chemical_count }}</div>
                    </div>
                    <div class="flex items-center justify-center bg-orange-100 dark:bg-orange-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-fw pi-slack text-orange-500 !text-xl"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Records</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ stats.record_count }}</div>
                    </div>
                    <div class="flex items-center justify-center bg-cyan-100 dark:bg-cyan-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-link text-cyan-500 !text-xl"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">References</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ stats.reference_count }}</div>
                    </div>
                    <div class="flex items-center justify-center bg-purple-100 dark:bg-purple-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-book text-purple-500 !text-xl"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- <div class="relative bg-[url('/images/homepage/blue-t-shirt.jpg')] bg-cover bg-center h-96 w-full flex items-center justify-center">
        <div>
            <div class="col-span-12 xl:col-span-6 flex items-center">
                <section>
                    <span class="block text-6xl font-bold mb-1"></span>
                    <div class="text-6xl text-primary font-bold mb-3">Algicide Database</div>
                    <p class="mt-0 mb-4 text-700 line-height-3">
                        Algae bloom represent a growing threat to global water security. With fast proliferation, they raise great concern due to potential health and socioeconomic concerns. Algaecides are commonly employed as a mitigative measure to
                        suppress and manage algae bloom. AlgaecideDB is a comprehensive Knowledgebase providing algaecide data including the toxicity data.
                    </p>
                </section>

                <div class="col-span-12 xl:col-span-6">
                    <Carousel :value="carouselItems" :numVisible="1" :numScroll="1" circular :responsiveOptions="carouselResponsiveOptions" :autoplayInterval="4000" :showNavigators="false" :showIndicators="false">
                        <template #item="carouselItem">
                            <img :src="'images/homepage/iloveimg-resized/' + carouselItem.data.image" :alt="carouselItem.data.id" class="img-responsive center-block img-circle" />
                        </template>
                    </Carousel>
                </div>
            </div>
        </div>
    </div> -->

    <!-- 背景图片容器 -->
    <!-- 半透明遮罩层（可选） -->
    <!-- <div class="absolute inset-0 bg-black bg-opacity-10"></div> -->

    <!-- 内容区域 -->

    <!-- <div class="card">
        <div>
            <div class="col-span-12 xl:col-span-6 flex items-center">
                <section>
                    <span class="block text-6xl font-bold mb-1"></span>
                    <div class="text-6xl text-primary font-bold mb-3">Algicide Database</div>
                    <p class="mt-0 mb-4 text-700 line-height-3">
                        Algae bloom represent a growing threat to global water security. With fast proliferation, they raise great concern due to potential health and socioeconomic concerns. Algaecides are commonly employed as a mitigative measure to
                        suppress and manage algae bloom. AlgaecideDB is a comprehensive Knowledgebase providing algaecide data including the toxicity data.
                    </p>
                </section>

                <div class="col-span-12 xl:col-span-6">
                    <Carousel :value="carouselItems" :numVisible="1" :numScroll="1" circular :responsiveOptions="carouselResponsiveOptions" :autoplayInterval="4000" :showNavigators="false" :showIndicators="false">
                        <template #item="carouselItem">
                            <img :src="'images/homepage/iloveimg-resized/' + carouselItem.data.image" :alt="carouselItem.data.id" class="img-responsive center-block img-circle" />
                        </template>
                    </Carousel>
                </div>
            </div>
        </div>
    </div> -->
</template>

<style scoped>
.hover-effect {
    width: 300px; /* 设置图片宽度 */
    height: auto; /* 高度自适应 */
    display: block;
    margin: auto; /* 图片居中 */
    border-radius: 8px; /* 圆角效果 */
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease; /* 添加平滑过渡效果 */
}

/* 悬浮效果 */
.hover-effect:hover {
    transform: scale(1.05); /* 图片轻微放大 */
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3); /* 添加阴影 */
    cursor: pointer; /* 鼠标变为手型 */
}
</style>
