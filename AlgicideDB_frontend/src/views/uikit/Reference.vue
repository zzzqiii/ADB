<script setup>
import axios from 'axios';
import Paginator from 'primevue/paginator';
import { onMounted, ref } from 'vue';

const references = ref([]); // Store fetched references
const filteredReferences = ref([]); // Store filtered references based on search
const currentPage = ref(0); // For paginator
const pageSize = ref(5); // Number of references per page
const totalRecords = ref(0); // Total number of references
const searchQuery = ref(''); // Search query
const loading = ref(true);

// Fetch references from backend
const fetchReferences = async () => {
    try {
        const response = await axios.get('/algaecide/reference/');
        references.value = response.data;
        filteredReferences.value = references.value.slice(0, pageSize.value); // Initial page load
        totalRecords.value = references.value.length; // Set total records for paginator
        loading.value = false;
    } catch (error) {
        console.error('Error fetching references:', error);
    }
};

// Filter references based on search
const filterReferences = () => {
    const query = searchQuery.value.toLowerCase();
    const filtered = references.value.filter((ref) => ref.title.toLowerCase().includes(query) || ref.author.toLowerCase().includes(query) || ref.publication_title?.toLowerCase().includes(query));
    totalRecords.value = filtered.length;
    updatePage(0, pageSize.value, filtered);
};

// Update the displayed references when pagination changes
const updatePage = (page, size, data = references.value) => {
    const start = page * size;
    const end = start + size;
    filteredReferences.value = data.slice(start, end);
};

// Handle pagination event
const onPageChange = (event) => {
    currentPage.value = event.page;
    updatePage(event.page, event.rows);
};

// Initialize data when component is mounted
onMounted(() => {
    fetchReferences();
});
</script>

<template>
    <div class="container">
        <!-- Search bar -->
        <div class="search-bar">
            <InputText v-model="searchQuery" placeholder="Search References" />
            <Button icon="pi pi-search" label="Search" @click="filterReferences" />
        </div>

        <!-- Reference list -->
        <div class="reference-list">
            <div v-for="(ref, index) in filteredReferences" :key="index" class="reference-card">
                <div class="reference-title">
                    <a :href="ref.url" target="_blank" v-html="ref.title"></a>
                </div>
                <div class="reference-meta">
                    <span class="reference-author">{{ ref.author }}</span> -
                    <span class="reference-year">{{ ref.publication_year }}</span>
                </div>
                <div class="reference-publication">
                    <span>{{ ref.publication_title }}</span>
                </div>
                <div class="reference-doi">
                    <a v-if="ref.doi" :href="`https://doi.org/${ref.doi}`" target="_blank">{{ ref.doi }}</a>
                </div>
            </div>
        </div>

        <!-- Pagination -->
        <Paginator :first="currentPage * pageSize" :rows="pageSize" :totalRecords="totalRecords" @page="onPageChange" :rowsPerPageOptions="[5, 10, 20]" />
    </div>
</template>

<style scoped>
.container {
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.search-bar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.reference-list {
    margin-bottom: 20px;
}

.reference-card {
    padding: 15px;
    margin-bottom: 10px;
    border-bottom: 1px solid #ddd;
}

.reference-title a {
    font-size: 1.2em;
    font-weight: bold;
    color: #0073e6;
}

.reference-meta,
.reference-publication,
.reference-doi {
    font-size: 0.9em;
    color: #555;
}

.reference-doi a {
    color: #0073e6;
    text-decoration: underline;
}

.paginator {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
</style>
