<script setup>
import { useLayout } from '@/layout/composables/layout';
import AppConfigurator from './AppConfigurator.vue';

const { onMenuToggle, toggleDarkMode, isDarkTheme } = useLayout();
</script>

<template>
    <div class="layout-topbar">
        <div class="layout-topbar-logo-container">
            <router-link to="/" class="layout-topbar-logo">
                <!-- 替换为你的 SVG 文件路径 -->
                <img src="@/assets/algicidedb1.svg" alt="My Logo" />
                <!-- 替换文本内容 -->
                <span>AlgicideDB</span>
            </router-link>
        </div>

        <button class="layout-menu-button layout-topbar-action" @click="onMenuToggle">
            <i class="pi pi-bars"></i>
        </button>

        <div class="layout-topbar-actions">
            <div class="layout-config-menu">
                <button type="button" class="layout-topbar-action" @click="toggleDarkMode">
                    <i :class="['pi', { 'pi-moon': isDarkTheme, 'pi-sun': !isDarkTheme }]"></i>
                </button>
                <div class="relative">
                    <button
                        v-styleclass="{ selector: '@next', enterFromClass: 'hidden', enterActiveClass: 'animate-scalein', leaveToClass: 'hidden', leaveActiveClass: 'animate-fadeout', hideOnOutsideClick: true }"
                        type="button"
                        class="layout-topbar-action layout-topbar-action-highlight"
                    >
                        <i class="pi pi-palette"></i>
                    </button>
                    <AppConfigurator />
                </div>
            </div>

            <button
                class="layout-topbar-menu-button layout-topbar-action"
                v-styleclass="{ selector: '@next', enterFromClass: 'hidden', enterActiveClass: 'animate-scalein', leaveToClass: 'hidden', leaveActiveClass: 'animate-fadeout', hideOnOutsideClick: true }"
            >
                <i class="pi pi-ellipsis-v"></i>
            </button>

            <div class="layout-topbar-menu hidden lg:block">
                <div class="layout-topbar-menu-content">
                    <!-- <button type="button" class="layout-topbar-action">
                        <i class="pi pi-calendar"></i>
                        <span>Calendar</span>
                    </button>
                    <button type="button" class="layout-topbar-action">
                        <i class="pi pi-inbox"></i>
                        <span>Messages</span>
                    </button> -->
                    <button type="button" class="layout-topbar-action relative group hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-md p-2">
                        <!-- 提示信息 -->
                        <div class="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 bg-gray-700 text-white text-xs rounded-md py-1 px-2 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 pointer-events-none">
                            Contact
                        </div>

                        <!-- 图标和文字 -->
                        <a href="https://person.zju.edu.cn/xixiao" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2">
                            <i class="pi pi-user text-lg"></i>
                            <span class="text-sm">Profile</span>
                        </a>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
