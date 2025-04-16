<script lang="ts">
	import { Datepicker } from '$lib';
	import { Input, Button, Label, Select, Card } from 'flowbite-svelte';
	import { parse } from 'date-fns';
	let { data } = $props();

	// Datos de configuración existentes (si los hay)
	const config = data.configuracion;

	let cicloYear = $state(config?.ciclo?.split('-')[0] ?? new Date().getFullYear());
	let cicloPeriodo = $state(config?.ciclo?.split('-')[1] ?? '1');
	let num_porcentaje = $state(config?.num_porcentaje ?? 3);
	let num_cuotas = $state(config?.num_cuotas ?? 5);
	let horario = $state([
		parse(config?.horario_inicio ?? '2025-03-10', 'yyyy-MM-dd', new Date()),
		parse(config?.horario_fin ?? '2025-04-15', 'yyyy-MM-dd', new Date())
	]);
	let porcentajes = $state<number[]>(config?.porcentajes ?? [30, 30, 40]);
	let cuotas = $state<Date[]>(config?.cuotas ?? Array(5).fill(new Date()));

	function updatePorcentaje(index: number, value: number) {
		porcentajes[index] = value;
	}

	function updateCuota(index: number, value: string) {
		cuotas[index] = value;
	}
</script>

<div class="flex h-full w-full justify-center items-center">
	<Card class="p-6 space-y-6" size="lg">
		<h1 class="text-2xl font-bold">Configuración General</h1>

		<div class="grid md:grid-cols-2 gap-4">
			<div>
				<Label>Ciclo</Label>
				<div class="flex gap-2">
					<Select bind:value={cicloYear}>
						{#each Array(6)
							.fill(0)
							.map((_, i) => new Date().getFullYear() - 2 + i) as year}
							<option value={year}>{year}</option>
						{/each}
					</Select>
					<span class="self-center">-</span>
					<Select bind:value={cicloPeriodo}>
						<option value="1">1</option>
						<option value="2">2</option>
						<option value="3">3</option>
					</Select>
				</div>
			</div>

			<div>
				<Label>Número de cortes de nota</Label>
				<Input type="number" min={1} max={10} bind:value={num_porcentaje} />
			</div>

			<div>
				<Label>Número de cuotas</Label>
				<Input type="number" min={1} max={12} bind:value={num_cuotas} />
			</div>

			<div>
				<Label>Fecha de inicio y cierre para realizar el Horario</Label>
				<Datepicker
					bind:value={horario}
					dateRange
					maxDate={new Date(horario[0].getFullYear() + 2, 0, 1)}
				/>
			</div>
		</div>

		<div>
			<h2 class="text-lg font-semibold">Porcentajes de nota</h2>
			<div class="grid md:grid-cols-3 gap-2">
				{#each Array(num_porcentaje) as _, i}
					<Input
						type="number"
						bind:value={porcentajes[i]}
						on:input={(e) => updatePorcentaje(i, +e.target.value)}
						placeholder={`Corte ${i + 1}`}
					/>
				{/each}
			</div>
		</div>

		<div>
			<h2 class="text-lg font-semibold">Fechas de cuotas</h2>
			<div class="grid md:grid-cols-3 gap-2">
				{#each Array(num_cuotas) as _, i}
					<Datepicker
						bind:value={cuotas[i]}
						minDate={i > 0 ? cuotas[i - 1] : undefined}
						on:change={(e) => updateCuota(i, e.target.value)}
						locale="es-VE"
						maxDate={new Date(horario[0].getFullYear() + 2, 0, 1)}
					/>
				{/each}
			</div>
		</div>

		<div class="pt-4">
			<Button color="primary">Guardar Configuración</Button>
		</div>
	</Card>
</div>
