<template>
    <NuxtLayout>
        <NuxtLoadingIndicator />
        <NuxtPage />
    </NuxtLayout>
</template>

<style>
    .page-enter-active,
    .layout-enter-active,
    .page-leave-active,
    .layout-leave-active {
        transition: all 100ms;
    }
    .page-enter-from,
    .layout-enter-from,
    .page-leave-to,
    .layout-leave-to {
        opacity: 0;
    }
</style>
