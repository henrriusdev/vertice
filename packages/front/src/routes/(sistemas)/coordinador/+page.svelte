<script lang="ts">
	import {
		Alert,
		Badge,
		Card,
		Chart,
		Heading,
		P,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import type { PageData } from './$types';
	import type { DistribucionCarrera, PromedioCarrera } from './types';

	let { data }: { data: PageData } = $props();

	// Estadísticas de la(s) carrera(s) del coordinador
	let totalEstudiantes = $derived(data.estadisticas?.estudiantes || 0);
	let totalDocentes = $derived(data.estadisticas?.docentes || 0);
	let totalMaterias = $derived(data.estadisticas?.materias || 0);

	// Gráfico de distribución por carrera (solo las del coordinador)
	let distribucionOptions = $derived({
		chart: {
			type: 'bar' as const,
			height: 350,
			toolbar: { show: false }
		},
		series: [
			{
				name: 'Estudiantes',
				data: [data.distribucionCarreras?.estudiantes ?? 0]
			}
		],
		xaxis: {
			categories: [data.distribucionCarreras?.nombre ?? 'Carrera'],
			title: { text: 'Carrera' }
		},
		yaxis: { title: { text: 'Estudiantes' } },
		colors: ['#1a56db']
	});

	// Gráfico de promedios por carrera (solo las del coordinador)
	let promediosOptions = $derived({
		chart: {
			type: 'line' as const,
			height: 350,
			toolbar: { show: false }
		},
		series: [
			{
				name: 'Promedio',
				data: [data.promediosCarreras?.promedio ?? 0]
			}
		],
		xaxis: {
			categories: [data.promediosCarreras?.nombre ?? 'Carrera'],
			title: { text: 'Carrera' }
		},
		yaxis: { min: 0, max: 20, title: { text: 'Promedio' } },
		colors: ['#16a34a'],
		stroke: { curve: 'smooth' as const, width: 3 },
		markers: { size: 5 }
	});
</script>

<div class="w-full p-4">
	<h2 class="text-2xl font-bold mb-4">Panel de Coordinador</h2>

	<div class="grid md:grid-cols-6 gap-4 mb-6">
		<!-- Estadísticas -->
		<Card class="col-span-6 p-4 max-w-full">
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<P weight="bold" class="text-3xl text-primary-700">{totalEstudiantes}</P>
					<P size="sm">Estudiantes Activos</P>
				</div>
				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<P weight="bold" class="text-3xl text-green-600">{totalDocentes}</P>
					<P size="sm">Docentes Activos</P>
				</div>
				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<P weight="bold" class="text-3xl text-blue-600">{totalMaterias}</P>
					<P size="sm">Materias Activas</P>
				</div>
			</div>
		</Card>

		<!-- Gráfico de distribución por carrera -->
		<Card class="col-span-3 p-4 max-w-full">
			<Heading tag="h3" class="mb-4">Distribución de Estudiantes por Carrera</Heading>
			<Chart options={distribucionOptions} />
		</Card>

		<!-- Gráfico de promedios por carrera -->
		<Card class="col-span-3 p-4 max-w-full">
			<Heading tag="h3" class="mb-4">Promedio por Carrera</Heading>
			<Chart options={promediosOptions} />
		</Card>


	</div>
</div>
