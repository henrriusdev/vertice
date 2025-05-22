<script lang="ts">
	import { toasts } from '$lib';
	import { Toast } from 'flowbite-svelte';
	import '../app.css';
	import { fly } from 'svelte/transition';
	import {
		CheckCircleOutline,
		ExclamationCircleOutline,
		InfoCircleOutline
	} from 'flowbite-svelte-icons';

	let { children } = $props();
</script>

<div class="relative">
	{#each $toasts as toast (toast.id)}
		{@const color = toast.type === 'error' ? 'red' : toast.type === 'success' ? 'green' : 'primary'}
		<Toast
			position="bottom-right"
			class="z-[800]"
			transition={fly}
			{color}
			params={{ duration: 300, x: 150 }}
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
			{toast.message}</Toast
		>
	{/each}
	{@render children()}
</div>
