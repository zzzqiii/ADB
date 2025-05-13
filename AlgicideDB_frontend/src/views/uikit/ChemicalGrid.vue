<script setup>
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';

// 接收 origin 属性
const props = defineProps({
    origin: String
});

const chemicalList = ref([]); // 全部化合物数据
const filteredChemicals = ref([]); // 过滤后的化合物数据

// 过滤符合 origin 的化合物
const filterChemicals = () => {
    if (props.origin) {
        filteredChemicals.value = chemicalList.value.filter((chemical) => chemical.origin === props.origin);
    }
};

// 监听 props.origin 变化时，重新过滤化合物数据
watch(() => props.origin, filterChemicals);

// 获取化合物数据
const fetchChemicalData = async () => {
    try {
        const response = await axios.get('/algaecide/chemical/');
        chemicalList.value = response.data; // 将返回的数据存储在 chemicalList 中
        filterChemicals(); // 数据加载后立即进行过滤
    } catch (error) {
        console.error('Error fetching chemical data:', error);
    }
};

// 使用 onMounted 生命周期钩子来加载数据
onMounted(fetchChemicalData);
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <!-- DataView 组件 -->
            <DataView :value="filteredChemicals" layout="grid" :paginator="true" :rows="8">
                <!-- Grid 模式 -->
                <template #grid="slotProps">
                    <div v-if="slotProps.items.length > 0" class="grid grid-cols-12 gap-4">
                        <div v-for="(chemical, index) in slotProps.items" :key="index" class="col-span-12 sm:col-span-6 md:col-span-4 xl:col-span-3 p-2">
                            <Card class="h-full rounded-lg shadow-md overflow-hidden">
                                <template #header>
                                    <!-- 固定图片区域高度 -->
                                    <div class="relative w-full h-48 md:h-56 lg:h-60 overflow-hidden">
                                        <router-link :to="{ path: `/algicides/${chemical.id}` }" class="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer">
                                            <img v-if="chemical.image" :src="chemical.image" :alt="chemical.name" class="w-full h-full object-cover" />
                                        </router-link>
                                        <!-- <a href="javascript:void(0)" @click="navigateToRecords(chemical.name)" class="block">
                                            <img v-if="chemical.image" :src="chemical.image" :alt="chemical.name" class="w-full h-full object-cover" />
                                        </a> -->
                                    </div>
                                </template>
                                <template #title>
                                    <!-- 使用flex布局使文字垂直水平居中 -->
                                    <div class="text-center py-2">
                                        <div class="text-lg font-medium">
                                            <router-link :to="{ path: `/algicides/${chemical.id}` }" class="text-primary" target="_blank" rel="noopener noreferrer">
                                                {{ chemical.name }}
                                            </router-link>
                                        </div>
                                    </div>
                                </template>
                            </Card>
                        </div>
                    </div>
                    <!-- 如果没有匹配的化合物数据，显示提示信息 -->
                    <p v-else>No chemicals found for the selected origin.</p>
                </template>
            </DataView>
        </div>
    </div>
</template>

<style scoped>
.grid {
    padding: 20px;
}

.text-lg {
    font-size: 1.125rem;
}

.text-sm {
    font-size: 0.875rem;
}
</style>
