<script lang="ts">
	import { DataTable } from '$lib';
	import { Button } from 'flowbite-svelte';
	import { CheckOutline, CloseOutline, XSolid } from 'flowbite-svelte-icons';
	import type { Peticion } from '../../../app';

	let { data } = $props();

	let peticiones = $derived(data.peticiones);
</script>

<div class="container mx-auto p-4">
	<h2 class="md:text-2xl text-xl font-bold mb-4">Peticiones de cambio de notas</h2>
	{#snippet actions(row: Peticion)}
		<div class="flex gap-2">
			<Button type="button" pill color="green" outline class="p-1!" size="sm">
				<CheckOutline class="w-5 h-5" />
			</Button>
			<Button type="button" pill color="red" outline class="p-1!" size="sm">
				<CloseOutline class="w-5 h-5" />
			</Button>
		</div>
	{/snippet}

	<DataTable data={peticiones} {actions} onSearch={(key: string, value: string) => 'hola'} />
</div>
