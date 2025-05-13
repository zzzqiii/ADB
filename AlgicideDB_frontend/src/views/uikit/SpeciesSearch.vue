<script>
export default {
    data() {
        return {
            filters: {
                speciesName: '',
                kingdom: ''
            }
        };
    },
    methods: {
        submitForm() {
            this.$emit('search', this.filters);
        }
    }
};
</script>

<template>
    <form @submit.prevent="submitForm">
        <!-- 物种名称 -->
        <div class="mb-4">
            <label for="speciesName" class="block text-sm font-medium">物种名称</label>
            <input type="text" id="speciesName" v-model="filters.speciesName" class="mt-1 p-2 border rounded w-full" placeholder="Enter species name" />
        </div>

        <!-- 分类筛选 -->
        <div class="mb-4">
            <label class="block text-sm font-medium">分类</label>
            <div>
                <label>
                    <input type="radio" value="Animals" v-model="filters.kingdom" />
                    动物
                </label>
                <label>
                    <input type="radio" value="Plants" v-model="filters.kingdom" />
                    植物
                </label>
                <label>
                    <input type="radio" value="Both" v-model="filters.kingdom" />
                    Both
                </label>
            </div>
        </div>

        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">搜索</button>
    </form>
</template>
