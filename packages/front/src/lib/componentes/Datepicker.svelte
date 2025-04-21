<script lang="ts">
	import { Datepicker, Timepicker } from 'flowbite-svelte';

	let {
		dateRange,
		timePicker,
		value = $bindable()
	}: {
		dateRange?: boolean;
		timePicker?: boolean;
		value: Date | { from?: Date; to?: Date } | null;
	} = $props();

</script>

<div class="w-full">
	{#if dateRange}
		<Datepicker
			autohide
			range
			bind:rangeFrom={value!.from}
			bind:rangeTo={value!.to}
			firstDayOfWeek={1}
			title="Selecciona fecha de inicio y fin"
			inputClass="w-full"
			locale="es-VE"
			dateFormat={{ year: 'numeric', month: '2-digit', day: '2-digit' }}
		/>
	{:else if timePicker}
		<Timepicker
			bind:value
			format="24"
			placeholder="Selecciona una hora"
			inputClass="w-full"
		/>
	{:else}
		<Datepicker
			bind:value
			autohide
			firstDayOfWeek={1}
			locale="es-VE"
			title="Selecciona una fecha"
			inputClass="w-full"
			dateFormat={{ year: 'numeric', month: '2-digit', day: '2-digit' }}
		/>
	{/if}
</div>
