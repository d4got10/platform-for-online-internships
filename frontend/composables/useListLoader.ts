import type { LocationQuery, LocationQueryValue } from 'vue-router';
import { APIPath, APIMethod, LoaderArgs } from '~/types';

interface ExtendedLoaderArgs extends LoaderArgs {
    otherQueries?: {
        [k: string]: LocationQueryValue | LocationQueryValue[] | string | undefined;
    };
}

export default async function <P extends APIPath, M extends APIMethod<P>>({
    path,
    method,
    params,
    watchQuery,
}: {
    path: P;
    method: M;
    params?: Record<string, string | number>;
    watchQuery?: Record<string, Ref<string | number | undefined>>;
}) {
    const { $api } = useNuxtApp();
    const config = useRuntimeConfig();
    const route = useRoute();

    function filterRouteQuery(newQuery: LocationQuery) {
        return Object.fromEntries(Object.entries(newQuery).filter(([key]) => !['limit', 'offset'].includes(key)));
    }

    function unpackWatchQueries() {
        if (!watchQuery) {
            return {};
        }
        return Object.fromEntries(
            Object.entries(watchQuery).map(([key, value]) => {
                let v = value.value;
                if (v !== undefined) {
                    v = String(v);
                }
                return [key, v];
            }),
        );
    }

    const loader = ({ limit, offset, otherQueries }: ExtendedLoaderArgs = {}) => {
        return $api({
            path,
            method,
            query: {
                ...otherQueries,
                limit,
                offset,
            },
            params,
        });
    };

    const data = ref(
        await loader({
            limit: config.public.pageSize,
            otherQueries: {
                ...filterRouteQuery(route.query),
                ...unpackWatchQueries(),
            },
        }),
    );

    async function loadMore({ limit, offset }: LoaderArgs) {
        const newData = await loader({ limit, offset });
        // @ts-expect-error expecting list path
        data.value = {
            ...newData,
            // @ts-expect-error expecting list path
            items: [...data.value!.items, ...newData.items],
        };
    }

    watch(toRef(route, 'query'), async newQuery => {
        // @ts-expect-error expecting list path
        data.value = await loader({
            limit: config.public.pageSize,
            otherQueries: {
                ...filterRouteQuery(newQuery),
                ...unpackWatchQueries(),
            },
        });
    });

    if (watchQuery) {
        for (const [key, value] of Object.entries(watchQuery)) {
            watch(value, async value => {
                if (value !== undefined) {
                    value = String(value);
                }
                // @ts-expect-error expecting list path
                data.value = await loader({
                    limit: config.public.pageSize,
                    otherQueries: {
                        ...filterRouteQuery(route.query),
                        ...unpackWatchQueries(),
                        [key]: value,
                    },
                });
            });
        }
    }

    return {
        data,
        loadMore,
    };
}
