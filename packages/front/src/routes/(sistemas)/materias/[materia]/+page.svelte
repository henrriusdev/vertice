<script lang="ts">
	import { DataTable, nota as notaMask } from '$lib';
	import { Button, Input, Modal, Select, Textarea } from 'flowbite-svelte';
	import { imask } from '@imask/svelte';
	import { PenOutline, ReceiptOutline } from 'flowbite-svelte-icons';
	import type { Nota } from '../../../../app';

	let { data } = $props();

	let estudiantes = $derived(
		data.materia.materia.estudiantes.map((e) => ({
			...e,
			...e.notas.reduce((acc, n, i) => ({ ...acc, [`nota ${i + 1}`]: n }), {})
		}))
	);

	let estudianteSeleccionado: Nota | null = $state(null);
	let corte = $state('');
	let nota = $state('');
	let mostrarFormulario = $state(false);
	let esPeticion = $state(false);

	const handleEdit = (row: Nota) => {
		mostrarFormulario = true;
		console.log(row);
	};

	const handlePeticion = (row: Nota) => {
		mostrarFormulario = true;
		esPeticion = true;
		console.log(row);
	};

	$effect(() => {
		if (estudiantes.length) {
			estudianteSeleccionado = estudiantes[0];
		}
	});
</script>

<div class="container mx-auto p-4">
	<h2 class="md:text-2xl text-xl font-bold mb-4">
		Notas de estudiantes en <span class="text-blue-600">{data.materia.materia.nombre}</span>
	</h2>
	{#snippet actions(row: Nota)}
		<div class="flex gap-2">
			<Button
				type="button"
				onclick={() => handleEdit(row)}
				pill
				color="primary"
				outline
				class="p-1!"
				size="sm"
			>
				<PenOutline class="w-5 h-5" />
			</Button>
			<Button
				type="button"
				onclick={() => handlePeticion(row)}
				pill
				color="light"
				outline
				class="p-1!"
				size="sm"
			>
				<ReceiptOutline class="w-5 h-5" />
			</Button>
		</div>
	{/snippet}

	<DataTable data={estudiantes} {actions} />

	<Modal bind:open={mostrarFormulario} size="md">
		<h3 class="font-semibold mb-3 text-lg" slot="header">
			Asignación de Notas {esPeticion ? '(Petición)' : ''}
		</h3>

		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<Input placeholder="Estudiante" value={estudianteSeleccionado?.cedula} disabled />

			<Select
				bind:value={corte}
				placeholder="Corte"
				items={esPeticion
					? []
					: data.materia.materia.estudiantes[0].notas
							.filter((nota) => (esPeticion ? nota !== 0 : true))
							.map((_, i) => ({
								value: i + 1,
								name: 'Nota ' + (i + 1)
							}))}
			></Select>

			<input
				type="number"
				placeholder="Nota"
				bind:value={nota}
				min={0}
				max={20}
				use:imask={notaMask as any}
				step={0.01}
				class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 pl-10"
			/>
			{#if esPeticion}
				<Textarea class="md:col-span-3" placeholder="Motivo de la petición" />
			{/if}
		</div>

		<div class="w-full flex justify-end items-center gap-2" slot="footer">
			<Button color="red" on:click={() => (mostrarFormulario = false)}>Cancelar</Button>
			<Button
				on:click={() => {
					if (corte && nota !== '') {
						estudianteSeleccionado.notas[corte] = Number(nota);
						mostrarFormulario = false;
					}
				}}>Editar</Button
			>
		</div>
	</Modal>
</div>
