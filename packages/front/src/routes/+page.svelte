<script lang="ts">
	import { enhance } from '$app/forms';
	import { resolver } from '$lib/utilidades/resolver';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { Alert, Button, Input, Label } from 'flowbite-svelte';
	import { EyeSlashSolid, EyeSolid, LockSolid, UserSolid } from 'flowbite-svelte-icons';

	let password = $state('');
	let error = $state('');
	let visible = $state(false);
	let loading = $state(false);

	const toggleVisibility = () => (visible = !visible);

	const handleSubmit: SubmitFunction = () => {
		return resolver(() => loading = false);
	};
</script>

<div class="min-h-screen flex items-center justify-center bg-blue-50 dark:bg-gray-900 relative">
	
	<form
		method="post"
		use:enhance={handleSubmit}
		class="w-full max-w-md bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-xl space-y-6"
	>
		<h1 class="text-2xl font-bold text-center text-blue-700 dark:text-white">Iniciar sesión</h1>

		{#if error}
			<Alert color="primary" class="text-sm">{error}</Alert>
		{/if}

		<div>
			<Label for="correo">Correo</Label>
			<Input id="correo" name="correo" type="email" placeholder="usuario@ejemplo.com" required />
		</div>

		<div>
			<Label for="password">Contraseña</Label>
			<div class="relative">
				<Input
					id="password"
					bind:value={password}
					type={visible ? 'text' : 'password'}
					name="password"
					required
				/>
				<Button
					type="button"
					outline
					size="xs"
					class="absolute right-2 top-1/2 -translate-y-1/2 !p-2"
					onclick={toggleVisibility}
				>
					{#if visible}
						<EyeSlashSolid />
					{:else}
						<EyeSolid />
					{/if}
				</Button>
			</div>
		</div>

		<Button type="submit" color="blue" class="w-full">Entrar</Button>

		<div class="text-center">
			<a href="/recuperar" class="text-sm text-blue-600 hover:underline dark:text-blue-500">
				¿Olvidaste tu contraseña?
			</a>
		</div>
	</form>
</div>

<style>
	:global(input + div.flex.absolute) {
		padding: 0 !important;
	}
</style>
