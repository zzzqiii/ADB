<script setup>
import axios from 'axios';
import ProgressBar from 'primevue/progressbar';
import { useToast } from 'primevue/usetoast';
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

// 在 FileUpload 的 before-upload 方法中设置 CSRF Token
const addCSRFToken = (event) => {
    if (csrfToken) {
        // 在上传的请求头中添加 X-CSRFToken
        event.xhr.setRequestHeader('X-CSRFToken', csrfToken);
        console.log('CSRF Token added to headers:', csrfToken);
    } else {
        console.error('CSRF Token not found!');
    }
};

const toast = useToast();
// const router = useRouter();

const showProgress = ref(false); // 是否显示进度条
const progressMessage = ref('Uploading file...'); // 进度消息
const resultLink = ref(''); // 结果链接
const exampleFiles = [
    { name: 'Example.csv', url: 'http://algicidedb.ocean-meta.com/algaecide/download/example.csv' },
    { name: 'Example.txt', url: 'http://algicidedb.ocean-meta.com/algaecide/download/example.txt' }
];
// 示例 SMILES 填充
const smilesInput = ref(''); // SMILES 输入框的内容
const onExampleFill = () => {
    smilesInput.value = 'C(C(=O)O)N\nC1=CC=CC=C1\nO=C(O)C1=CC=CC=C1';
    toast.add({
        severity: 'info',
        summary: 'Example Filled',
        detail: 'Example SMILES loaded successfully.',
        life: 3000
    });
};
// Tab 切换事件
const activeTab = ref('0'); // 当前激活的标签
const onTabChange = (newValue) => {
    if (newValue === '2') {
        window.open('https://admetlab3.scbdd.com/server/screening', '_blank');
        activeTab.value = '0'; // 重置回第一个 Tab
    }
};
// 上传成功回调
const onAdvancedUpload = (event) => {
    const response = JSON.parse(event.xhr.response); // 后端返回的数据
    console.log('Upload success:', response);

    // 提示上传成功
    toast.add({
        severity: 'success',
        summary: 'Upload Successful',
        detail: `File uploaded successfully! Task ID: ${response.task_id}`,
        life: 3000
    });

    // 显示进度条并模拟处理进度
    showProgress.value = true;

    progressMessage.value = 'Processing your file...';

    // 模拟后台处理完成（假设处理需要 3 秒）
    setTimeout(() => {
        progressMessage.value = 'Processing complete!';
        showProgress.value = false;

        // 显示结果链接
        if (response.task_id) {
            resultLink.value = `${window.location.origin}/#/predict/result/${response.task_id}`;
        } else {
            console.error('Task ID not found in response.');
            toast.add({
                severity: 'error',
                summary: 'Navigation Error',
                detail: 'Unable to generate the results link.',
                life: 3000
            });
        }
    }, 3000);
};

// 上传失败回调
const onUploadError = (event) => {
    toast.add({
        severity: 'error',
        summary: 'Upload Failed',
        detail: 'There was an error uploading your file.',
        life: 3000
    });
    console.error('Upload error:', event);
};
// 提交示例文件
const onSubmitExampleFile = () => {
    const taskId = 'exampleresult';
    resultLink.value = `${window.location.origin}/#/predict/result/${taskId}`;
    toast.add({
        severity: 'success',
        summary: 'Example Submitted',
        detail: 'Example results generated successfully!',
        life: 3000
    });
};

// 提交 SMILES 数据到后端
const onSubmitSmiles = async () => {
    if (!smilesInput.value.trim()) {
        toast.add({
            severity: 'error',
            summary: 'Submission Failed',
            detail: 'Please provide valid SMILES input.',
            life: 3000
        });
        return;
    }

    showProgress.value = true;
    progressMessage.value = 'Processing your SMILES...';

    try {
        const response = await axios.post('/algaecide/predict/', {
            smiles: smilesInput.value.trim()
        });

        const taskId = response.data.task_id;
        resultLink.value = `${window.location.origin}/#/predict/result/${taskId}`;
        progressMessage.value = 'Processing complete!';
        toast.add({
            severity: 'success',
            summary: 'SMILES Submitted',
            detail: 'Results generated successfully!',
            life: 3000
        });
    } catch (error) {
        console.error('SMILES submission failed:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to submit SMILES.',
            life: 3000
        });
    } finally {
        showProgress.value = false;
    }
};
</script>

<template>
    <div class="max-w-7xl mx-auto p-6 bg-white rounded-lg shadow-md space-y-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Predict Molecular Properties</h1>
        <!-- Description Section -->
        <div class="mb-6 text-gray-700 text-lg">
            <p>
                This tool is for predicting molecular properties by uploading a file containing SMILES strings or entering them directly in the text box. It performs a <strong>Quantitative Estimation of Algicide-Likeness</strong> and calculates key
                molecular properties including:
            </p>
            <ul class="list-disc list-inside ml-4 mt-2">
                <li>Molecular weight</li>
                <li>Octanol-water partition coefficient (logP)</li>
                <li>Number of hydrogen bond acceptors (HBA)</li>
                <li>Number of hydrogen bond donors (HBD)</li>
                <li>Number of rotatable bonds (nRotB)</li>
                <li>Number of aromatic rings (nArR)</li>
            </ul>
            <p class="mt-4">It allows compounds to be ranked by their relative merit as algicides. The results are displayed in a table and can be downloaded as a CSV file.</p>

            <p class="mt-4">
                Additionally, the tab links to
                <strong>AdmetLab Service</strong> for advanced aquatic toxicity predictions.
            </p>
        </div>
        <Tabs v-model:value="activeTab" @update:value="onTabChange">
            <TabList>
                <Tab value="0">Load a molecule file</Tab>
                <Tab value="1">Enter a list of SMILES</Tab>
                <Tab value="2">AdmetLab Service</Tab>
            </TabList>
            <!-- Tab 1: Upload File -->
            <TabPanel value="0">
                <div class="space-y-4">
                    <!-- 文件上传卡片 -->
                    <div class="card">
                        <Toast />
                        <!-- 文件上传 -->
                        <FileUpload name="file" url="http://algicidedb.ocean-meta.com/algaecide/predict/" :multiple="false" accept=".txt,.csv" :maxFileSize="5000000" @before-send="addCSRFToken" @upload="onAdvancedUpload" @error="onUploadError">
                            <template #empty>
                                <span class="text-gray-500">Drag and drop files here to upload, or click "Browse" to select a file.</span>
                            </template>
                        </FileUpload>

                        <!-- 进度条 -->
                        <div v-if="showProgress" class="mt-4">
                            <ProgressBar mode="indeterminate" class="w-full" />
                            <p class="text-center mt-2 text-gray-600">
                                {{ progressMessage }}
                            </p>
                        </div>

                        <!-- 结果链接 -->
                        <div v-if="resultLink" class="mt-4 text-center">
                            <div class="flex flex-col items-center space-y-2">
                                <i class="pi pi-check-circle text-green-500 text-4xl"></i>
                                <p class="text-gray-700 text-lg font-medium">Processing complete!</p>
                                <a :href="resultLink" class="p-button p-button-success p-button-rounded px-6 py-3 text-white"> View Results </a>
                            </div>
                        </div>
                    </div>

                    <!-- 示例文件链接 -->
                    <div class="flex space-x-4 items-center">
                        <a v-for="file in exampleFiles" :key="file.name" :href="file.url" class="text-blue-500 hover:underline" target="_blank">
                            {{ file.name }}
                        </a>
                        <Button label="Submit with example file" class="p-button-primary" @click="onSubmitExampleFile" />
                    </div>
                </div>
            </TabPanel>

            <!-- Tab 2: Enter a list of SMILES -->
            <TabPanel value="1">
                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-lg">SMILES (MAX 1000)</span>
                        <Button label="Example" class="p-button-info" @click="onExampleFill" />
                    </div>
                    <Textarea v-model="smilesInput" rows="10" placeholder="Enter SMILES" class="w-full border rounded-md p-2" />
                    <div v-if="showProgress" class="mt-4">
                        <ProgressBar mode="indeterminate" class="w-full" />
                        <p class="text-center mt-2 text-gray-600">{{ progressMessage }}</p>
                    </div>
                    <div v-if="resultLink" class="mt-4 text-center">
                        <div class="flex flex-col items-center space-y-2">
                            <i class="pi pi-check-circle text-green-500 text-4xl"></i>
                            <p class="text-gray-700 text-lg font-medium">Processing complete!</p>
                            <a :href="resultLink" class="p-button p-button-success p-button-rounded px-6 py-3 text-white"> View Results </a>
                        </div>
                    </div>
                    <div class="flex justify-end space-x-4 mt-4">
                        <Button label="Submit" class="p-button-success" @click="onSubmitSmiles" />
                    </div>
                </div>
            </TabPanel>

            <!-- Tab 3: External Service -->
            <TabPanel value="2">
                <div class="text-center">
                    <p class="text-gray-700 mb-4">Redirecting to <a href="https://admetlab3.scbdd.com/server/screening" class="text-blue-500 hover:underline">AdmetLab 3.0</a>...</p>
                </div>
            </TabPanel>
        </Tabs>
    </div>
</template>
