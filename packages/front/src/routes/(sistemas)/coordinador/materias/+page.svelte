<script lang="ts">
	import { enhance } from '$app/forms';
	import { resolver } from '$lib/utilidades/resolver';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { Button, Input, Label, Modal, MultiSelect, Select, Tooltip } from 'flowbite-svelte';
	import ToastContainer from '$lib/componentes/ToastContainer.svelte';
	import {
		CalendarMonthOutline,
		CogOutline,
		EyeOutline,
		EyeSlashOutline,
		PenOutline,
		PlusOutline,
		TrashBinOutline
	} from 'flowbite-svelte-icons';
	import type { Asignacion, Horario, Materia } from '../../../app';
	import type { PageData } from './$types';
	import type { AsignacionReq } from '$lib/types';

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
		asignaciones: AsignacionReq[];
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
		asignaciones: [],
		activo: true
	});

	let formEl: HTMLFormElement;
	let { data }: { data: PageData } = $props();
	let showModal = $state(false);
	let showSeccionesModal = $state(false);
	let editMode = $state(false);
	let filtroSemestre = $state(1);
	let materiaParaSecciones: Materia | null = $state(null);
	let toggleOutForm: HTMLFormElement | null = $state(null);

	// Opciones de prelación calculadas dinámicamente
	let opcionesPrelacion: { value: string; name: string }[] = $state([]);

	function openModal(materia: Materia | null = null) {
		if (materia) {
			form = {
				...materia,
				id_carrera: materia.id_carrera.toString(),
				asignaciones: materia.asignaciones.map(asig => ({
					id: asig.id,
					nombre: asig.nombre,
					profesor_id: asig.profesor?.id,
					horarios: asig.horarios
				})),
				prelacion: materia.prelacion ? materia.prelacion.split(',').map((p) => p.trim()) : []
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
				asignaciones: [],
				activo: true
			};
			editMode = false;
		}
		showModal = true;
	}

	function openSeccionesModal(materia: Materia) {
		materiaParaSecciones = materia;
		form = {
			...materia,
			id_carrera: materia.id_carrera.toString(),
			asignaciones: materia.asignaciones.map(asig => ({
				id: asig.id,
				nombre: asig.nombre,
				profesor_id: asig.profesor?.id,
				horarios: asig.horarios
			})),
			prelacion: materia.prelacion ? materia.prelacion.split(',').map((p) => p.trim()) : []
		};
		showSeccionesModal = true;
	}

	function addAsignacion() {
		form.asignaciones.push({
			nombre: '',
			profesor_id: undefined,
			horarios: []
		});
	}

	function removeAsignacion(index: number) {
		form.asignaciones.splice(index, 1);
	}

	function addHorarioToAsignacion(asignacionIndex: number) {
		form.asignaciones[asignacionIndex].horarios.push({
			dia: 'Lunes',
			hora_inicio: '08:00',
			hora_fin: '10:00'
		});
	}

	function removeHorarioFromAsignacion(asignacionIndex: number, horarioIndex: number) {
		form.asignaciones[asignacionIndex].horarios.splice(horarioIndex, 1);
	}

	const toggleMateriaStatus: SubmitFunction = () => {
		return resolver(() => {
			// Form will be reloaded automatically
		});
	};

	const handleSubmit: SubmitFunction = () => {
		return resolver(() => (showModal = false));
	};

	const handleSeccionesSubmit: SubmitFunction = () => {
		return resolver(() => (showSeccionesModal = false));
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
		<h1 class="text-2xl font-bold">Gestión de Materias</h1>
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
			Materias del semestre {filtroSemestre}: {data.materias.filter(m => m.semestre === filtroSemestre).length}
		</p>
	</div>

	<!-- Lista de materias con secciones -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
		{#each data.materias.filter((m) => m.semestre === filtroSemestre) as materia}
			<div class="bg-white rounded-lg shadow p-4 border {!materia.activo ? 'opacity-50' : ''}">
				<div class="flex justify-between items-start mb-3">
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
								color="blue"
								onclick={() => openSeccionesModal(materia)}
							>
								<CogOutline class="w-4 h-4" />
							</Button>
							<Tooltip placement="top">Configurar Secciones</Tooltip>
						</div>
						<div class="relative">
							<Button
								pill
								class="p-2!"
								size="xs"
								color={materia.activo ? 'red' : 'green'}
								onclick={() => toggleOutForm?.requestSubmit()}
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
							<form use:enhance={toggleMateriaStatus} action="?/toggleStatus" method="POST" bind:this={toggleOutForm}>
								<input type="hidden" name="id" value={materia.id} />
							</form>
						</div>
					</div>
				</div>
				
				<!-- Secciones -->
				<div class="border-t pt-3">
					<p class="text-sm font-medium text-gray-700 mb-2">Secciones configuradas:</p>
					{#if materia.asignaciones && materia.asignaciones.length > 0}
						{#each materia.asignaciones as asignacion}
							<div class="bg-gray-50 rounded p-2 mb-2">
								<div class="flex justify-between items-start">
									<div>
										<p class="text-sm font-medium">{asignacion.nombre}</p>
										{#if asignacion.profesor}
											<p class="text-xs text-gray-600">Prof: {asignacion.profesor.nombre}</p>
										{/if}
									</div>
									<div class="text-xs text-gray-500">
										{asignacion.horarios.length} horario(s)
									</div>
								</div>
							</div>
						{/each}
					{:else}
						<p class="text-sm text-gray-500 italic">Sin secciones configuradas</p>
					{/if}
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
					items={data.carreras.map((c) => ({ value: c.id.toString(), name: c.nombre }))}
					placeholder="Seleccione"
				></Select>
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
					class="multiselect"
					options={opcionesPrelacion}
					placeholder="Seleccione materias"
				/>
			</div>
		</div>
		
		<!-- Hidden input for asignaciones -->
		<input type="hidden" name="asignaciones" value={JSON.stringify(form.asignaciones)} />
		<input type="hidden" name="prelacion" value={form.prelacion.join(',')} />

		<div class="flex justify-end gap-2 mt-4">
			<Button color="red" onclick={() => (showModal = false)}>Cancelar</Button>
			<Button type="submit">{editMode ? 'Actualizar' : 'Crear'}</Button>
		</div>
	</form>
</Modal>

<!-- Modal de configuración de secciones -->
<Modal bind:open={showSeccionesModal} size="xl">
	{#snippet header()}
		<div class="flex justify-between items-center w-full">
			<span>Configurar Secciones - {materiaParaSecciones?.nombre}</span>
		</div>
	{/snippet}
	<form
		method="POST"
		use:enhance={handleSeccionesSubmit}
		action="?/edit"
	>
		<input type="hidden" name="id" value={form.id} />
		<input type="hidden" name="nombre" value={form.nombre} />
		<input type="hidden" name="prelacion" value={form.prelacion.join(',')} />
		<input type="hidden" name="unidad_credito" value={form.unidad_credito} />
		<input type="hidden" name="hp" value={form.hp} />
		<input type="hidden" name="ht" value={form.ht} />
		<input type="hidden" name="semestre" value={form.semestre} />
		<input type="hidden" name="id_carrera" value={form.id_carrera} />
		<input type="hidden" name="ciclo" value={form.ciclo} />
		<input type="hidden" name="maximo" value={form.maximo} />
		
		<div class="space-y-4">
			<div class="flex justify-between items-center">
				<h3 class="text-lg font-medium">Asignaciones</h3>
				<Button onclick={addAsignacion} color="blue" size="sm">
					<PlusOutline class="w-4 h-4 mr-2" />
					Agregar Sección
				</Button>
			</div>
			
			{#each form.asignaciones as asignacion, i}
				<div class="border rounded-lg p-4 bg-gray-50">
					<div class="flex justify-between items-start mb-3">
						<h4 class="font-medium">Sección {i + 1}</h4>
						<Button onclick={() => removeAsignacion(i)} color="red" size="xs">
							<TrashBinOutline class="w-4 h-4" />
						</Button>
					</div>
					
					<div class="grid grid-cols-2 gap-4 mb-4">
						<div>
							<Label for={`nombre_${i}`} class="mb-2">Nombre de la sección</Label>
							<Input
								id={`nombre_${i}`}
								bind:value={asignacion.nombre}
								placeholder="ej: MA, MB, MC"
								class="input"
							/>
						</div>
						<div>
							<Label for={`profesor_${i}`} class="mb-2">Profesor</Label>
							<Select
								id={`profesor_${i}`}
								bind:value={asignacion.profesor_id}
								items={data.docentes.map((d) => ({ value: d.id, name: d.nombre }))}
								placeholder="Seleccione profesor"
								class="select"
							/>
						</div>
					</div>
					
					<!-- Horarios para esta asignación -->
					<div>
						<div class="flex justify-between items-center mb-2">
							<Label class="text-sm">Horarios</Label>
							<Button onclick={() => addHorarioToAsignacion(i)} color="green" size="xs">
								<PlusOutline class="w-3 h-3 mr-1" />
								Agregar Horario
							</Button>
						</div>
						
						{#each asignacion.horarios as horario, j}
							<div class="grid grid-cols-4 gap-2 mb-2 items-end">
								<div>
									<Label for={`dia_${i}_${j}`} class="text-xs">Día</Label>
									<Select
										id={`dia_${i}_${j}`}
										bind:value={horario.dia}
										items={dias.map(d => ({ value: d, name: d }))}
										class="select"
									/>
								</div>
								<div>
									<Label for={`inicio_${i}_${j}`} class="text-xs">Hora inicio</Label>
									<Input
										id={`inicio_${i}_${j}`}
										type="time"
										bind:value={horario.hora_inicio}
										class="input"
									/>
								</div>
								<div>
									<Label for={`fin_${i}_${j}`} class="text-xs">Hora fin</Label>
									<Input
										id={`fin_${i}_${j}`}
										type="time"
										bind:value={horario.hora_fin}
										class="input"
									/>
								</div>
								<div>
									<Button onclick={() => removeHorarioFromAsignacion(i, j)} color="red" size="xs">
										<TrashBinOutline class="w-3 h-3" />
									</Button>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/each}
		</div>
		
		<input type="hidden" name="asignaciones" value={JSON.stringify(form.asignaciones)} />

		<div class="flex justify-end gap-2 mt-6">
			<Button color="red" onclick={() => (showSeccionesModal = false)}>Cancelar</Button>
			<Button type="submit" color="blue">Guardar Secciones</Button>
		</div>
	</form>
</Modal>

<ToastContainer />
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
				{#if editMode}
					<Button
						color={form.activo ? 'red' : 'green'}
						onclick={() => {
							const materia = data.materias.find((m) => m.id === form.id);
							if (materia) {
								toggleForm.requestSubmit();
								showModal = false;
							}
						}}
					>
					{form.activo ? 'Inactivar' : 'Activar'}
				</Button>
				<form use:enhance={toggleMateriaStatus} action="?/toggleStatus" method="POST" class="hidden" bind:this={toggleForm}>
					<input type="hidden" name="id" bind:value={form.id} />
					<input type="hidden" name="activo" value={form.activo.toString()} />
				</form>
				<Button color="light" onclick={() => goto(`/materias/${form.id}`)}>Ver notas</Button>
				{/if}
			</div>
			<ToastContainer />
		</div>
	{/snippet}
</Modal>
