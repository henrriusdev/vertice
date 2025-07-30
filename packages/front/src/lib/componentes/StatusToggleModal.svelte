<script lang="ts">
	import { Modal, Button } from 'flowbite-svelte';
	import { ExclamationCircleOutline } from 'flowbite-svelte-icons';
	import { addToast } from '$lib';
	import { resolver } from '$lib/utilidades/resolver';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { enhance } from '$app/forms';

	let { 
		open = $bindable(false),
		title = 'Cambiar estado',
		message = '¿Estás seguro de que deseas cambiar el estado de este elemento?',
		action,
		formData = {},
		isActivating = false,
		onSuccess,
		onError
	} = $props<{
		open: boolean;
		title?: string;
		message?: string;
		action: string;
		formData?: Record<string, string | number>;
		isActivating?: boolean;
		onSuccess?: () => void;
		onError?: (error: string) => void;
	}>();

	let loading = $state(false);
	let formEl: HTMLFormElement | undefined = $state();

	const handleSubmit: SubmitFunction = () => {
		loading = true;
		return resolver(() => {
			loading = false;
			onSuccess?.();
		});
	};

	function handleCancel() {
		open = false;
		loading = false;
	}
</script>

<Modal bind:open size="sm">
	{#snippet header()}
		<div class="flex items-center">
			<ExclamationCircleOutline class="h-6 w-6 text-{isActivating ? 'green' : 'red'}-600 mr-3" />
			<h3 class="text-lg font-semibold text-gray-900">{title}</h3>
		</div>
	{/snippet}
	
	<div class="text-gray-600 mb-6">
		{message}
	</div>

	<form bind:this={formEl} {action} method="POST" use:enhance={handleSubmit}>
		{#each Object.entries(formData) as [key, value]}
			<input type="hidden" name={key} {value} />
		{/each}
	</form>

	{#snippet footer()}
		<div class="flex justify-end space-x-3">
			<Button 
				type="button" 
				color="alternative" 
				onclick={handleCancel}
				disabled={loading}
			>
				Cancelar
			</Button>
			<Button 
				type="button" 
				color={isActivating ? "green" : "red"}
				onclick={() => formEl?.requestSubmit()}
				disabled={loading}
			>
				{loading ? (isActivating ? 'Activando...' : 'Inactivando...') : (isActivating ? 'Activar' : 'Inactivar')}
			</Button>
		</div>
	{/snippet}
</Modal>
