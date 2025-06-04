<script lang="ts">
	import { Toast } from 'flowbite-svelte';
	import { fly } from 'svelte/transition';
	import {
		CheckCircleOutline,
		ExclamationCircleOutline,
		InfoCircleOutline
	} from 'flowbite-svelte-icons';

	import { toasts } from '$lib';

	let { position = 'bottom-right' } = $props<{ position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' }>();
</script>

{#each $toasts as toast (toast.id)}
	{@const color = toast.type === 'error' ? 'red' : toast.type === 'success' ? 'green' : 'primary'}
	<Toast
		transition={fly}
		{color}
		params={{ duration: 300, x: 150 }}
		class="z-[99999]"
		{position}
	>
		{#snippet icon()}
			{#if toast.type === 'error'}
				<ExclamationCircleOutline class="h-5 w-5" />
			{:else if toast.type === 'success'}
				<CheckCircleOutline class="h-5 w-5" />
			{:else}
				<InfoCircleOutline class="h-5 w-5" />
			{/if}
			<span class="sr-only">Check icon</span>
		{/snippet}
		{toast.message}
	</Toast>
{/each}
