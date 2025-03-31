<script lang="ts">
	import { enhance } from '$app/forms';
	import { cedulaMask, DataTable, Datepicker, maxYearDate, nota } from '$lib';
	import { imask } from '@imask/svelte';
	import {
		Alert,
		Button,
		ButtonGroup,
		Checkbox,
		Helper,
		Input,
		Label,
		Modal,
		Select,
		TabItem,
		TableSearch,
		Tabs,
		Textarea
	} from 'flowbite-svelte';
	import {
		CheckCircleOutline,
		ExclamationCircleOutline,
		PenOutline,
		PlusOutline,
		TrashBinOutline
	} from 'flowbite-svelte-icons';
	import type { ActionData, PageData } from './$types';
	import type { Carrera } from '../../../../app';

	// Datos de la página
	let { data, form }: { data: PageData; form: ActionData } = $props<{
		data: PageData;
		form: ActionData;
	}>();

	// Estado para el modal
	let modalVisible = $state(false);
	let isEditing = $state(false);
	let searchTerm = $state('');
	let currentPage = 1;
	const pageSize = 10;
	let estudianteActual: any = $state({});
	let showAlert = $state(false);
	let alertMessage = $state('');
	let alertType: 'success' | 'error' = $state('success');

	// Función para mostrar alerta
	function mostrarAlerta(mensaje: string, tipo: 'success' | 'error') {
		alertMessage = mensaje;
		alertType = tipo;
		showAlert = true;
		setTimeout(() => {
			showAlert = false;
		}, 5000);
	}

	// Procesar respuesta del formulario
	$effect(() => {
		if (form) {
			if ((form as any).success) {
				modalVisible = false;
				mostrarAlerta((form as any).message, 'success');
			} else if ((form as any).error) {
				mostrarAlerta((form as any).error, 'error');
			}
		}
	});

  $effect(() => {
    if (!modalVisible) {
      estudianteActual = {};
    }
  })

	// Filtrar estudiantes por término de búsqueda
	let carrerasFiltradas = $derived(
		data.carreras.filter(
			(car) =>
				car.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
				car.id.toString().toLowerCase().includes(searchTerm.toLowerCase())
		)
	);

	// Función para abrir el modal en modo edición
	function editarEstudiante(estudiante: any) {
		estudianteActual = { ...estudiante };
		if (typeof estudianteActual.carrera === 'object') {
			estudianteActual.carrera = estudianteActual.carrera.id;
		}
		isEditing = true;
		modalVisible = true;
	}

	// Función para abrir el modal en modo creación
	function crearEstudiante() {
		estudianteActual = {
			cedula: '',
			nombre: '',
			correo: '',
			activo: true,
			semestre: 1,
			carrera: 1,
			promedio: 0,
			direccion: '',
			fecha_nac: '',
			sexo: 'M'
		};
		isEditing = false;
		modalVisible = true;
	}

	// Función para eliminar un estudiante
	function eliminarEstudiante(estudiante: any) {
		fetch(`/api/estudiantes/${estudiante.id}`, {
			method: 'DELETE'
		})
			.then((response) => {
				if (response.ok) {
					mostrarAlerta('Estudiante eliminado exitosamente', 'success');
				} else {
					mostrarAlerta('Error al eliminar el estudiante', 'error');
				}
			})
			.catch((error) => {});
	}
</script>

<div class="w-full">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Carreras</h1>
		<Button color="blue" on:click={crearEstudiante}>
			<PlusOutline class="mr-2 h-5 w-5" />
			Crear carrera
		</Button>
	</div>

	<!-- Alertas -->
	{#if showAlert}
		<Alert
			color={alertType === 'success' ? 'green' : 'red'}
			dismissable
			bind:open={showAlert}
			class="mb-4"
		>
			<svelte:fragment slot="icon">
				{#if alertType === 'success'}
					<CheckCircleOutline class="h-5 w-5" />
				{:else}
					<ExclamationCircleOutline class="h-5 w-5" />
				{/if}
			</svelte:fragment>
			{alertMessage}
		</Alert>
	{/if}

	<div class="mb-4">
		<TableSearch bind:inputValue={searchTerm} placeholder="Buscar por nombre, cédula o correo..." />
	</div>

	<div class="overflow-x-auto">
		<div class="w-max min-w-full">
			{#snippet actions(row: Carrera)}
				<div class="flex gap-2">
					<Button size="xs" color="light" on:click={() => editarEstudiante(row)}>
						<PenOutline class="w-4 h-4" />
					</Button>
					<Button size="xs" color="red" on:click={() => eliminarEstudiante(row)}>
						<TrashBinOutline class="w-4 h-4" />
					</Button>
				</div>
			{/snippet}
			<DataTable data={carrerasFiltradas} {actions}></DataTable>
		</div>
	</div>

	<Modal title={isEditing ? 'Editar Carrera' : 'Nueva Carrera'} bind:open={modalVisible} size="xs">
		<form
			action={isEditing ? '?/edit' : '?/create'}
			method="POST"
			use:enhance={() => {
				return async ({ result }) => {
					if (result.type === 'success') {
						modalVisible = false;
						mostrarAlerta(
							isEditing ? 'Estudiante actualizado exitosamente' : 'Estudiante creado exitosamente',
							'success'
						);
					}
				};
			}}
		>
			{#if isEditing}
				<input type="hidden" name="id" value={estudianteActual.id} />
			{/if}
			<div class="mb-4 w-full">
				<div>
					<Label for="nombre" class="mb-2">Nombre</Label>
					<ButtonGroup class="w-full">
						<Input
							id="nombre"
							name="nombre"
							placeholder="Informática"
							value={estudianteActual.nombre}
							required
							color={form?.errores?.nombre ? 'red' : undefined}
						/>
						{#if form?.errores?.nombre}
							<Helper class="mt-2" color="red">{form?.errores.nombre}</Helper>
						{/if}
						<Button type="submit">Guardar</Button>
					</ButtonGroup>
				</div>
			</div>
		</form>
	</Modal>
</div>
