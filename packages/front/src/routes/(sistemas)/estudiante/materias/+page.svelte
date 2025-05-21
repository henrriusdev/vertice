<script lang="ts">
	import { DataTable } from '$lib';

	let {data} = $props();
	let historicoMaterias = $derived(data.historico);
</script>

<div class="container mx-auto p-4">
	<h1 class="text-3xl font-bold mb-6">Materias cursando actualmente</h1>

	<DataTable data={historicoMaterias} />
</div>
