import { defineStore } from 'pinia';

export const useSearchStore = defineStore('searchStore', {
    state: () => ({
        records: [] // 用于存储搜索结果
    }),
    actions: {
        setRecords(newRecords) {
            this.records = newRecords;
        },
        clearRecords() {
            this.records = [];
        }
    }
});
