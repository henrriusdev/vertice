<script lang="ts">
	import { enhance } from '$app/forms';
	import { resolver } from '$lib/utilidades/resolver';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { Alert, Button, Input, Label, StepIndicator } from 'flowbite-svelte';

	// Estado
	let loading = $state(false);
	let error = $state('');
	let currentStep = $state(0);
	let intentos = $state(0);

	// Datos del formulario
	let correo = $state('');
	let respuesta = $state('');
	let preguntaSeguridad = $state('');
	let newPassword = $state('');
	let confirmPassword = $state('');

	// Validaciones
	let isPasswordValid = $derived(newPassword.length >= 8 && newPassword === confirmPassword);
	let canSubmitEmail = $derived(correo.length > 0);
	let canSubmitAnswer = $derived(respuesta.length > 0);
	let canSubmitPassword = $derived(isPasswordValid);

	// Handlers
	const handleEmailSubmit: SubmitFunction = () => {
		if (!canSubmitEmail) return;
		loading = true;

		return resolver(() => {
			loading = false;
		});
	};

	const handleAnswerSubmit: SubmitFunction = () => {
		if (!canSubmitAnswer) return;
		loading = true;

		return resolver(() => {
			loading = false;
		});
	};

	const handlePasswordSubmit: SubmitFunction = () => {
		if (!canSubmitPassword) return;
		loading = true;

		return resolver(() => {
			loading = false;
		});
	};
</script>

<div class="min-h-screen flex items-center justify-center bg-blue-50 dark:bg-gray-900">
	<div class="w-full max-w-md bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-xl space-y-6">
		<h1 class="text-2xl font-bold text-center text-blue-700 dark:text-white">
			Recuperar Contraseña
		</h1>

		<StepIndicator currentStep={currentStep} steps={['Correo', 'Pregunta', 'Contraseña']} color="blue" class="mb-4" />

		{#if error}
			<Alert color="red" class="text-sm">{error}</Alert>
		{/if}

		{#if currentStep === 0}
			<div>
				<h3 class="mb-4">Paso 1: Ingresa tu correo</h3>
				<form method="POST" use:enhance={handleEmailSubmit} class="space-y-6">
					<div>
						<Label for="correo">Correo Electrónico</Label>
						<Input
							type="email"
							id="correo"
							name="correo"
							bind:value={correo}
							required
							placeholder="usuario@ejemplo.com"
						/>
					</div>

					<div class="flex justify-between gap-4">
						<Button href="/" color="alternative">Cancelar</Button>
						<Button type="submit" disabled={!canSubmitEmail || loading}>
							{loading ? 'Verificando...' : 'Siguiente'}
						</Button>
					</div>
				</form>
			</div>
		{:else if currentStep === 1}
			<div>
				<h3 class="mb-4">Paso 2: Responde tu pregunta de seguridad</h3>
				<form method="POST" use:enhance={handleAnswerSubmit} class="space-y-6">
					<div>
						<Label>Pregunta de Seguridad</Label>
						<p class="text-gray-700 dark:text-gray-300 mb-4">{preguntaSeguridad}</p>

						<Label for="respuesta">Tu Respuesta</Label>
						<Input
							type="text"
							id="respuesta"
							name="respuesta"
							bind:value={respuesta}
							required
							placeholder="Tu respuesta"
						/>
					</div>

					<div class="flex justify-between gap-4">
						<Button color="alternative" onclick={() => currentStep = Math.max(0, currentStep - 1)}>Atrás</Button>
						<Button type="submit" disabled={!canSubmitAnswer || loading || intentos >= 3}>
							{loading ? 'Verificando...' : 'Siguiente'}
						</Button>
					</div>
				</form>
			</div>
		{:else if currentStep === 2}
			<div>
				<h3 class="mb-4">Paso 3: Establece tu nueva contraseña</h3>
				<form method="POST" use:enhance={handlePasswordSubmit} class="space-y-6">
					<div>
						<Label for="newPassword">Nueva Contraseña</Label>
						<Input
							type="password"
							id="newPassword"
							name="newPassword"
							bind:value={newPassword}
							required
							color={isPasswordValid ? 'green' : undefined}
						/>
					</div>

					<div>
						<Label for="confirmPassword">Confirmar Nueva Contraseña</Label>
						<Input
							type="password"
							id="confirmPassword"
							name="confirmPassword"
							bind:value={confirmPassword}
							required
							color={isPasswordValid ? 'green' : undefined}
						/>
					</div>

					<div class="flex justify-between gap-4">
						<Button color="alternative" onclick={() => currentStep = Math.max(0, currentStep - 1)}>Atrás</Button>
						<Button type="submit" disabled={!canSubmitPassword || loading}>
							{loading ? 'Guardando...' : 'Cambiar Contraseña'}
						</Button>
					</div>
				</form>
			</div>
		{/if}
	</div>
</div>
