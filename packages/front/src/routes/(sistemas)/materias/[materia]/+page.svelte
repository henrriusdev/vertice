<script lang="ts">
	import { DataTable, Datepicker, nota as notaMask } from '$lib';
	import { Button, Input, Label, Modal, Select, Textarea } from 'flowbite-svelte';
	import { imask } from '@imask/svelte';
	import { FileLinesOutline, PenOutline, ReceiptOutline } from 'flowbite-svelte-icons';
	import type { Nota } from '../../../../app';
	import { enhance } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { onMount } from 'svelte';
	import { resolver } from '$lib/utilidades/resolver';

	let { data } = $props();

	let estudiantes = $derived(
		data.materia.materia.estudiantes.map((e) => ({
			...e,
			...e.notas.reduce((acc, n, i) => ({ ...acc, [`nota ${i + 1}`]: n }), {})
		}))
	);

	let estudianteSeleccionado: Nota | null = $state(null);
	let corte = $state('');
	let form: HTMLFormElement | undefined = $state();
	let nota = $state('');
	let motivo = $state('');
	let mostrarFormulario = $state(false);
	let esPeticion = $state(false);
	let formDrop: HTMLFormElement;
	let archivosDrop: FileList | null = $state(null);
	let dropVisible = $state(false);
	let dragCounter = 0;

	const handleEdit = (row: Nota) => {
		mostrarFormulario = true;
		console.log(row);
	};

	const handlePeticion = (row: Nota) => {
		mostrarFormulario = true;
		esPeticion = true;
		console.log(row);
	};

	const enviarCambioNotas: SubmitFunction = ({ formData }) => {
		formData.set('cedula_estudiante', estudianteSeleccionado?.cedula ?? '');
		formData.set('nombre_campo', corte);
		formData.set('valor', nota);
		formData.set('materia', data.materia.materia.id);
		formData.set('peticion', String(esPeticion));
		formData.set('observacion', motivo);

		return async ({ update }) => {
			await update();
			mostrarFormulario = false;
		};
	};

	const handleFileUpload: SubmitFunction = ({formData}) => {
		formData.set("folder", data.materia.materia.id)
		formData.set("ciclo", data.materia.ciclo)
		formData.set("file", archivosDrop[0], archivosDrop[0].name)
		return async ({ update }) => {
			await update();
			dropVisible = false;
		};
	};

	const handleSubmit: SubmitFunction = () => {
		return resolver();
	};


	$effect(() => {
		if (estudiantes.length) {
			estudianteSeleccionado = estudiantes[0];
		}
	});

	onMount(() => {
		const handleDragOver = (e: DragEvent) => {
			if (!mostrarFormulario) {
				e.preventDefault();
			}
		};

		const handleDragEnter = (e: DragEvent) => {
			if (!mostrarFormulario) {
				e.preventDefault();
				dragCounter++;
				dropVisible = true;
			}
		};

		const handleDragLeave = (e: DragEvent) => {
			if (!mostrarFormulario) {
				dragCounter--;
				if (dragCounter === 0) {
					dropVisible = false;
				}
			}
		};

		const handleDrop = (e: DragEvent) => {
			if (!mostrarFormulario) {
				e.preventDefault();
				dragCounter = 0;
				dropVisible = false;
				const file = e.dataTransfer?.files?.[0];
				if (file && formDrop) {
					const dt = new DataTransfer();
					dt.items.add(file);
					archivosDrop = dt.files;
					formDrop.requestSubmit();
				}
			}
		};

		window.addEventListener('dragenter', handleDragEnter);
		window.addEventListener('dragleave', handleDragLeave);
		window.addEventListener('dragover', handleDragOver);
		window.addEventListener('drop', handleDrop);

		return () => {
			window.removeEventListener('dragenter', handleDragEnter);
			window.removeEventListener('dragleave', handleDragLeave);
			window.removeEventListener('dragover', handleDragOver);
			window.removeEventListener('drop', handleDrop);
		};
	});

</script>

<div class="container mx-auto p-4">
	<div class="flex justify-between items-center mb-4">
		<h1 class="text-3xl font-bold">Notas de estudiantes en <span class="text-blue-600">{data.materia.materia.nombre}</span></h1>
		<form
			method="POST"
			action="?/notas"
			use:enhance={handleSubmit}
			class="space-y-6"
		>
			<Button color="primary" size="lg" class="w-full" type="submit">
				<FileLinesOutline class="mr-2 h-5 w-5" />
				Descargar Reporte
			</Button>
		</form>
	</div>
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
			{#if data.rol.toLowerCase() === 'docente'}
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
			{/if}
		</div>
	{/snippet}

	<!-- FORMULARIO OCULTO PARA SUBIR ARCHIVO -->
	<form
		bind:this={formDrop}
		use:enhance={handleFileUpload}
		method="post"
		enctype="multipart/form-data"
		class="hidden"
		action="?/subir"
	>
	</form>

	<Modal bind:open={dropVisible} size="lg">
		<h3 class="text-2xl font-bold py-60 text-center">ARRASTRA AQUÍ</h3>
	</Modal>

	<DataTable data={estudiantes} {actions} />

	<Modal bind:open={mostrarFormulario} size="md">
		<h3 class="font-semibold mb-3 text-lg" slot="header">
			Asignación de Notas {esPeticion ? '(Petición)' : ''}
		</h3>

		<form
			bind:this={form}
			use:enhance={enviarCambioNotas}
			method="post"
			action="?/editar"
			class="grid grid-cols-1 md:grid-cols-3 gap-4"
		>
			<Input placeholder="Estudiante" value={estudianteSeleccionado?.cedula} disabled />

			<Select
				bind:value={corte}
				placeholder="Corte"
				items={data.materia.materia.estudiantes[0].notas
							.map((n, i) => ({
								value: i + 1,
								nota: n,
								name: 'Nota ' + (i + 1)
							}))
							.filter((nota) =>
								esPeticion
									? nota.nota !== 0
									: data.rol.toLowerCase() === 'docente'
										? nota.nota === 0
										: true
							)}
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
				<Textarea class="md:col-span-3" placeholder="Motivo de la petición" bind:value={motivo} />
			{/if}
		</form>

		<div class="w-full flex justify-end items-center gap-2" slot="footer">
			<Button color="red" onclick={() => (mostrarFormulario = false)}>Cancelar</Button>
			<Button
				onclick={() => {
					if (corte && nota !== '') {
						form?.requestSubmit();
					}
				}}>Editar</Button
			>
		</div>
	</Modal>
</div>
