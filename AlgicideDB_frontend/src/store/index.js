import { createStore } from 'vuex';

const store = createStore({
    state: {
        searchQuery: '', // 通用搜索词
        searchType: '', // 搜索类型 (general 或 advanced)
        advancedQueries: [] // 高级搜索查询条件
    },
    mutations: {
        setSearchQuery(state, query) {
            state.searchQuery = query;
        },
        setSearchType(state, type) {
            state.searchType = type;
        },
        setSearchAdvancedQueries(state, queries) {
            state.advancedQueries = queries;
        }
    },
    actions: {
        setSearchQuery({ commit }, query) {
            commit('setSearchQuery', query);
        },
        setSearchType({ commit }, type) {
            commit('setSearchType', type);
        },
        setSearchAdvancedQueries({ commit }, queries) {
            commit('setSearchAdvancedQueries', queries);
        }
    },
    getters: {
        getSearchQuery(state) {
            return state.searchQuery;
        },
        getSearchType(state) {
            return state.searchType;
        },
        getSearchAdvancedQueries(state) {
            return state.advancedQueries;
        }
    }
});

export default store;
