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
		EyeSlashSolid,
		EyeSolid,
		PenOutline,
		PlusOutline,
		TrashBinOutline
	} from 'flowbite-svelte-icons';
	import type { Docente } from '../../../../app';
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
	let docenteActual: Partial<{
		id: number;
		cedula: string;
		nombre: string;
		correo: string;
		estatus: string;
		fecha_ingreso: Date | string;
		observaciones: string;
		dedicacion: string;
		titulo: string;
		especialidad: string;
		usuario: number;
	}> = $state({
		cedula: '',
		nombre: '',
		correo: '',
		activo: true,
		semestre: 1,
		carrera: 1,
		promedio: 0,
		direccion: '',
		sexo: 'M',
		fecha_ingreso: new Date()
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
			console.log('form', form);
			if ((form as any).success) {
				modalVisible = false;
				mostrarAlerta((form as any).message, 'success');
			} else if (form.errores) {
			}
		}
	});

	$effect(() => {
		if (!modalVisible) {
			docenteActual = {};
		}
	});

	$effect(() => {
		if (data.docentes) {
			docentesFiltrados =
				data?.docentes.filter(
					(est) =>
						est?.dedicacion?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est?.especialidad?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est?.titulo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est.fecha_ingreso.toLowerCase().includes(searchTerm.toLowerCase())
				) ?? [];
		}
	});

	let isConfirmed = $derived(password === confirmPassword);
	let docentes: Docente[] = $state(data.docentes);
	let docentesFiltrados = $derived(
		docentes.filter(
			(est) =>
				est?.dedicacion?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est?.especialidad?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est?.titulo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est.fecha_ingreso.toLowerCase().includes(searchTerm.toLowerCase())
		) ?? []
	);

	// Función para abrir el modal en modo edición
	function editarDocente(docente: any) {
		docenteActual = { ...docente };
		console.log('docenteActual', docenteActual);
		isEditing = true;
		modalVisible = true;
	}

	// Función para abrir el modal en modo creación
	function crearDocente() {
		isEditing = false;
		modalVisible = true;
	}
</script>

<div class="w-full">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Docentes</h1>
		<Button color="blue" on:click={crearDocente}>
			<PlusOutline class="mr-2 h-5 w-5" />
			Registrar
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
			{#snippet actions(row: Docente)}
				<div class="flex gap-2">
					<Button size="xs" color="light" on:click={() => editarDocente(row)}>
						<PenOutline class="w-4 h-4" />
					</Button>
					<form action="?/delete" method="POST">
						<input type="hidden" name="cedula" value={row.cedula} />
						<Button size="xs" color="red" type="submit">
							<TrashBinOutline class="w-4 h-4" />
						</Button>
					</form>
				</div>
			{/snippet}
			<DataTable data={docentesFiltrados} {actions}></DataTable>
		</div>
	</div>

	<Modal title={isEditing ? 'Editar Docente' : 'Nuevo Docente'} bind:open={modalVisible} size="lg">
		<form action={isEditing ? '?/edit' : '?/create'} method="POST" bind:this={formEl}>
			{#if isEditing}
				<input type="hidden" name="id_docente" value={docenteActual!.id} />
				<input type="hidden" name="id" value={docenteActual!?.usuario} />
			{/if}
q
			<div class="grid grid-cols-1 md:grid-cols-6 gap-4 mb-4">
				<div class="md:col-span-2">
					<Label for="cedula" class="mb-2">Cédula</Label>
					<input
						id="cedula"
						name="cedula"
						placeholder="Ingrese la cédula"
						value={docenteActual?.cedula}
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
						value={docenteActual!.nombre}
						required
						color={form?.errores?.nombre ? 'red' : undefined}
					/>
					{#if form?.errores?.nombre}
						<Helper class="mt-2" color="red">{form?.errores.nombre}</Helper>
					{/if}
				</div>
				<div class="md:col-span-2">
					<Label for="correo" class="mb-2">Correo Electrónico</Label>
					<Input
						id="correo"
						name="correo"
						type="email"
						placeholder="correo@ejemplo.com"
						value={docenteActual?.correo}
						required
						color={form?.errores?.correo ? 'red' : undefined}
					/>
					{#if form?.errores?.correo}
						<Helper class="mt-2" color="red">{form?.errores.correo}</Helper>
					{/if}
				</div>
				{#if !isEditing}
					<div class="md:col-span-3">
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
					<div class="md:col-span-3">
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
					<Label for="titulo" class="mb-2">Titulo</Label>
					<Input
						id="titulo"
						name="titulo"
						placeholder="Ingrese el titulo"
						value={docenteActual!.titulo}
						required
						color={form?.errores?.titulo ? 'red' : undefined}
					/>
					{#if form?.errores?.titulo}
						<Helper class="mt-2" color="red">{form?.errores.titulo}</Helper>
					{/if}
				</div>
				<div class="md:col-span-2">
					<Label for="especialidad" class="mb-2">Especialidad</Label>
					<Input
						id="especialidad"
						name="especialidad"
						placeholder="Ingrese la especialidad"
						value={docenteActual!.nombre}
						required
						color={form?.errores?.nombre ? 'red' : undefined}
					/>
					{#if form?.errores?.especialidad}
						<Helper class="mt-2" color="red">{form?.errores.especialidad}</Helper>
					{/if}
				</div>
				<div class="md:col-span-2">
					<Label for="dedicacion" class="mb-2">Dedicacion</Label>
					<Input
						id="dedicacion"
						name="dedicacion"
						placeholder="Ingrese la dedicacion"
						value={docenteActual!.dedicacion}
						required
						color={form?.errores?.dedicacion ? 'red' : undefined}
					/>
					{#if form?.errores?.dedicacion}
						<Helper class="mt-2" color="red">{form?.errores.dedicacion}</Helper>
					{/if}
				</div>
				<div class="md:col-span-2">
					<Label for="estatus" class="mb-2">Estatus</Label>
					<Select
						id="estatus"
						name="estatus"
						value={docenteActual?.estatus}
						required
						color={form?.errores?.estatus ? 'red' : undefined}
						items={[
							{ value: 'activo', name: 'Activo' },
							{ value: 'inactivo', name: 'Inactivo' },
							{ value: 'suspendido', name: 'Suspendido' },
							{ value: 'retirado', name: 'Retirado' },
							{ value: 'expulsado', name: 'Expulsado' },
							{ value: 'de permiso', name: 'De permiso' }
						]}
					/>
					{#if form?.errores?.estatus}
						<Helper class="mt-2" color="red">{form?.errores.estatus}</Helper>
					{/if}
				</div>
				<div class="md:col-span-2">
					<Label for="fecha_ingreso" class="mb-2">Fecha e ingreso</Label>
					<Datepicker
						id="fecha_ingreso"
						name="fecha_ingreso"
						maxDate={new Date()}
						bind:value={docenteActual.fecha_ingreso}
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="observaciones" class="mb-2">Observaciones</Label>
					<Textarea
						id="observaciones"
						name="observaciones"
						placeholder="Ingrese la observación completa"
						value={docenteActual?.observaciones}
						rows={1}
						color={form?.errores?.observaciones ? 'red' : undefined}
					/>
					{#if form?.errores?.observaciones}
						<Helper class="mt-2" color="red">{form?.errores.observaciones}</Helper>
					{/if}
				</div>
			</div>
		</form>
		<svelte:fragment slot="footer">
			<Button color="blue" type="button" on:click={() => isConfirmed && formEl.requestSubmit()}>
				{isEditing ? 'Actualizar' : 'Guardar'}
			</Button>
			<Button color="light" on:click={() => (modalVisible = false)}>Cancelar</Button>
		</svelte:fragment>
	</Modal>
</div>
