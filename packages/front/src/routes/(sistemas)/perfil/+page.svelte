<script lang="ts">
	import { enhance } from '$app/forms';
	import { PREGUNTAS_SEGURIDAD } from '$lib/servicios/pregunta-seguridad';
	import { resolver } from '$lib/utilidades/resolver.js';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { Avatar, Button, Card, Input, Label, Select } from 'flowbite-svelte';
	import { EnvelopeOutline, ShieldCheckOutline } from 'flowbite-svelte-icons';

	
	// Props
	let { data } = $props();

	let usuario = $derived(data.usuario);
	

	// Estado
	let selectedPregunta = $state('');
	let currentPassword = $state('');
	let newPassword = $state('');
	let confirmPassword = $state('');
	let securityAnswer = $state('');
	let currentPasswordSQ = $state('');
	let loading = $state(false);

	// Estado derivado
	let isPasswordValid = $derived(newPassword === confirmPassword && newPassword.length > 0);
	let canSubmitQuestion = $derived(selectedPregunta && securityAnswer && currentPasswordSQ);

	const handleSubmit: SubmitFunction = () => {
		loading = true;
		return resolver(() => {
			loading = false;
		});
	};
	
</script>

<div class="h-full bg-gray-50">
	<div class="container grid place-items-center h-full">
		<div class="max-w-4xl mx-auto space-y-8">
			<h1 class="text-2xl font-bold text-center">Perfil</h1>
			<!-- Información del Usuario -->
			<Card class="p-8 shadow-lg max-w-full!">
				<div class="flex flex-col items-center md:flex-row md:items-start gap-12">
					<!-- Avatar grande -->
					<div class="flex flex-col items-center gap-6">
						<div class="relative">
							<Avatar
								src={`https://unavatar.io/${usuario?.correo}`}
								size="xl"
								class="w-40 h-40 ring-4 ring-primary-500 ring-offset-4 ring-offset-white"
							/>
							<div
								class="absolute -bottom-2 left-1/2 -translate-x-1/2 px-3 py-1 bg-primary-500 text-white text-sm font-medium rounded-full"
							>
								{usuario?.activo ? 'Activo' : 'Inactivo'}
							</div>
						</div>
						<div class="text-center">
							<h2 class="text-2xl font-bold text-gray-900">{usuario?.nombre}</h2>
							<p class="text-primary-600 font-medium capitalize mt-1">{usuario?.rol.nombre}</p>
						</div>
					</div>

					<!-- Detalles del usuario -->
					<div class="flex-1 space-y-6">
						<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
							<div class="p-4 bg-white rounded-lg border border-gray-200">
								<div class="flex items-center gap-3 mb-1">
									<div class="p-2 bg-primary-100 rounded-lg">
										<EnvelopeOutline class="w-5 h-5 text-primary-600" />
									</div>
									<p class="text-sm font-medium text-gray-600">Información de Contacto</p>
								</div>
								<div class="space-y-2 ml-11">
									<p class="text-gray-900 font-medium">Correo: {usuario?.correo}</p>
									<p class="text-gray-900 font-medium">Cédula: {usuario?.cedula}</p>
								</div>
							</div>
							<div class="p-4 bg-white rounded-lg border border-gray-200">
								<div class="flex items-center gap-3 mb-1">
									<div class="p-2 bg-primary-100 rounded-lg">
										<ShieldCheckOutline class="w-5 h-5 text-primary-600" />
									</div>
									<p class="text-sm font-medium text-gray-600">Estado de la Cuenta</p>
								</div>
								<div class="space-y-2 ml-11">
									<p class="text-gray-900 font-medium">Miembro desde: {usuario?.fecha_creacion}</p>
									<p class="text-gray-900 font-medium">
										Pregunta de seguridad: {usuario?.pregunta_configurada
											? 'Configurada'
											: 'Pendiente'}
									</p>
									<p class="text-gray-900 font-medium">
										Contraseña: {usuario?.cambiar_clave
											? 'Debe cambiar su contraseña'
											: 'Actualizada'}
									</p>
								</div>
							</div>
						</div>
					</div>
				</div>
			</Card>

			<div class="grid md:grid-cols-2 gap-8">
				<!-- Cambiar Contraseña -->
				<Card class="p-6 shadow-lg">
					<h2 class="text-xl font-semibold mb-4">Cambiar Contraseña</h2>
					<form method="POST" action="?/cambiarPassword" use:enhance={handleSubmit}>
						<div class="space-y-4">
							<div>
								<Label for="currentPassword" class="space-y-2">Contraseña Actual</Label>
								<Input
									type="password"
									name="currentPassword"
									id="currentPassword"
									required
									bind:value={currentPassword}
								/>
							</div>
							<div>
								<Label for="newPassword" class="space-y-2">Nueva Contraseña</Label>
								<Input
									type="password"
									name="newPassword"
									id="newPassword"
									required
									bind:value={newPassword}
									color={isPasswordValid ? 'green' : undefined}
								/>
							</div>
							<div>
								<Label for="confirmPassword" class="space-y-2">Confirmar Nueva Contraseña</Label>
								<Input
									type="password"
									name="confirmPassword"
									id="confirmPassword"
									required
									bind:value={confirmPassword}
									color={isPasswordValid ? 'green' : undefined}
								/>
							</div>
							<Button type="submit" class="w-full" disabled={!isPasswordValid || loading}>
								{loading ? 'Cambiando...' : 'Cambiar Contraseña'}
							</Button>
						</div>
					</form>
				</Card>

				<!-- Configurar Pregunta de Seguridad -->
				<Card class="p-6 shadow-lg">
					<h2 class="text-xl font-semibold mb-4">Pregunta de Seguridad</h2>
					<form method="POST" action="?/configurarPregunta" use:enhance={handleSubmit}>
						<div class="space-y-4">
							<div>
								<Label for="pregunta" class="space-y-2">Selecciona una Pregunta</Label>
								<Select name="pregunta" id="pregunta" bind:value={selectedPregunta} required>
									{#each PREGUNTAS_SEGURIDAD as pregunta}
										<option value={pregunta}>{pregunta}</option>
									{/each}
								</Select>
							</div>
							<div>
								<Label for="respuesta" class="space-y-2">Respuesta</Label>
								<Input
									type="text"
									name="respuesta"
									id="respuesta"
									required
									bind:value={securityAnswer}
								/>
							</div>
							<div>
								<Label for="currentPasswordSQ" class="space-y-2">Contraseña Actual</Label>
								<Input
									type="password"
									name="currentPassword"
									id="currentPasswordSQ"
									required
									bind:value={currentPasswordSQ}
								/>
							</div>
							<Button type="submit" class="w-full" disabled={!canSubmitQuestion || loading}>
								{loading ? 'Configurando...' : 'Configurar Pregunta'}
							</Button>
						</div>
					</form>
				</Card>
			</div>
		</div>
	</div>
</div>
