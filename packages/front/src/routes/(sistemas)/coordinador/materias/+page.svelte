<script lang="ts">
	import { enhance } from '$app/forms';
	import { GrillaHorario } from '$lib/componentes';
	import { resolver } from '$lib/utilidades/resolver';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { Button, Input, Label, Modal, MultiSelect, Select, Tooltip } from 'flowbite-svelte';
	import ToastContainer from '$lib/componentes/ToastContainer.svelte';
	import {
		CalendarMonthOutline,
		EyeOutline,
		EyeSlashOutline,
		PenOutline,
		PlusOutline
	} from 'flowbite-svelte-icons';
	import type { Horario, Materia } from '../../../app';
	import type { PageData } from './$types';

	interface Form {
		id: string;
		nombre: string;
		prelacion: (string | number)[];
		unidad_credito: number;
		hp: number;
		ht: number;
		semestre: number;
		id_carrera: string;
		ciclo: string;
		maximo: number;
		id_docente: string;
		horarios: Horario[];
		activo: boolean;
	}

	const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

	let form: Form = $state({
		id: '',
		nombre: '',
		prelacion: [],
		unidad_credito: 0,
		hp: 0,
		ht: 0,
		semestre: 1,
		id_carrera: '',
		ciclo: '',
		maximo: 0,
		id_docente: '',
		horarios: [],
		activo: true
	});

	let formEl: HTMLFormElement;
	let { data }: { data: PageData } = $props();
	let showModal = $state(false);
	let editMode = $state(false);
	let filtroSemestre = $state(1);
	let selectedMateria: Materia | null = $state(null);

	// Opciones de prelación calculadas dinámicamente
	let opcionesPrelacion: { value: string; name: string }[] = $state([]);

	// Filter materias by semester
	const materiasFiltradas = $derived(
		data.materias
			.filter(mat => mat.semestre === filtroSemestre)
			.map(mat => ({
				id: mat.id,
				nombre: mat.nombre,
				dia: mat.horarios[0]?.dia || 'Lunes',
				hora_inicio: mat.horarios[0]?.hora_inicio || '08:00',
				hora_fin: mat.horarios[0]?.hora_fin || '10:00',
				color: mat.activo === false ? 'gray' : undefined,
				conflicto: false,
				activo: mat.activo
			}))
	);

	function openModal(materia: Materia | null = null) {
		if (materia) {
			form = { 
				...materia, 
				id_carrera: materia.id_carrera.toString(),
				id_docente: materia.id_docente.toString(),
				prelacion: materia.prelacion ? materia.prelacion.split(',').map(p => p.trim()) : []
			};
			editMode = true;
		} else {
			form = {
				id: '',
				nombre: '',
				prelacion: [],
				unidad_credito: 0,
				hp: 0,
				ht: 0,
				semestre: filtroSemestre,
				id_carrera: '',
				ciclo: '',
				maximo: 30,
				id_docente: '',
				horarios: [],
				activo: true
			};
			editMode = false;
		}
		showModal = true;
	}

	function addHorario() {
		form.horarios.push({ dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00' });
	}

	function removeHorario(index: number) {
		form.horarios.splice(index, 1);
	}

	function handleMateriaDoubleClick(materia: any) {
		const fullMateria = data.materias.find(m => m.id === materia.id);
		if (fullMateria) {
			openModal(fullMateria);
		}
	}

	function toggleMateriaStatus(materia: Materia) {
		selectedMateria = materia;
		// Create a form element and submit it
		const formData = new FormData();
		formData.set('id', materia.id);
		formData.set('activo', materia.activo.toString());
		
		fetch('?/toggleStatus', {
			method: 'POST',
			body: formData
		}).then(response => {
			if (response.ok) {
				window.location.reload();
			}
		});
	}

	const handleSubmit: SubmitFunction = () => {
		return resolver(() => (showModal = false));
	};

	$effect(() => {
		if (form.semestre === 1) {
			opcionesPrelacion = [];
		} else {
			opcionesPrelacion = data.materias
				.filter(
					(m) => m.id_carrera == form.id_carrera && m.semestre < form.semestre && m.id !== form.id
				)
				.map((m) => ({ value: m.id, name: m.nombre }));
		}
	});
</script>

<div class="container mx-auto p-4">
	<div class="flex justify-between items-center mb-4">
		<h1 class="text-2xl font-bold">Gestión de Materias por Coordinador</h1>
		<div class="flex gap-2 items-center">
			<div class="flex items-center gap-2">
				<Label for="semestre">Semestre:</Label>
				<Select
					id="semestre"
					bind:value={filtroSemestre}
					items={Array(10)
						.fill(null)
						.map((_, i) => ({ value: i + 1, name: `${i + 1}°` }))}
					class="min-w-[100px]"
				/>
			</div>
			<Button onclick={() => openModal()} class="btn btn-primary">
				<PlusOutline class="h-5 w-5 mr-2" />
				Crear Materia
			</Button>
		</div>
	</div>

	<div class="mb-4">
		<p class="text-sm text-gray-600">
			Materias del semestre {filtroSemestre}: {materiasFiltradas.length} 
			| Haga doble clic en una materia para editarla
		</p>
	</div>

	<!-- Enhanced GrillaHorario with double-click functionality -->
	<div class="relative">
		<GrillaHorario 
			materias={materiasFiltradas} 
			docente={false}
			onMateriaDoubleClick={handleMateriaDoubleClick}
		/>
	</div>

	<!-- Action buttons for quick access -->
	<div class="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
		{#each data.materias.filter(m => m.semestre === filtroSemestre) as materia}
			<div class="bg-white rounded-lg shadow p-4 border {!materia.activo ? 'opacity-50' : ''}">
				<div class="flex justify-between items-start">
					<div class="flex-1">
						<h3 class="font-medium text-gray-900">{materia.nombre}</h3>
						<p class="text-sm text-gray-500">Código: {materia.id}</p>
						<p class="text-sm text-gray-500">
							Estado: {materia.activo ? 'Activa' : 'Inactiva'}
						</p>
					</div>
					<div class="flex gap-1">
						<div class="relative">
							<Button 
								pill 
								class="p-2!" 
								size="xs" 
								color="primary" 
								onclick={() => openModal(materia)}
							>
								<PenOutline class="w-4 h-4" />
							</Button>
							<Tooltip placement="top">Editar</Tooltip>
						</div>
						<div class="relative">
							<Button 
								pill 
								class="p-2!" 
								size="xs" 
								color={materia.activo ? 'red' : 'green'}
								onclick={() => toggleMateriaStatus(materia)}
							>
								{#if materia.activo}
									<EyeSlashOutline class="w-4 h-4" />
								{:else}
									<EyeOutline class="w-4 h-4" />
								{/if}
							</Button>
							<Tooltip placement="top">
								{materia.activo ? 'Inactivar' : 'Activar'}
							</Tooltip>
						</div>
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>

<!-- Modal de creación/edición -->
<Modal bind:open={showModal} size="lg">
	{#snippet header()}
		<div class="flex justify-between items-center w-full">
			<span>{editMode ? 'Editar Materia' : 'Crear Materia'}</span>
			{#if editMode}
				<Button 
					color={form.activo ? 'red' : 'green'}
					size="sm"
					onclick={() => {
						const materia = data.materias.find(m => m.id === form.id);
						if (materia) {
							toggleMateriaStatus(materia);
							showModal = false;
						}
					}}
				>
					{form.activo ? 'Inactivar' : 'Activar'}
				</Button>
			{/if}
		</div>
	{/snippet}
	<form
		method="POST"
		use:enhance={handleSubmit}
		bind:this={formEl}
		action={editMode ? `?/edit` : '?/create'}
	>
		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-2">
				<Label for="id" class="mb-2">Código</Label>
				<Input id="id" name="id" bind:value={form.id} class="input" required readonly={editMode} />
			</div>
			<div class="col-span-2">
				<Label for="nombre" class="mb-2">Nombre</Label>
				<Input name="nombre" bind:value={form.nombre} class="input" required />
			</div>
			<div>
				<Label for="unidad_credito" class="mb-2">Unidades de crédito</Label>
				<Input
					id="unidad_credito"
					name="unidad_credito"
					type="number"
					bind:value={form.unidad_credito}
					class="input"
					required
				/>
			</div>
			<div>
				<Label for="hp" class="mb-2">Horas prácticas</Label>
				<Input id="hp" name="hp" type="number" bind:value={form.hp} class="input" required />
			</div>
			<div>
				<Label for="ht" class="mb-2">Horas Teóricas</Label>
				<Input id="ht" name="ht" type="number" bind:value={form.ht} class="input" required />
			</div>
			<div>
				<Label for="semestre" class="mb-2">Semestre</Label>
				<Input
					id="semestre"
					name="semestre"
					type="number"
					bind:value={form.semestre}
					class="input"
					required
				/>
			</div>
			<div class="col-span-3">
				<Label for="id_carrera" class="mb-2">Carrera</Label>
				<Select
					id="id_carrera"
					name="id_carrera"
					bind:value={form.id_carrera}
					class="select"
					required
					items={data.carreras.map((c) => ({ value: c.id, name: c.nombre }))}
					placeholder="Seleccione"
				></Select>
				<Input type="hidden" name="id_carrera" bind:value={form.id_carrera} />
			</div>
			<div class="col-span-3">
				<Label for="id_docente" class="mb-2">Docente</Label>
				<Select
					id="id_docente"
					name="id_docente"
					placeholder="Seleccione"
					bind:value={form.id_docente}
					class="select"
					items={data.docentes.map((d) => ({ value: d.id, name: d.nombre }))}
				></Select>
				<input type="hidden" name="id_docente" bind:value={form.id_docente} />
			</div>
			<div>
				<Label for="maximo" class="mb-2">Máximo de estudiantes</Label>
				<Input id="maximo" name="maximo" type="number" bind:value={form.maximo} class="input" />
			</div>
			<div class="col-span-4">
				<Label for="prelacion" class="mb-2">Prelación</Label>
				<MultiSelect
					id="prelacion"
					dropdownClass="z-[99999]!"
					name="prelacion"
					bind:value={form.prelacion}
					items={opcionesPrelacion}
					placeholder="Seleccione las prelaciones"
				/>
			</div>
		</div>

		<div class="mt-4">
			<h2 class="font-bold mb-2">Horarios</h2>
			{#each form.horarios as h, i}
				<div class="flex gap-2 mb-2">
					<Select bind:value={h.dia} class="select min-w-[15%]" placeholder="Seleccionar">
						{#each dias as d}
							<option>{d}</option>
						{/each}
					</Select>
					<Input type="time" bind:value={h.hora_inicio} class="input" />
					<Input type="time" bind:value={h.hora_fin} class="input" />
					<Button type="button" color="red" size="sm" class="p-1" onclick={() => removeHorario(i)}
						>✕
					</Button>
				</div>
			{/each}
			<Button type="button" color="primary" outline size="sm" onclick={addHorario}>
				<PlusOutline class="h-5 w-5 mr-2" />
				Agregar Horario
			</Button>
			<input type="hidden" name="horarios" value={JSON.stringify(form.horarios)} />
		</div>
	</form>
	{#snippet footer()}
		<div class="flex justify-between items-center w-full">
			<div>
				<Button type="button" color="alternative" onclick={() => (showModal = false)}
					>Cancelar
				</Button>
				<Button type="submit" color="primary" onclick={() => formEl.requestSubmit()}
					>{editMode ? 'Actualizar' : 'Guardar'}</Button
				>
			</div>
			<ToastContainer />
		</div>
	{/snippet}
</Modal>