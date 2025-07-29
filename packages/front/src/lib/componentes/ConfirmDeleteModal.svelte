<script lang="ts">
	import { Modal, Button } from 'flowbite-svelte';
	import { ExclamationCircleOutline } from 'flowbite-svelte-icons';
	import { addToast } from '$lib';
	import { enhance } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';

	let { 
		open = $bindable(false),
		title = 'Confirmar eliminación',
		message = '¿Estás seguro de que deseas eliminar este elemento? Esta acción no se puede deshacer.',
		action,
		formData = {},
		onSuccess,
		onError
	} = $props<{
		open: boolean;
		title?: string;
		message?: string;
		action: string;
		formData?: Record<string, string | number>;
		onSuccess?: () => void;
		onError?: (error: string) => void;
	}>();

	let loading = $state(false);
	let formEl: HTMLFormElement | undefined = $state();

	const handleSubmit: SubmitFunction = () => {
		loading = true;
		return async ({ result, update }) => {
			loading = false;
			
			if (result.type === 'success') {
				addToast({
					type: 'success',
					message: 'Elemento eliminado exitosamente'
				});
				open = false;
				onSuccess?.();
				await update();
			} else if (result.type === 'failure') {
				const errorMessage = result.data?.message || 'Error al eliminar el elemento';
				addToast({
					type: 'error',
					message: errorMessage
				});
				onError?.(errorMessage);
			} else {
				await update();
			}
		};
	};

	function handleCancel() {
		open = false;
		loading = false;
	}
</script>

<Modal bind:open size="sm">
	{#snippet header()}
		<div class="flex items-center">
			<ExclamationCircleOutline class="h-6 w-6 text-red-600 mr-3" />
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
				color="red" 
				onclick={() => formEl?.requestSubmit()}
				disabled={loading}
			>
				{loading ? 'Eliminando...' : 'Eliminar'}
			</Button>
		</div>
	{/snippet}
</Modal>