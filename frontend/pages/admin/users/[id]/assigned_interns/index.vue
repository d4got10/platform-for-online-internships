<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonCreate page-name="assign" text="Прикрепить" />
            </template>
            <template #inputs>
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable
                :items="data!.items"
                :hide-fields="['is_admin', 'is_teacher']"
                link-param-name="intern_id"
            />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const { data, loadMore } = await useListLoader({
        path: '/api/users/{teacher_id}/assigned_interns',
        method: 'get',
        params: { teacher_id: route.params.id as string },
    });

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));
</script>
