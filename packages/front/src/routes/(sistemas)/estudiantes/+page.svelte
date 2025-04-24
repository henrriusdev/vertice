<script lang="ts">
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
		TableSearch,
		Textarea
	} from 'flowbite-svelte';
	import {
		CheckCircleOutline,
		ExclamationCircleOutline,
		EyeOutline,
		EyeSlashSolid,
		EyeSolid,
		PenOutline,
		PlusOutline,
		TrashBinOutline
	} from 'flowbite-svelte-icons';
	import type { Estudiante } from '../../../../app';
	import type { ActionData, PageData } from './$types';

	// Datos de la página
	let { data, form }: { data: PageData; form: ActionData } = $props<{
		data: PageData;
		form: ActionData;
	}>();

	// Estado para el modal
	let modalVisible = $state(false);
	let isEditing = $state(false);
	let passwordVisible = $state(false);
	let confirmPVisible = $state(false);
	let searchTerm = $state('');
	let formEl: HTMLFormElement | undefined = $state();
	let estudianteActual: Partial<{
			id: number
			cedula: string
			nombre: string
			correo: string
			activo: boolean,
			semestre: number,
			carrera: number,
			promedio: number,
			direccion: string,
			fecha_nac: Date | string,
			sexo: 'M' | 'F' | '',
			usuario?: {
				id: number
			}
		}> = $state({
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
		});
	let showAlert = $state(false);
	let alertMessage = $state('');
	let password = $state('');
	let confirmPassword = $state('');
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
			} else if (form.errores) {
			}
		}
	});

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

	let isConfirmed = $derived(password === confirmPassword);
	let estudiantes: Estudiante[] = $state(data.estudiantes)
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
		estudianteActual = { ...estudiante, carrera: data.carreras.find((car) => car.nombre === estudiante.carrera)?.id, fecha_nac: new Date(estudiante.fecha_nacimiento), fecha_nacimiento: undefined };
		console.log('estudianteActual', estudianteActual);
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
			fecha_nac: maxYearDate(),
			sexo: 'M'
		};
		isEditing = false;
		modalVisible = true;
	}

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
	let edad = $derived(calcularEdad(estudianteActual!.fecha_nac as string));
</script>

<div class="w-full">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Estudiantes</h1>
		{#if data.rol !== 'coordinador'}
		<Button color="blue" on:click={crearEstudiante}>
			<PlusOutline class="mr-2 h-5 w-5" />
			Registrar
		</Button>
		{/if}
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
		{#if data.rol !== 'coordinador'}
					<Button pill size="xs" class="p-1.5!" color="light" on:click={() => editarEstudiante(row)}>
						<PenOutline class="w-5 h-5" />
					</Button>
					<form action="?/delete" method="POST">
						<input type="hidden" name="cedula" value={row.cedula} />
						<Button pill class="p-1.5!" size="xs" color="red" type="submit">
							<TrashBinOutline class="w-5 h-5" />
						</Button>
					</form>
					{:else}
					<Button pill size="xs" color="light" class="p-1!" >
				<EyeOutline class="w-5 h-5" />
			</Button>
					{/if}
				</div>
			{/snippet}
			<DataTable data={estudiantesFiltrados} {actions}></DataTable>
		</div>
	</div>

	<Modal
		title={isEditing ? 'Editar Estudiante' : 'Nuevo Estudiante'}
		bind:open={modalVisible}
		size="xl"
	>
		<form
			action={isEditing ? '?/edit' : '?/create'}
			method="POST"
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
						value={estudianteActual?.cedula}
						required
						use:imask={cedulaMask as any}
						class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
						color={form?.errores?.cedula ? 'red' : undefined}
					/>

					{#if form?.errores?.cedula}
						<Helper class="mt-2" color="red">{form?.errores.cedula}</Helper>
					{/if}
				</div>
				<div class="md:col-span-2">
					<Label for="nombre" class="mb-2">Nombre Completo</Label>
					<Input
						id="nombre"
						name="nombre"
						placeholder="Ingrese el nombre completo"
						value={estudianteActual!.nombre}
						required
						color={form?.errores?.nombre ? 'red' : undefined}
					/>
					{#if form?.errores?.nombre}
						<Helper class="mt-2" color="red">{form?.errores.nombre}</Helper>
					{/if}
				</div>
				<div class="md:col-span-2">
					<Label for="fecha_nac" class="mb-2">Fecha de Nacimiento</Label>
					<Datepicker
						id="fecha_nac"
						name="fecha_nac"
						maxYear={new Date().getFullYear() - 16}
						bind:value={estudianteActual.fecha_nac}
					/>
					{#if form?.errores?.fecha_nac}
						<Helper class="mt-2" color="red">{form?.errores.fecha_nac}</Helper>
					{/if}
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
						color={form?.errores?.correo ? 'red' : undefined}
					/>
					{#if form?.errores?.correo}
						<Helper class="mt-2" color="red">{form?.errores.correo}</Helper>
					{/if}
				</div>
				{#if !isEditing}
				<div class="md:col-span-2">
					<Label for="password" class="mb-2">Contraseña</Label>
					<Input
						id="password"
						bind:value={password}
						type={passwordVisible ? 'text' : 'password'}
						name="password"
						color={confirmPassword.length !== 0 && !isConfirmed
							? 'red'
							: confirmPassword.length === 0
								? 'base'
								: 'green'}
						required
					>
						<Button
							slot="right"
							type="button"
							outline
							size="xs"
							class="!p-2"
							on:click={() => (passwordVisible = !passwordVisible)}
						>
							{#if passwordVisible}
								<EyeSlashSolid />
							{:else}
								<EyeSolid />
							{/if}
						</Button>
					</Input>
				</div>
				<div class="md:col-span-2">
					<Label for="password" class="mb-2">Confirmar contraseña</Label>
					<Input
						id="password"
						bind:value={confirmPassword}
						type={confirmPVisible ? 'text' : 'password'}
						name=""
						required
						color={confirmPassword.length !== 0 && !isConfirmed
							? 'red'
							: confirmPassword.length === 0
								? 'base'
								: 'green'}
					>
						<Button
							slot="right"
							type="button"
							outline
							size="xs"
							class="!p-2"
							on:click={() => (confirmPVisible = !confirmPVisible)}
						>
							{#if confirmPVisible}
								<EyeSlashSolid />
							{:else}
								<EyeSolid />
							{/if}
						</Button>
					</Input>
					{#if confirmPassword.length !== 0 && !isConfirmed}
						<Helper class="mt-2" color="red">Las contraseñas deben ser iguales</Helper>
					{/if}
				</div>
				{/if}
				<div class="md:col-span-2">
					<Label for="carrera" class="mb-2">Carrera</Label>
					<Select
						id="carrera"
						name="carrera"
						value={estudianteActual?.carrera}
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
					<Label for="sexo" class="mb-2">Sexo</Label>
					<Select
						id="sexo"
						name="sexo"
						value={estudianteActual?.sexo}
						placeholder=""
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
					<Label for="semestre" class="mb-2">Semestre</Label>
					<Select
						id="semestre"
						name="semestre"
						value={estudianteActual?.semestre}
						placeholder=""
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
						value={estudianteActual?.promedio}
						required
						color={form?.errores?.promedio ? 'red' : undefined}
					/>
					{#if form?.errores?.promedio}
						<Helper class="mt-2" color="red">{form?.errores.promedio}</Helper>
					{/if}
				</div>
				<div>
					<Label for="edad" class="mb-2">Edad</Label>
					<Input id="edad" name="edad" type="number" value={edad} readonly />
				</div>
				<div class={!isEditing ? "md:col-span-5" : "md:col-span-4 row-span-2"}>
					<Label for="direccion" class="mb-2">Dirección</Label>
					<Textarea
						id="direccion"
						name="direccion"
						placeholder="Ingrese la dirección completa"
						value={estudianteActual?.direccion}
						rows={3}
						color={form?.errores?.direccion ? 'red' : undefined}
					/>
					{#if form?.errores?.direccion}
						<Helper class="mt-2" color="red">{form?.errores.direccion}</Helper>
					{/if}
				</div>
				{#if isEditing}
					<div class="flex items-center">
						<Checkbox id="activo" name="activo" checked={estudianteActual?.activo} />
						<Label for="activo" class="ml-2">Usuario Activo</Label>
					</div>
				{/if}
			</div>
		</form>
		<svelte:fragment slot="footer">
			<Button color="blue" type="button" on:click={() => isConfirmed && formEl?.requestSubmit()}>
				{isEditing ? 'Actualizar' : 'Guardar'}
			</Button>
			<Button color="light" on:click={() => (modalVisible = false)}>Cancelar</Button>
		</svelte:fragment>
	</Modal>
</div>
