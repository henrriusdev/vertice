<script lang="ts">
	import Flatpickr from 'svelte-flatpickr';
	import 'flatpickr/dist/themes/material_blue.css';

	import type { BaseOptions } from 'flatpickr/dist/types/options';

	type InputHTMLProps = Partial<Omit<HTMLElementTagNameMap['input'], 'value'>>;
	// ✅ Props reactivas
	let {
		value = $bindable(),
		options = {},
		dateRange = false,
		timePicker = false,
    maxDate = new Date(),
		onChange,
		...others
	} = $props<{
		value: Date | Date[] | null;
		options?: Partial<BaseOptions>;
		dateRange?: boolean;
		timePicker?: boolean;
    maxDate?: Date;
		onChange?: () => void;
	} & InputHTMLProps>();

	// ✅ Valor derivado sin usar $:
	const mergedOptions = $derived({
		mode: dateRange ? 'range' : 'single',
		enableTime: timePicker || options.enableTime,
		noCalendar: timePicker,
		dateFormat: timePicker ? 'H:i' : 'd/m/Y',
		time_24hr: false,
		allowInput: false,
    maxDate,
		locale: {
			firstDayOfWeek: 1,
			rangeSeparator: ' al ',
			weekdays: {
				shorthand: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
				longhand: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
			},
			months: {
				shorthand: [
					'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
				],
				longhand: [
					'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
				]
			}
		},
		...options
	});

	function change() {
		if (onChange) {
			onChange();
		}
	}

</script>

<div class="form-control w-full">
	<Flatpickr
		bind:value
		id="datepicker"
		name="datepicker"
		options={mergedOptions}
		class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
		on:change={change}
		{...others}
	/>
</div>
