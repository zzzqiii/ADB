<script setup>
import axios from 'axios';
import { useToast } from 'primevue/usetoast'; // 引入 PrimeVue 的 Toast 组件
import { ref } from 'vue';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrfToken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
axios.defaults.withCredentials = true; // 确保跨域请求附带 Cookie

const toast = useToast(); // 初始化 Toast

// 表单数据
const formData = ref({
    algae_name: '',
    algae_strain: '',
    phylum: '',
    class_name: '',
    order: '',
    family: '',
    algae_risk: '',
    algae_environment: '',
    chemical_name: '',
    cas_number: '',
    is_natural_product: null,
    chemical_source: '',
    classification: '',
    measurement: '',
    effect: '',
    unit: '',
    cultivation_system: '',
    irradiance: '',
    initial_density: '',
    temperature: '',
    time: '',
    response: '',
    mechanism: '',
    submitter_name: '', // 提交人姓名
    submitter_email: '' // 提交人邮箱
});

// 错误信息
const errors = ref({});

// 选项
const riskOptions = [
    { label: 'Toxic', value: 'toxic' },
    { label: 'Harmful but non-toxic', value: 'harmful but non-toxic' },
    { label: 'Fouling', value: 'fouling' },
    { label: 'Harmless', value: 'harmless' },
    { label: 'Unknown', value: 'unknown' }
];

const environmentOptions = [
    { label: 'Freshwater', value: 'freshwater' },
    { label: 'Marine', value: 'marine' },
    { label: 'Brackish', value: 'brackish' },
    { label: 'Unknown', value: 'unknown' }
];

const booleanOptions = [
    { label: 'Yes', value: true },
    { label: 'No', value: false }
];

const loading = ref(false);

// 提交表单
const handleSubmit = async () => {
    errors.value = {}; // 清空错误信息

    if (!formData.value.algae_name) {
        errors.value.algae_name = 'Algae Name is required.';
    }

    if (!formData.value.chemical_name) {
        errors.value.chemical_name = 'Chemical Name is required.';
    }

    if (!formData.value.measurement) {
        errors.value.measurement = 'Measurement is required.';
    }

    if (!formData.value.effect) {
        errors.value.effect = 'Effect is required.';
    }

    // 如果有错误信息，阻止提交
    if (Object.keys(errors.value).length > 0) {
        return;
    }

    loading.value = true;

    try {
        await axios.post('/algaecide/submit/', formData.value);
        toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Record submitted successfully!',
            life: 3000
        });
        formData.value = {}; // 清空表单
    } catch (error) {
        console.error('Error submitting record:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to submit record.',
            life: 3000
        });
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div class="max-w-7xl mx-auto p-6 bg-white rounded-lg shadow-md space-y-6">
        <h1 class="text-3xl font-bold text-gray-800 text-center">Submit New Record</h1>

        <!-- Introductory Explanation -->
        <div class="p-4 bg-gray-100 rounded-lg">
            <p class="text-gray-800">
                This page is for submitting new algicidal data that is not currently included in the database. By sharing data, you can help expand the database and support the community in advancing research and knowledge about algicides. Fields
                marked with <span class="text-red-500">*</span> are required.
            </p>
        </div>

        <!-- Algae Information -->
        <Panel header="Algae Information" toggleable class="mb-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Algae Name -->
                <div>
                    <label for="algae_name" class="block text-sm font-medium text-gray-700"> Algae Name <span class="text-red-500">*</span> </label>
                    <InputText v-model="formData.algae_name" id="algae_name" placeholder="Enter Algae Name" class="w-full" />
                    <small v-if="errors.algae_name" class="text-red-500">{{ errors.algae_name }}</small>
                </div>

                <!-- Algae Strain -->
                <div>
                    <label for="algae_strain" class="block text-sm font-medium text-gray-700">Algae Strain</label>
                    <InputText v-model="formData.algae_strain" id="algae_strain" placeholder="Enter Algae Strain" class="w-full" />
                </div>

                <!-- Phylum, Class Name, Order, Family -->
                <div class="col-span-2">
                    <div class="grid grid-cols-4 gap-4">
                        <div>
                            <label for="phylum" class="block text-sm font-medium text-gray-700">Phylum</label>
                            <InputText v-model="formData.phylum" id="phylum" placeholder="Enter Phylum" class="w-full" />
                        </div>
                        <div>
                            <label for="class_name" class="block text-sm font-medium text-gray-700">Class Name</label>
                            <InputText v-model="formData.class_name" id="class_name" placeholder="Enter Class Name" class="w-full" />
                        </div>
                        <div>
                            <label for="order" class="block text-sm font-medium text-gray-700">Order</label>
                            <InputText v-model="formData.order" id="order" placeholder="Enter Order" class="w-full" />
                        </div>
                        <div>
                            <label for="family" class="block text-sm font-medium text-gray-700">Family</label>
                            <InputText v-model="formData.family" id="family" placeholder="Enter Family" class="w-full" />
                        </div>
                    </div>
                </div>

                <!-- Algae Risk -->
                <div>
                    <label for="algae_risk" class="block text-sm font-medium text-gray-700">Algae Risk</label>
                    <Dropdown v-model="formData.algae_risk" :options="riskOptions" optionLabel="label" optionValue="value" placeholder="Select Risk" class="w-full" />
                </div>

                <!-- Algae Environment -->
                <div>
                    <label for="algae_environment" class="block text-sm font-medium text-gray-700">Environment</label>
                    <Dropdown v-model="formData.algae_environment" :options="environmentOptions" optionLabel="label" optionValue="value" placeholder="Select Environment" class="w-full" />
                </div>
            </div>
        </Panel>

        <!-- Chemical Information -->
        <Panel header="Chemical Information" toggleable class="mb-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label for="chemical_name" class="block text-sm font-medium text-gray-700"> Chemical Name <span class="text-red-500">*</span> </label>
                    <InputText v-model="formData.chemical_name" id="chemical_name" placeholder="Enter Chemical Name" class="w-full" />
                    <small v-if="errors.chemical_name" class="text-red-500">{{ errors.chemical_name }}</small>
                </div>

                <div>
                    <label for="cas_number" class="block text-sm font-medium text-gray-700">CAS Number</label>
                    <InputText v-model="formData.cas_number" id="cas_number" placeholder="Enter CAS Number" class="w-full" />
                </div>

                <div>
                    <label for="is_natural_product" class="block text-sm font-medium text-gray-700">Is it a Natural Product?</label>
                    <Dropdown v-model="formData.is_natural_product" :options="booleanOptions" optionLabel="label" optionValue="value" placeholder="Select Yes or No" class="w-full" />
                </div>

                <div v-if="formData.is_natural_product === true">
                    <label for="chemical_source" class="block text-sm font-medium text-gray-700">Source</label>
                    <InputText v-model="formData.chemical_source" id="chemical_source" placeholder="Enter Source (e.g., Plant)" class="w-full" />
                </div>

                <div>
                    <label for="classification" class="block text-sm font-medium text-gray-700">Classification</label>
                    <InputText v-model="formData.classification" id="classification" placeholder="Enter Classification" class="w-full" />
                </div>
            </div>
        </Panel>

        <!-- Experimental Details -->
        <Panel header="Experimental Details" toggleable class="mb-4">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div>
                    <label for="measurement" class="block text-sm font-medium text-gray-700"> Measurement <span class="text-red-500">*</span> </label>
                    <InputText v-model="formData.measurement" id="measurement" placeholder="e.g., EC50, IC50, Inhibition rate under concentration" class="w-full" />
                    <small v-if="errors.measurement" class="text-red-500">{{ errors.measurement }}</small>
                </div>

                <div>
                    <label for="effect" class="block text-sm font-medium text-gray-700"> Effect <span class="text-red-500">*</span> </label>
                    <InputText v-model="formData.effect" id="effect" placeholder="Enter specific effect value" class="w-full" />
                    <small v-if="errors.effect" class="text-red-500">{{ errors.effect }}</small>
                </div>

                <div>
                    <label for="unit" class="block text-sm font-medium text-gray-700">Unit</label>
                    <InputText v-model="formData.unit" id="unit" placeholder="Enter Unit" class="w-full" />
                </div>

                <div>
                    <label for="cultivation_system" class="block text-sm font-medium text-gray-700">Cultivation System</label>
                    <InputText v-model="formData.cultivation_system" id="cultivation_system" placeholder="Enter Cultivation System" class="w-full" />
                </div>

                <div>
                    <label for="irradiance" class="block text-sm font-medium text-gray-700">Irradiance</label>
                    <InputText v-model="formData.irradiance" id="irradiance" placeholder="Enter Irradiance" class="w-full" />
                </div>

                <div>
                    <label for="initial_density" class="block text-sm font-medium text-gray-700">Initial Density</label>
                    <InputText v-model="formData.initial_density" id="initial_density" placeholder="Enter Initial Density" class="w-full" />
                </div>

                <div>
                    <label for="temperature" class="block text-sm font-medium text-gray-700">Temperature</label>
                    <InputText v-model="formData.temperature" id="temperature" placeholder="Enter Temperature" class="w-full" />
                </div>

                <div>
                    <label for="time" class="block text-sm font-medium text-gray-700">Time</label>
                    <InputText v-model="formData.time" id="time" placeholder="Enter Time" class="w-full" />
                </div>

                <div>
                    <label for="response" class="block text-sm font-medium text-gray-700">Response</label>
                    <InputText v-model="formData.response" id="response" placeholder="Enter Response" class="w-full" />
                </div>

                <div class="col-span-3">
                    <label for="mechanism" class="block text-sm font-medium text-gray-700">Mechanism</label>
                    <Textarea v-model="formData.mechanism" id="mechanism" rows="4" placeholder="Describe Mechanism" class="w-full" />
                </div>
            </div>
        </Panel>

        <!-- Submitter Information -->
        <Panel header="Submitter Information" toggleable class="mb-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Submitter Name -->
                <div>
                    <label for="submitter_name" class="block text-sm font-medium text-gray-700">Submitter Name <span class="text-red-500">*</span></label>
                    <InputText v-model="formData.submitter_name" id="submitter_name" placeholder="Enter Submitter Name" class="w-full" />
                    <small v-if="errors.submitter_name" class="text-red-500">{{ errors.submitter_name }}</small>
                </div>

                <!-- Submitter Email -->
                <div>
                    <label for="submitter_email" class="block text-sm font-medium text-gray-700">Submitter Email <span class="text-red-500">*</span></label>
                    <InputText v-model="formData.submitter_email" id="submitter_email" placeholder="Enter Submitter Email" class="w-full" />
                    <small v-if="errors.submitter_email" class="text-red-500">{{ errors.submitter_email }}</small>
                </div>
            </div>
        </Panel>

        <!-- Submit Button -->
        <div class="flex justify-center">
            <Button label="Submit" icon="pi pi-check" :loading="loading" @click="handleSubmit" />
        </div>
    </div>
</template>
