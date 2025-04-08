<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import {
		Label,
		Pagination,
		Select,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		type LinkType,
		type SelectOptionType
	} from 'flowbite-svelte';
	import { ChevronLeftOutline, ChevronRightOutline } from 'flowbite-svelte-icons';

	let { data = [], actions } = $props<{
		data: any[];
		actions: (row: any) => ReturnType<import('svelte').Snippet>;
	}>();

	const pageOptions: SelectOptionType<number>[] = [
		{ value: 3, name: '3' },
		{ value: 10, name: '10' },
		{ value: 25, name: '25' },
		{ value: 50, name: '50' }
	];

	// lee de URL
	let currentPage = $derived(parseInt(page.url.searchParams.get('page') || '1'));
	let perPage = $derived(parseInt(page.url.searchParams.get('perPage') || '25'));

	let total = $derived(data.length);
	const headers = $derived(
		Object.keys(data[0] || {})
			.filter((k) => !['usuario', 'activo', 'ruta_foto', 'ultima_sesion'].includes(k))
			.sort((a, b) => (a === 'id' ? -1 : b === 'id' ? 1 : 0))
	);
	let start = $derived((currentPage - 1) * perPage + 1);
	let end = $derived(Math.min(start + perPage - 1, total));
	let paginated = $derived(data.slice(start - 1, end));
	let totalPages = $derived(Math.ceil(total / perPage));

	let pages: LinkType[] = $derived(
		Array.from({ length: totalPages }, (_, i) => ({
			name: String(i + 1),
			href: `?page=${i + 1}&perPage=${perPage}`,
			active: i + 1 === currentPage
		}))
	);

	// navegación reactiva
	function goTo(p: number) {
		goto(`?page=${p}&perPage=${perPage}`, { replaceState: true });
	}

	function changePerPage() {
		goto(`?page=1&perPage=${perPage}`, { replaceState: true });
	}
</script>

<div class="w-full">
	<Table striped hoverable shadow>
		<TableHead>
			{#each headers as h}
				<TableHeadCell>{h.replace(/_/g, ' ')}</TableHeadCell>
			{/each}
			<TableHeadCell>Acciones</TableHeadCell>
		</TableHead>

		<TableBody tableBodyClass="divide-y">
			{#each paginated as row}
				<TableBodyRow>
					{#each headers.length ? headers : Object.keys(row) as h}
						{#if h === 'rol'}
							<TableBodyCell class="capitalize">{row[h].nombre}</TableBodyCell>
						{:else}
							<TableBodyCell>{row[h]}</TableBodyCell>
						{/if}
					{/each}
					<TableBodyCell>
						{@render actions(row)}
					</TableBodyCell>
				</TableBodyRow>
			{/each}
			{#if paginated.length === 0}
				<TableBodyRow>
					<TableBodyCell colspan={headers.length + 1} class="text-center py-4">
						No se encontraron resultados
					</TableBodyCell>
				</TableBodyRow>
			{/if}
		</TableBody>
	</Table>

	<div class="flex items-center justify-between mt-4 flex-wrap gap-2">
		<Label for="perPage" class="flex items-center">
			Filas por página
			<Select
				on:change={changePerPage}
				bind:value={perPage}
				items={pageOptions}
				id="perPage"
				class="ml-2 w-20"
			/>
		</Label>

		<span class="text-sm text-gray-700 dark:text-gray-400">
			Mostrando <b>{start}</b> - <b>{end}</b> de <b>{total}</b>
		</span>

		<Pagination
			{pages}
			on:click={(e) => goTo(Number(e.detail))}
			on:previous={() => goTo(Math.max(1, currentPage - 1))}
			on:next={() => goTo(Math.min(totalPages, currentPage + 1))}
		>
			<svelte:fragment slot="prev">
				<span class="sr-only">Anterior</span>
				<ChevronLeftOutline class="w-2.5 h-2.5" />
			</svelte:fragment>
			<svelte:fragment slot="next">
				<span class="sr-only">Siguiente</span>
				<ChevronRightOutline class="w-2.5 h-2.5" />
			</svelte:fragment>
		</Pagination>
	</div>
</div>
