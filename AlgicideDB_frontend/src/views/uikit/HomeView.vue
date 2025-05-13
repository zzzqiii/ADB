<script setup>
import PhotoService from '@/service/PhotoService';
import ProductService from '@/service/ProductService';
import { onMounted, ref } from 'vue';

const products = ref([]);
const images = ref([]);
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

const productService = new ProductService();
const photoService = new PhotoService();

onMounted(() => {
    productService.getProductsSmall().then((data) => (products.value = data));
    photoService.getImages().then((data) => (images.value = data));
});
</script>

<template>
    <!-- <div class="grid p-fluid">
        <div class="col-12">
            <div class="card">
                <div class="grid grid-nogutter surface-section text-800">
                    <div class="col-12 md:col-6 p-6 text-center md:text-left flex align-items-center">
                        <section>
                            <span class="block text-6xl font-bold mb-1"></span>
                            <div class="text-6xl text-primary font-bold mb-3">Algaecide Database</div>
                            <p class="mt-0 mb-4 text-700 line-height-3">
                                Algae bloom represent a growing threat to global water security. With fast proliferation, they raise great concern due to potential health and socioeconomic concerns. Algaecides are commonly employed as a mitigative
                                measure to suppress and manage algae bloom. AlgaecideDB is a comprehensive Knowledgebase providing algaecide data including the toxicity data.
                            </p>
                        </section>
                    </div>
                    <div class="col-12 md:col-6 overflow-hidden">
                        <Carousel :value="products" :numVisible="1" :numScroll="1" circular :responsiveOptions="carouselResponsiveOptions" :autoplayInterval="4000" :showNavigators="false" :showIndicators="false">
                            <template #item="product">
                                <img
                                    :src="'demo/images/product/' + product.data.image"
                                    :alt="product.data.name"
                                    class="md:ml-auto block md:h-full"
                                    width="100%"
                                    style="height: auto; margin: auto; clip-path: polygon(8% 0, 100% 0%, 100% 100%, 0 100%)"
                                />
                            </template>
                        </Carousel>
                    </div>
                </div>
            </div>
        </div>
    </div> -->

    <div class="grid p-fluid">
        <!-- <div class="col-12"> -->
        <div class="card">
            <div class="grid grid-nogutter surface-section text-800">
                <div class="col-span-12 md:col-span-12 p-6 text-center md:text-left flex align-items-center">
                    <section>
                        <span class="block text-6xl font-bold mb-1"></span>
                        <div class="text-6xl text-primary font-bold mb-3">Algaecide Database</div>
                        <p class="mt-0 mb-4 text-700 line-height-3">
                            Algae bloom represent a growing threat to global water security. With fast proliferation, they raise great concern due to potential health and socioeconomic concerns. Algaecides are commonly employed as a mitigative
                            measure to suppress and manage algae bloom. AlgaecideDB is a comprehensive Knowledgebase providing algaecide data including the toxicity data.
                        </p>
                    </section>
                </div>
                <div class="col-span-12 md:col-span-6">
                    <Carousel :value="products" :numVisible="1" :numScroll="1" circular :responsiveOptions="carouselResponsiveOptions" :autoplayInterval="4000" :showNavigators="false" :showIndicators="false">
                        <template #item="product">
                            <img :src="'demo/images/product/' + product.data.image" :alt="product.data.name" class="md:ml-auto block md:h-full" width="50%" style="height: auto; margin: auto; clip-path: polygon(8% 0, 100% 0%, 100% 100%, 0 100%)" />
                        </template>
                    </Carousel>
                </div>
            </div>
        </div>
        <!-- </div> -->
    </div>

    <div class="grid">
        <div class="col-12 md:col-6">
            <section>
                <h1>Create the screens</h1>
                <h2>Your visitors deserve to see</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                <button pButton pRipple label="Learn More" type="button" class="mr-3 p-button-raised"></button>
                <button pButton pRipple label="Live Demo" type="button" class="p-button-outlined"></button>
            </section>
        </div>

        <div class="col-12 md:col-6">
            <img src="/demo/images/product/blue-t-shirt.jpg" alt="Image" style="width: 100%; height: auto" />
        </div>
    </div>

    <br />
    <div class="grid grid-cols-12 gap-8">
        <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Orders</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">152</div>
                    </div>
                    <div class="flex items-center justify-center bg-blue-100 dark:bg-blue-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-shopping-cart text-blue-500 !text-xl"></i>
                    </div>
                </div>
                <span class="text-primary font-medium">24 new </span>
                <span class="text-muted-color">since last visit</span>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Revenue</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">$2.100</div>
                    </div>
                    <div class="flex items-center justify-center bg-orange-100 dark:bg-orange-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-dollar text-orange-500 !text-xl"></i>
                    </div>
                </div>
                <span class="text-primary font-medium">%52+ </span>
                <span class="text-muted-color">since last week</span>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Customers</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">28441</div>
                    </div>
                    <div class="flex items-center justify-center bg-cyan-100 dark:bg-cyan-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-users text-cyan-500 !text-xl"></i>
                    </div>
                </div>
                <span class="text-primary font-medium">520 </span>
                <span class="text-muted-color">newly registered</span>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Comments</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">152 Unread</div>
                    </div>
                    <div class="flex items-center justify-center bg-purple-100 dark:bg-purple-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-comment text-purple-500 !text-xl"></i>
                    </div>
                </div>
                <span class="text-primary font-medium">85 </span>
                <span class="text-muted-color">responded</span>
            </div>
        </div>
    </div>
</template>

<!-- <Carousel :value="products" :numVisible="1" :numScroll="1" :responsiveOptions="responsiveOptions" circular :autoplayInterval="3000">
  <div class="relative mx-auto">
      <img :src="'https://primefaces.org/cdn/primevue/images/product/' + slotProps.data.image" :alt="slotProps.data.name" class="w-full border-round" />
  </div>
</Carousel> -->
