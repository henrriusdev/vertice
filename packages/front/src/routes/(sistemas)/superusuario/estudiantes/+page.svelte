<script lang="ts">
	import { enhance } from '$app/forms';
	import { cedulaMask, DataTable, Datepicker, maxYearDate, nota } from '$lib';
	import { imask } from '@imask/svelte';
	import {
		Alert,
		Button,
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
	import type { Estudiante } from '../../../../app';

	// Datos de la página
	export let data;
	export let form;

	// Estado para el modal
	let modalVisible = false;
	let isEditing = false;
	let searchTerm = '';
	let currentPage = 1;
	const pageSize = 10;
	let estudianteActual: any = {};
	let showAlert = false;
	let alertMessage = '';
	let alertType: 'success' | 'error' = 'success';

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
	$: if (form) {
		if (form.success) {
			modalVisible = false;
			mostrarAlerta(form.message, 'success');
		} else if (form.error) {
			mostrarAlerta(form.error, 'error');
		}
	}

	// Filtrar estudiantes por término de búsqueda
	$: estudiantesFiltrados = data.estudiantes.filter(
		(est: any) =>
			est.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
			est.cedula.toLowerCase().includes(searchTerm.toLowerCase()) ||
			est.correo.toLowerCase().includes(searchTerm.toLowerCase())
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

	// Calcular edad automáticamente al cambiar fecha de nacimiento
	function calcularEdad(fechaNacimiento: string): number {
		if (!fechaNacimiento) return 0;

		const hoy = new Date();
		const fechaNac = new Date(fechaNacimiento);
		let edad = hoy.getFullYear() - fechaNac.getFullYear();
		const mes = hoy.getMonth() - fechaNac.getMonth();

		if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())) {
			edad--;
		}

		return edad;
	}

	// Actualizar edad cuando cambia la fecha de nacimiento
	$: edad = calcularEdad(estudianteActual.fecha_nac);
</script>

<div class="w-full">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Estudiantes</h1>
		<Button color="blue" on:click={crearEstudiante}>
			<PlusOutline class="mr-2 h-5 w-5" />
			Nuevo Estudiante
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
			{#snippet actions(row: Estudiante)}
				<div class="flex gap-2">
					<Button size="xs" color="light" on:click={() => editarEstudiante(row)}>
						<PenOutline class="w-4 h-4" />
					</Button>
					<Button size="xs" color="red" on:click={() => eliminarEstudiante(row)}>
						<TrashBinOutline class="w-4 h-4" />
					</Button>
				</div>
			{/snippet}
			<DataTable
				data={estudiantesFiltrados}
				{actions}
			>
			</DataTable>
		</div>
	</div>

	<!-- Modal para crear/editar estudiante -->
	<Modal
		title={isEditing ? 'Editar Estudiante' : 'Nuevo Estudiante'}
		bind:open={modalVisible}
		size="xl"
	>
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

			<Tabs style="underline">
				<TabItem open title="Información de usuario">
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
						<div>
							<Label for="cedula" class="mb-2">Cédula</Label>
							<input
								id="cedula"
								name="cedula"
								placeholder="Ingrese la cédula"
								value={estudianteActual.cedula}
								required
								use:imask={cedulaMask as any}
								class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
								color={form?.errores?.cedula ? 'red' : undefined}
							/>

							{#if form?.errores?.cedula}
								<Helper class="mt-2" color="red">{form?.errores.cedula}</Helper>
							{/if}
						</div>
						<div>
							<Label for="nombre" class="mb-2">Nombre Completo</Label>
							<Input
								id="nombre"
								name="nombre"
								placeholder="Ingrese el nombre completo"
								value={estudianteActual.nombre}
								required
								color={form?.errores?.nombre ? 'red' : undefined}
							/>
							{#if form?.errores?.nombre}
								<Helper class="mt-2" color="red">{form?.errores.nombre}</Helper>
							{/if}
						</div>
						<div>
							<Label for="correo" class="mb-2">Correo Electrónico</Label>
							<Input
								id="correo"
								name="correo"
								type="email"
								placeholder="correo@ejemplo.com"
								value={estudianteActual.correo}
								required
								color={form?.errores?.correo ? 'red' : undefined}
							/>
							{#if form?.errores?.correo}
								<Helper class="mt-2" color="red">{form?.errores.correo}</Helper>
							{/if}
						</div>
						<div class="flex items-center">
							<Checkbox id="activo" name="activo" checked={estudianteActual.activo} />
							<Label for="activo" class="ml-2">Usuario Activo</Label>
						</div>
					</div>
				</TabItem>
				<TabItem title="Información General">
					<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
						<div>
							<Label for="fecha_nac" class="mb-2">Fecha de Nacimiento</Label>
							<input type="hidden" name="fecha_nac" value={estudianteActual.fecha_nac} />
							<Datepicker
								id="fecha_nac"
								name="fecha_nac"
								maxDate={maxYearDate()}
								bind:value={estudianteActual.fecha_nac}
							/>

							{#if form?.errores?.fecha_nac}
								<Helper class="mt-2" color="red">{form?.errores.fecha_nac}</Helper>
							{/if}
						</div>
						<div>
							<Label for="edad" class="mb-2">Edad</Label>
							<Input id="edad" type="number" value={edad} disabled />
						</div>
						<div>
							<Label for="sexo" class="mb-2">Sexo</Label>
							<Select
								id="sexo"
								name="sexo"
								value={estudianteActual.sexo}
								required
								color={form?.errores?.sexo ? 'red' : undefined}
								items={[
									{ value: 'M', name: 'Masculino' },
									{ value: 'F', name: 'Femenino' }
								]}
							/>
							{#if form?.errores?.sexo}
								<Helper class="mt-2" color="red">{form?.errores.sexo}</Helper>
							{/if}
						</div>
						<div>
							<Label for="carrera" class="mb-2">Carrera</Label>
							<Select
								id="carrera"
								name="carrera"
								value={estudianteActual.carrera}
								required
								color={form?.errores?.carrera ? 'red' : undefined}
								items={data.carreras.map((carrera) => ({
									value: carrera.id,
									name: carrera.nombre
								}))}
							/>
							{#if form?.errores?.carrera}
								<Helper class="mt-2" color="red">{form?.errores.carrera}</Helper>
							{/if}
						</div>
						<div>
							<Label for="semestre" class="mb-2">Semestre</Label>
							<Select
								id="semestre"
								name="semestre"
								value={estudianteActual.semestre}
								required
								color={form?.errores?.semestre ? 'red' : undefined}
								items={Array(10)
									.fill(null)
									.map((_, i) => ({ value: i + 1, name: `${i + 1}° Semestre` }))}
							/>
							{#if form?.errores?.semestre}
								<Helper class="mt-2" color="red">{form?.errores.semestre}</Helper>
							{/if}
						</div>
						<div>
							<Label for="promedio" class="mb-2">Promedio</Label>
							<input
								id="promedio"
								name="promedio"
								type="number"
								class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
								use:imask={nota}
								value={estudianteActual.promedio}
								required
								color={form?.errores?.promedio ? 'red' : undefined}
							/>
							{#if form?.errores?.promedio}
								<Helper class="mt-2" color="red">{form?.errores.promedio}</Helper>
							{/if}
						</div>
						<div class="md:col-span-3">
							<Label for="direccion" class="mb-2">Dirección</Label>
							<Textarea
								id="direccion"
								name="direccion"
								placeholder="Ingrese la dirección completa"
								value={estudianteActual.direccion}
								rows={3}
								color={form?.errores?.direccion ? 'red' : undefined}
							/>
							{#if form?.errores?.direccion}
								<Helper class="mt-2" color="red">{form?.errores.direccion}</Helper>
							{/if}
						</div>
					</div>
				</TabItem>
			</Tabs>
		</form>
		<svelte:fragment slot="footer">
			<Button color="blue" type="submit">
				{isEditing ? 'Actualizar' : 'Guardar'}
			</Button>
			<Button color="light" on:click={() => (modalVisible = false)}>Cancelar</Button>
		</svelte:fragment>
	</Modal>
</div>
