<template>
    <table class="table-auto border-collapse rounded-md w-full bg-white shadow">
        <thead v-if="!hideHead">
            <tr class="border-b">
                <th v-for="(key, idx) in headerKeys" :key="idx" class="text-left px-4 py-2">{{ $t(key) }}</th>
            </tr>
        </thead>
        <tbody v-if="!disableDetailLinks">
            <NuxtLink
                v-for="(item, idx) in items"
                :key="idx"
                v-slot="{ navigate, href }"
                :to="getDetailLink(item)"
                :custom="true"
            >
                <tr class="border-b hover:bg-gray-100 hover:cursor-pointer" :data-href="href" @click.stop="navigate">
                    <td v-for="([key, value], valueIdx) in getEntries(item)" :key="valueIdx" class="px-4 py-2">
                        <FieldAbstract :field-name="key" :value="value" />
                    </td>
                </tr>
            </NuxtLink>
        </tbody>
        <tbody v-else>
            <tr v-for="(item, idx) in items" :key="idx" class="border-b">
                <td v-for="([key, value], valueIdx) in getEntries(item)" :key="valueIdx" class="px-4 py-2">
                    <FieldAbstract :field-name="key" :value="value" />
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script setup lang="ts">
    interface Item {
        id: number;
        [key: string]: unknown;
    }

    const route = useRoute();

    const props = withDefaults(
        defineProps<{
            items: Item[];
            withId?: boolean;
            linkParamName?: string;
            apiValueFieldName?: string;
            hideFields?: Array<string>;
            hideHead?: boolean;
            disableDetailLinks?: boolean;
            routeName?: string;
            routeParamsMap?: Record<string, string | number>;
        }>(),
        {
            linkParamName: 'id',
            apiValueFieldName: 'id',
            withId: false,
            hideFields: () => [],
            hideHead: false,
            disableDetailLinks: false,
            routeName: undefined,
            routeParamsMap: () => ({}),
        },
    );

    function getDetailLink(item: Item) {
        const routeName = props.routeName ?? route.name;
        const additionalParams: Record<string, string | number> = {};
        for (const [key, value] of Object.entries(props.routeParamsMap)) {
            additionalParams[key] = String(item[value]);
        }
        return {
            name: `${String(routeName)}-${props.linkParamName}`,
            params: {
                [props.linkParamName]: String(item[props.apiValueFieldName]),
                ...additionalParams,
            },
        };
    }

    function getEntries(item: Record<string, unknown>) {
        let entries = Object.entries(item);
        if (!props.withId) {
            entries = entries.filter(([key]) => key !== 'id');
        }
        if (props.hideFields.length) {
            entries = entries.filter(([key]) => !props.hideFields.includes(key));
        }
        return entries;
    }

    const headerKeys = computed(() => {
        if (props.items.length === 0) {
            return [];
        }
        let keys = Object.keys(props.items[0]);
        if (!props.withId) {
            keys = keys.filter(key => key !== 'id');
        }
        if (props.hideFields.length) {
            keys = keys.filter(key => !props.hideFields.includes(key));
        }
        return keys.map(value => capitalize(value.replaceAll('_', ' ')));
    });
</script>
