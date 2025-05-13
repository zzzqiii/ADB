<script>
export default {
    data() {
        return {
            filters: {
                chemicalName: '',
                group: []
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
        <!-- 化学品名称 -->
        <div class="mb-4">
            <label for="chemicalName" class="block text-sm font-medium">化学品名称</label>
            <input type="text" id="chemicalName" v-model="filters.chemicalName" class="mt-1 p-2 border rounded w-full" placeholder="Enter chemical name" />
        </div>

        <!-- 分类 -->
        <div class="mb-4">
            <label class="block text-sm font-medium">化学品分类</label>
            <div>
                <label>
                    <input type="checkbox" value="Organic" v-model="filters.group" />
                    有机化合物
                </label>
                <label>
                    <input type="checkbox" value="Metal" v-model="filters.group" />
                    金属化合物
                </label>
            </div>
        </div>

        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">搜索</button>
    </form>
</template>
