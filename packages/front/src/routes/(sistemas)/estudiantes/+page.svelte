<script lang="ts">
	import { cedulaMask, DataTable, maxYearDate, nota, ConfirmDeleteModal } from '$lib';
	import { imask } from '@imask/svelte';
	import {
		Button,
		Checkbox,
		Input,
		Label,
		Modal,
		Select,
		TableSearch,
		Textarea,
		Datepicker,

		Tooltip

	} from 'flowbite-svelte';
	import { EyeOutline, FileCopyOutline, PenOutline, PlusOutline, TrashBinOutline } from 'flowbite-svelte-icons';
	import type { Estudiante } from '../../../app';
	import { resolver } from '$lib/utilidades/resolver';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { enhance } from '$app/forms';
	import ToastContainer from '$lib/componentes/ToastContainer.svelte';

	// Datos de la página
	let { data } = $props();

	// Estado para el modal
	let modalVisible = $state(false);
	let isEditing = $state(false);
	let searchTerm = $state('');
	let formEl: HTMLFormElement | undefined = $state();
	// Estado para el modal de confirmación de eliminación
	let deleteModalOpen = $state(false);
	let selectedStudentForDelete: Estudiante | null = $state(null);
	let estudianteActual: Partial<{
		id: number;
		cedula: string;
		nombre: string;
		correo: string;
		activo: boolean;
		semestre: number;
		carrera: number;
		promedio: number;
		direccion: string;
		fecha_nac: Date;
		sexo: 'M' | 'F' | '';
		usuario?: {
			id: number;
		};
	}> = $state({});

	$effect(() => {
		if (!modalVisible) {
			estudianteActual = {};
		}
	});

	$effect(() => {
		if (data.estudiantes) {
			estudiantesFiltrados =
				data?.estudiantes.filter(
					(est) =>
						est?.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est?.cedula?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est?.correo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est.direccion.toLowerCase().includes(searchTerm.toLowerCase())
				) ?? [];
		}
	});

	let estudiantes: Estudiante[] = $state(data.estudiantes);
	let estudiantesFiltrados = $derived(
		estudiantes.filter(
			(est) =>
				est?.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est?.cedula?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est?.correo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est.direccion.toLowerCase().includes(searchTerm.toLowerCase())
		) ?? []
	);

	// Función para abrir el modal en modo edición
	function editarEstudiante(estudiante: any) {
		estudianteActual = {
			...estudiante,
			carrera: data.carreras.find((car) => car.nombre === estudiante.carrera)?.id,
			fecha_nac: new Date(estudiante.fecha_nacimiento),
			fecha_nacimiento: undefined
		};
		isEditing = true;
		modalVisible = true;
	}

	// Función para abrir el modal en modo creación
	function crearEstudiante() {
		estudianteActual = {
			id: 0,
			cedula: '',
			nombre: '',
			correo: '',
			activo: true,
			semestre: 1,
			carrera: 1,
			promedio: 0,
			direccion: '',
			fecha_nac: maxYearDate(),
			sexo: 'M'
		};
		isEditing = false;
		modalVisible = true;
	}

	function calcularEdad(fechaNacimiento: Date | null = null): number {
		if (!fechaNacimiento) return 0;

		const hoy = new Date();
		const nacimiento = fechaNacimiento;

		let edad = hoy.getFullYear() - nacimiento.getFullYear();
		const mes = hoy.getMonth() - nacimiento.getMonth();

		if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
			edad--;
		}

		return edad;
	}

	// Actualizar edad cuando cambia la fecha de nacimiento
	let edad = $derived(calcularEdad(estudianteActual!.fecha_nac));

	// Función para abrir el modal de eliminación
	function confirmarEliminarEstudiante(estudiante: Estudiante) {
		selectedStudentForDelete = estudiante;
		deleteModalOpen = true;
	}

	const handleSubmit: SubmitFunction = () => {
		return resolver(() => {
			if (isEditing) {
				modalVisible = false;
			}
		});
	};
</script>

<div class="w-full">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Estudiantes</h1>
		{#if data.rol !== 'coordinador' && data.rol !== 'caja'}
			<Button color="blue" onclick={crearEstudiante}>
				<PlusOutline class="mr-2 h-5 w-5" />
				Registrar
			</Button>
		{/if}
	</div>

	<div class="mb-4">
		<TableSearch bind:inputValue={searchTerm} placeholder="Buscar por nombre, cédula o correo..." />
	</div>

	{#snippet actions(row: Estudiante)}
		<div class="flex gap-2">
			{#if data.rol !== 'coordinador' && data.rol !== 'caja'}
				<Button pill size="xs" class="p-1.5!" color="light" onclick={() => editarEstudiante(row)}>
					<PenOutline class="w-5 h-5" />
				</Button>
				<Button
					pill
					class="p-1.5!"
					size="xs"
					color="red"
					onclick={() => confirmarEliminarEstudiante(row)}
				>
					<TrashBinOutline class="w-5 h-5" />
				</Button>
			{/if}
			<Button pill size="xs" class="p-1.5!" color="blue" onclick={() => navigator.clipboard.writeText(row.cedula)}>
				<FileCopyOutline class="w-5 h-5" />
			</Button>
			<Tooltip placement="top">Copiar cédula</Tooltip>
		</div>
	{/snippet}
	<DataTable data={estudiantesFiltrados} {actions}></DataTable>

	<Modal
		title={isEditing ? 'Editar Estudiante' : 'Nuevo Estudiante'}
		bind:open={modalVisible}
		size="xl"
	>
		<form
			action={isEditing ? '?/edit' : '?/create'}
			method="POST"
			use:enhance={handleSubmit}
			bind:this={formEl}
		>
			{#if isEditing}
				<input type="hidden" name="id_estudiante" value={estudianteActual!.id} />
				<input type="hidden" name="id" value={estudianteActual!.usuario?.id} />
			{/if}

			<div class="grid grid-cols-1 md:grid-cols-6 gap-4 mb-4">
				<div class="md:col-span-2">
					<Label for="cedula" class="mb-2">Cédula</Label>
					<input
						id="cedula"
						name="cedula"
						placeholder="Ingrese la cédula"
						value={estudianteActual?.cedula || ''}
						oninput={(e) => {
							if (estudianteActual) estudianteActual.cedula = e.currentTarget.value;
						}}
						required
						use:imask={cedulaMask as any}
						class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="nombre" class="mb-2">Nombre Completo</Label>
					<Input
						id="nombre"
						name="nombre"
						placeholder="Ingrese el nombre completo"
						value={estudianteActual!.nombre}
						required
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="fecha_nac" class="mb-2">Fecha de Nacimiento</Label>
					<Datepicker
						availableTo={maxYearDate()}
						placeholder="Seleccione una fecha"
						bind:value={estudianteActual.fecha_nac}
						translationLocale="es-VE"
						locale="fr-FR"
						dateFormat={{ year: 'numeric', month: '2-digit', day: '2-digit' }}
					/>
					<input
						type="hidden"
						name="fecha_nac"
						value={estudianteActual.fecha_nac?.toISOString().split('T')[0] ?? ''}
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="correo" class="mb-2">Correo Electrónico</Label>
					<Input
						id="correo"
						name="correo"
						type="email"
						placeholder="correo@ejemplo.com"
						value={estudianteActual?.correo}
						required
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="carrera" class="mb-2">Carrera</Label>
					<Select
						id="carrera"
						name="carrera"
						value={estudianteActual?.carrera}
						required
						items={data.carreras.map((carrera) => ({
							value: carrera.id,
							name: carrera.nombre
						}))}
					/>
				</div>
				<div>
					<Label for="sexo" class="mb-2">Sexo</Label>
					<Select
						id="sexo"
						name="sexo"
						value={estudianteActual?.sexo}
						placeholder=""
						required
						items={[
							{ value: 'M', name: 'Masculino' },
							{ value: 'F', name: 'Femenino' }
						]}
					/>
				</div>
				<div>
					<Label for="semestre" class="mb-2">Semestre</Label>
					<Select
						id="semestre"
						name="semestre"
						value={estudianteActual?.semestre}
						placeholder=""
						required
						items={Array(10)
							.fill(null)
							.map((_, i) => ({ value: i + 1, name: `${i + 1}° Semestre` }))}
					/>
				</div>
				<div>
					<Label for="promedio" class="mb-2">Promedio</Label>
					<input
						id="promedio"
						name="promedio"
						type="number"
						class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
						use:imask={nota}
						value={estudianteActual?.promedio}
						required
					/>
				</div>
				<div>
					<Label for="edad" class="mb-2">Edad</Label>
					<Input id="edad" name="edad" type="number" value={edad} readonly />
				</div>
				<div class={!isEditing ? 'md:col-span-5' : 'md:col-span-4 row-span-2'}>
					<Label for="direccion" class="mb-2">Dirección</Label>
					<Textarea
						id="direccion"
						name="direccion"
						placeholder="Ingrese la dirección completa"
						value={estudianteActual?.direccion}
						rows={3}
					/>
				</div>
				{#if isEditing}
					<div class="flex items-center">
						<Checkbox id="activo" name="activo" checked={estudianteActual?.activo} />
						<Label for="activo" class="ml-2">Usuario Activo</Label>
					</div>
				{/if}
			</div>
		</form>
		{#snippet footer()}
			<div class="flex justify-between items-center w-full">
				<div>
					<Button type="button" color="alternative" onclick={() => (modalVisible = false)}
						>Cancelar</Button
					>
					<Button type="submit" color="primary" onclick={() => formEl && formEl.requestSubmit()}
						>{isEditing ? 'Actualizar' : 'Guardar'}</Button
					>
				</div>
				<ToastContainer />
			</div>
		{/snippet}
	</Modal>

	<!-- Modal de confirmación de eliminación -->
	<ConfirmDeleteModal
		bind:open={deleteModalOpen}
		title="Eliminar Estudiante"
		message="¿Estás seguro de que deseas eliminar al estudiante {selectedStudentForDelete?.nombre}? Esta acción no se puede deshacer."
		action="?/delete"
		formData={{ cedula: selectedStudentForDelete?.cedula || '' }}
		onSuccess={() => {
			selectedStudentForDelete = null;
		}}
	/>
</div>
