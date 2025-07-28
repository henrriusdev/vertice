<script lang="ts">
	import ToastContainer from '$lib/componentes/ToastContainer.svelte';
	import '../app.css';
	let { children } = $props();
</script>

<div class="relative" data-sveltekit-preload-code>
	<ToastContainer position="bottom-right" />
	{@render children()}
</div>
