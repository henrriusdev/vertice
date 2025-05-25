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
	import type { Usuario } from '../../../../app';
	import type { ActionData, PageData } from './$types';
	import { resolver } from '$lib/utilidades/resolver';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { enhance } from '$app/forms';

	// Datos de la página
	let { data }: { data: PageData; form: ActionData } = $props<{
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
	let usuarioActual: Partial<{
		id: number;
		cedula: string;
		nombre: string;
		correo: string;
		rol: { id: number; nombre: string };
	}> = $state({
		cedula: '',
		nombre: '',
		correo: '',
		rol: { id: 0, nombre: '' }
	});
	let password = $state('');
	let confirmPassword = $state('');

	$effect(() => {
		if (!modalVisible) {
			usuarioActual = {};
		}
	});

	$effect(() => {
		if (data.usuarios) {
			usuariosFiltrados =
				data?.usuarios.filter(
					(est) =>
						est?.correo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est?.nombre?.toLowerCase().includes(searchTerm.toLowerCase())
				) ?? [];
		}
	});

	let isConfirmed = $derived(password === confirmPassword);
	let usuarios: Usuario[] = $state(data.usuarios);
	let usuariosFiltrados = $derived(
		usuarios.filter(
			(est) =>
				est?.correo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est?.nombre?.toLowerCase().includes(searchTerm.toLowerCase())
		) ?? []
	);

	// Función para abrir el modal en modo edición
	function editarUsuario(usuario: any) {
		usuarioActual = { ...usuario };
		console.log('usuarioActual', usuarioActual);
		isEditing = true;
		modalVisible = true;
	}

	// Función para abrir el modal en modo creación
	function crearUsuario() {
		isEditing = false;
		modalVisible = true;
	}

	const handleSubmit: SubmitFunction = () => {
		return resolver(() => modalVisible = false);
	};
</script>

<div class="w-full">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Usuarios</h1>
		<Button color="blue" onclick={crearUsuario}>
			<PlusOutline class="mr-2 h-5 w-5" />
			Registrar
		</Button>
	</div>

	<div class="mb-4">
		<TableSearch bind:inputValue={searchTerm} placeholder="Buscar por nombre, cédula o correo..." />
	</div>

	<div class="overflow-x-auto">
		<div class="w-max min-w-full">
			{#snippet actions(row: Usuario)}
				<div class="flex gap-2">
					<Button size="xs" color="light" onclick={() => editarUsuario(row)}>
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
			<DataTable data={usuariosFiltrados} {actions}></DataTable>
		</div>
	</div>

	<Modal
		title={isEditing ? 'Editar Usuario' : 'Nuevo Usuario'}
		bind:open={modalVisible}
		size="md"
	>
		<form action={isEditing ? '?/edit' : '?/create'} method="POST" use:enhance={handleSubmit} bind:this={formEl}>
			{#if isEditing}
				<input type="hidden" name="id" value={usuarioActual!.id} />
			{/if}
			<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
				<div class="md:col-span-2">
					<Label for="cedula" class="mb-2">Cédula</Label>
					<input
						id="cedula"
						name="cedula"
						placeholder="Ingrese la cédula"
						value={usuarioActual?.cedula}
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
						value={usuarioActual!.nombre}
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
						value={usuarioActual?.correo}
						required
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="rol" class="mb-2">Rol</Label>
					<Select
						id="rol"
						name="rol"
						value={usuarioActual?.rol?.id ?? 3}
						required
						items={[
							{ name: 'Personal de caja', value: 2 },
							{ name: 'Personal de control de estudio', value: 3 },
						]}
					/>
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
			</div>
			{#snippet footer()}
				<Button color="blue" type="button" onclick={() => isConfirmed && formEl?.requestSubmit()}>
					{isEditing ? 'Actualizar' : 'Guardar'}
				</Button>
				<Button color="light" onclick={() => (modalVisible = false)}>Cancelar</Button>
			{/snippet}
		</form>
	</Modal>
</div>
