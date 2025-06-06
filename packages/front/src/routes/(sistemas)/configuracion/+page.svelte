<script lang="ts">
	import { Datepicker } from '$lib';
	import { Input, Button, Label, Select, Card } from 'flowbite-svelte';
	import { format, parse } from 'date-fns';
	import { toZonedTime } from 'date-fns-tz';
	import { enhance } from '$app/forms';

	let { data } = $props();

	// Datos de configuración existentes (si los hay)
	const config = data.configuracion;

	let cicloYear = $derived(config?.ciclo?.split('-')[0] ?? new Date().getFullYear());
	let cicloPeriodo = $derived(config?.ciclo?.split('-')[1] ?? '1');
	let num_porcentaje = $state(config?.num_porcentaje ?? 3);
	let num_cuotas = $state(config?.num_cuotas ?? 5);
	let horario = $state({
		from: config?.horario_inicio
			? toZonedTime(config.horario_inicio, 'UTC')
			: toZonedTime(parse('2025-04-15', 'yyyy-MM-dd', new Date()), 'UTC'),
		to: config?.horario_fin
			? toZonedTime(config.horario_fin, 'UTC')
			: toZonedTime(parse('2025-05-15', 'yyyy-MM-dd', new Date()), 'UTC')
	});
	let filtroCarrera: number | null = $state(data.rol === 'coordinador' ? data.carrera_id : null);
	let porcentajes = $state<number[]>(config?.porcentajes ?? [30, 30, 40]);
	let cuotas = $state<Date[]>(
		config?.cuotas
			? [...config.cuotas.map((cuota) => toZonedTime(cuota, 'UTC'))]
			: Array(5).fill(new Date())
	);

	function updatePorcentaje(index: number, value: number) {
		porcentajes[index] = value;
	}

	function getValue(date: Date) {
		if (!date || date.toString() === 'Invalid Date') return '';
		return format(date, 'dd/MM/yyyy');
	}
</script>

<form
	use:enhance={() => {
		return async ({ update }) => {
			await update();
		};
	}}
	method="post"
	class="flex h-full w-full justify-center items-center"
>
	<Card class="p-6 space-y-6" size="xl">
		<h1 class="text-2xl font-bold">Configuración General</h1>

		<div class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
			<div>
				<Label>Ciclo</Label>
				<div class="flex gap-2">
					<Select
						name="cicloYear"
						bind:value={cicloYear}
						items={Array.from({ length: 5 }, (_, i) => ({
							value: String(new Date().getFullYear() + i),
							name: String(new Date().getFullYear() + i)
						}))}
					></Select>
					<span class="self-center font-black">-</span>
					<Select
						bind:value={cicloPeriodo}
						name="cicloPeriodo"
						items={[
							{ value: '1', name: '1' },
							{ value: '2', name: '2' },
							{ value: '3', name: '3' }
						]}
					></Select>
				</div>
			</div>

			<div>
				<Label for="num_porcentaje">Número de cortes de nota</Label>
				<Input
					id="num_porcentaje"
					name="num_porcentaje"
					type="number"
					min={1}
					max={10}
					bind:value={num_porcentaje}
				/>
			</div>

			<div>
				<Label for="num_cuotas">Número de cuotas</Label>
				<Input type="number"  id="num_cuotas" name="num_cuotas" min={1} max={12} bind:value={num_cuotas} />
			</div>

			<div>
				<Label>Fecha de inicio y cierre para realizar el Horario</Label>
				<Datepicker bind:value={horario} dateRange />
				{#if horario.from && horario.to && horario.from.toString() !== 'Invalid Date' && horario.to.toString() !== 'Invalid Date'}
					<input
						type="hidden"
						name="horario_inicio"
						value={horario.from && horario.from.toUTCString()}
					/>
					<input type="hidden" name="horario_fin" value={horario.to && horario.to.toUTCString()} />
				{/if}
			</div>
		</div>

		<div>
			<h2 class="text-lg font-semibold">Porcentajes de nota</h2>
			<p class="text-sm text-gray-500">Entre todos los porcentajes se debe sumar 100%</p>
			<div class="grid md:grid-cols-3 gap-2">
				{#each Array(num_porcentaje) as _, i}
					<Input type="number" 
						min={0}
						max={100}
						inputmode="numeric"
						name={`porcentajes[${i}]`}
						bind:value={porcentajes[i]}
						oninput={(e) => updatePorcentaje(i, +e.target.value)}
						placeholder={`Corte ${i + 1}`}
					/>
				{/each}
			</div>
		</div>

		<div>
			<h2 class="text-lg font-semibold">Fechas de cuotas</h2>
			<div class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
				{#each Array(num_cuotas) as _, i}
					<Datepicker bind:value={cuotas[i]} />
					<input type="hidden" name={`cuotas`} value={getValue(cuotas[i])} />
				{/each}
			</div>
		</div>

		<div class="pt-4">
			<Button color="primary" type="submit">Guardar Configuración</Button>
		</div>
	</Card>
</form>
