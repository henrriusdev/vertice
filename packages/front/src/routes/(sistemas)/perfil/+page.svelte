<script lang="ts">
	import { enhance } from '$app/forms';
	import { PREGUNTAS_SEGURIDAD } from '$lib/servicios/pregunta-seguridad';
	import { resolver } from '$lib/utilidades/resolver.js';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { Avatar, Button, Card, Input, Label, Modal, Select } from 'flowbite-svelte';
	import { EnvelopeOutline, ShieldCheckOutline } from 'flowbite-svelte-icons';

	// Props
	let { data } = $props();

	let usuario = $derived(data.usuario);

	// Estado
	let passwordModal = $state(false);
	let securityQuestionsModal = $state(false);
	let currentPassword = $state('');
	let newPassword = $state('');
	let confirmPassword = $state('');
	let loading = $state(false);

	// Preguntas de seguridad
	let securityQuestions = $state([
		{ pregunta: '', respuesta: '' },
		{ pregunta: '', respuesta: '' },
		{ pregunta: '', respuesta: '' }
	]);

	// Estado derivado
	let isPasswordValid = $derived(newPassword === confirmPassword && newPassword.length > 0);
	let canSubmitPassword = $derived(isPasswordValid);
	let canSubmitQuestions = $derived(securityQuestions.every((q) => q.pregunta && q.respuesta));

	const handleSubmit: SubmitFunction = () => {
		loading = true;
		return resolver(() => {
			loading = false;
			passwordModal = false;
			securityQuestionsModal = false;
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
						<!-- Botones de acción -->
						<div class="flex flex-col md:flex-row gap-4">
							<Button onclick={() => (passwordModal = true)} class="w-full">
								Cambio de contraseña
							</Button>
							<Button onclick={() => (securityQuestionsModal = true)} class="w-full">
								Preguntas de seguridad
							</Button>
						</div>
					</div>
				</div>
			</Card>

			<!-- Modal de cambio de contraseña -->
			<Modal bind:open={passwordModal} size="md" autoclose={false}>
				<form method="POST" action="?/cambiarPassword" use:enhance={handleSubmit} class="space-y-6">
					<h3 class="text-xl font-medium">Cambiar Contraseña</h3>
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
							/>
						</div>
						<div>
							<Label for="confirmPassword" class="space-y-2">Confirmar Contraseña</Label>
							<Input
								type="password"
								name="confirmPassword"
								id="confirmPassword"
								required
								bind:value={confirmPassword}
							/>
						</div>
						<div class="flex justify-end gap-4">
							<Button color="alternative" onclick={() => (passwordModal = false)}>Cancelar</Button>
							<Button type="submit" disabled={!canSubmitPassword || loading}>
								{loading ? 'Guardando...' : 'Cambiar Contraseña'}
							</Button>
						</div>
					</div>
				</form>
			</Modal>

			<!-- Modal de preguntas de seguridad -->
			<Modal bind:open={securityQuestionsModal} size="md" autoclose={false}>
				<form
					method="POST"
					action="?/configurarPregunta"
					use:enhance={handleSubmit}
					class="space-y-6"
				>
					<h3 class="text-xl font-medium">Configurar Preguntas de Seguridad</h3>
					<div class="space-y-4">
						{#each securityQuestions as question, i}
							<div class="space-y-4">
								<div>
									<Label for="pregunta{i}" class="space-y-2">Pregunta {i + 1}</Label>
									<Select
										name="pregunta{i}"
										id="pregunta{i}"
										bind:value={question.pregunta}
										placeholder="Seleccionar"
										required
									>
										{#each PREGUNTAS_SEGURIDAD.filter(p => 
										!securityQuestions.some((q, index) => index !== i && q.pregunta === p)
									) as pregunta}
										<option value={pregunta}>{pregunta}</option>
									{/each}
									</Select>
								</div>
								<div>
									<Label for="respuesta{i}" class="space-y-2">Respuesta {i + 1}</Label>
									<Input
										type="text"
										name="respuesta{i}"
										id="respuesta{i}"
										bind:value={question.respuesta}
										required
									/>
								</div>
							</div>
						{/each}
						<div class="flex justify-end gap-4">
							<Button color="alternative" onclick={() => (securityQuestionsModal = false)}
								>Cancelar</Button
							>
							<Button type="submit" disabled={!canSubmitQuestions || loading}>
								{loading ? 'Guardando...' : 'Guardar Preguntas'}
							</Button>
						</div>
					</div>
				</form>
			</Modal>
		</div>
	</div>
</div>
