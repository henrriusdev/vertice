<script lang="ts">
	import { cedulaMask, DataTable, Datepicker, maxYearDate, nota, telefono } from '$lib';
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
	import type { Coordinador } from '../../../../app';
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
	let coordinadorActual: Partial<{
		id: number;
		cedula: string;
		nombre: string;
		correo: string;
		telefono: string;
		carrera: number;
		usuario: number;
	}> = $state({
		cedula: '',
		nombre: '',
		correo: '',
		telefono: '',
		carrera: 0,
		usuario: 0
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
			coordinadorActual = {};
		}
	});

	$effect(() => {
		if (data.coordinadores) {
			coordinadoresFiltrados =
				data?.coordinadores.filter(
					(est) =>
						est?.telefono?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est?.correo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est?.nombre?.toLowerCase().includes(searchTerm.toLowerCase())
				) ?? [];
		}
	});

	let isConfirmed = $derived(password === confirmPassword);
	let coordinadores: Coordinador[] = $state(data.coordinadores);
	let coordinadoresFiltrados = $derived(
		coordinadores.filter(
			(est) =>
				est?.telefono?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est?.correo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est?.nombre?.toLowerCase().includes(searchTerm.toLowerCase())
		) ?? []
	);

	// Función para abrir el modal en modo edición
	function editarCoordinador(coordinador: any) {
		coordinadorActual = { ...coordinador, carrera: data.carreras.find((car) => car.nombre === coordinador.carrera)?.id };
		console.log('coordinadorActual', coordinadorActual);
		isEditing = true;
		modalVisible = true;
	}

	// Función para abrir el modal en modo creación
	function crearCoordinador() {
		isEditing = false;
		modalVisible = true;
	}
</script>

<div class="w-full">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Coordinadores</h1>
		<Button color="blue" onclick={crearCoordinador}>
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
			{#snippet actions(row: Coordinador)}
				<div class="flex gap-2">
					<Button size="xs" color="light" onclick={() => editarCoordinador(row)}>
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
			<DataTable data={coordinadoresFiltrados} {actions}></DataTable>
		</div>
	</div>

	<Modal
		title={isEditing ? 'Editar Coordinador' : 'Nuevo Coordinador'}
		bind:open={modalVisible}
		size="lg"
	>
		<form action={isEditing ? '?/edit' : '?/create'} method="POST" bind:this={formEl}>
			{#if isEditing}
				<input type="hidden" name="id_coordinador" value={coordinadorActual!.id} />
				<input type="hidden" name="id" value={coordinadorActual!?.usuario} />
			{/if}
			<div class="grid grid-cols-1 md:grid-cols-6 gap-4 mb-4">
				<div class="md:col-span-2">
					<Label for="cedula" class="mb-2">Cédula</Label>
					<input
						id="cedula"
						name="cedula"
						placeholder="Ingrese la cédula"
						value={coordinadorActual?.cedula}
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
						value={coordinadorActual!.nombre}
						required
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="correo" class="mb-2">Correo Electrónico</Label>
					<Input
						id="correo"
						name="correo"
						type="email"
						placeholder="correo@ejemplo.com"
						value={coordinadorActual?.correo}
						required
					/>
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
								onclick={() => (passwordVisible = !passwordVisible)}
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
								onclick={() => (confirmPVisible = !confirmPVisible)}
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
				<div class="md:col-span-3">
					<Label for="carrera" class="mb-2">Carrera</Label>
					<Select
						id="carrera"
						name="carrera_id"
						value={coordinadorActual?.carrera}
						required
						items={data.carreras.map((carrera) => ({
							value: carrera.id,
							name: carrera.nombre
						}))}
					/>
				</div>
				<div class="md:col-span-3">
					<Label for="telefono" class="mb-2">Teléfono</Label>
					<input
						id="telefono"
						name="telefono"
						placeholder="Ingrese el teléfono"
						value={coordinadorActual?.telefono}
						required
						use:imask={telefono}
						class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
					/>
				</div>
			</div>
		</form>
		<svelte:fragment slot="footer">
			<Button color="blue" type="button" onclick={() => isConfirmed && formEl?.requestSubmit()}>
				{isEditing ? 'Actualizar' : 'Guardar'}
			</Button>
			<Button color="light" onclick={() => (modalVisible = false)}>Cancelar</Button>
		</svelte:fragment>
	</Modal>
</div>
