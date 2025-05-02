<script lang="ts">
	import { Button, Select, Input } from 'flowbite-svelte';
	import {DataTable} from '$lib'; // Ajusta la ruta según tu estructura

	const estudiantes = [
		{ nombre: 'Nero Sanford', ci: 'E-16', corte1: null, corte2: null, corte3: null, promedio: 0 },
		{ nombre: 'Zahir Hart', ci: 'E-240', corte1: 17, corte2: 18, corte3: null, promedio: 10.5 },
		{
			nombre: 'Tanner Shannon',
			ci: 'E-254',
			corte1: 12,
			corte2: null,
			corte3: null,
			promedio: 8.1
		},
		{
			nombre: 'Melodie Montgomery',
			ci: 'E-75',
			corte1: 20,
			corte2: null,
			corte3: null,
			promedio: 0
		},
		{
			nombre: 'Francisco Silva',
			ci: 'V-30555724',
			corte1: null,
			corte2: null,
			corte3: null,
			promedio: 0
		}
	];

	let estudianteSeleccionado = estudiantes[0];
	let corte = '';
	let nota = '';
	let mostrarFormulario = false;

</script>

<div class="container mx-auto p-4">
	<h2 class="text-xl font-bold mb-4">
		Notas de estudiantes en <span class="text-blue-600">INGLES I</span>
	</h2>
	{#snippet actions(row: any)}
		<div class="flex gap-2"></div>
	{/snippet}

	<DataTable data={estudiantes} {actions} />

	{#if mostrarFormulario}
		<div class="mt-6 border p-4 rounded-md bg-white shadow">
			<h3 class="font-semibold mb-3 text-lg">Asignación de Notas</h3>

			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<Input label="Estudiante" value={estudianteSeleccionado.ci} disabled filled />

				<Select bind:value={corte} label="Corte">
					<option disabled value="">Seleccione una nota</option>
					<option value="corte1">1er corte</option>
					<option value="corte2">2do corte</option>
					<option value="corte3">3er corte</option>
				</Select>

				<Input type="number" label="Nota" bind:value={nota} min="0" max="20" filled />
			</div>

			<div class="flex gap-4 mt-6">
				<Button color="red" on:click={() => (mostrarFormulario = false)}>Cancelar</Button>
				<Button
					on:click={() => {
						if (corte && nota !== '') {
							estudianteSeleccionado[corte] = Number(nota);
							mostrarFormulario = false;
						}
					}}>Editar</Button
				>
			</div>

			<details class="mt-4 text-sm">
				<summary class="cursor-pointer text-blue-600">¿Hay alguna nota errónea?</summary>
				<p class="mt-2">Solicite corrección al control de estudio.</p>
			</details>
		</div>
	{/if}
</div>
