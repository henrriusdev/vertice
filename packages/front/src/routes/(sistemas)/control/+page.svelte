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

	// Estadísticas
	let totalEstudiantes = $derived(data.estadisticas?.estudiantes || 0);
	let totalDocentes = $derived(data.estadisticas?.docentes || 0);
	let totalMaterias = $derived(data.estadisticas?.materias || 0);
	let totalCarreras = $derived(data.estadisticas?.carreras || 0);

	// Gráfico de distribución por carrera
	let distribucionOptions = $derived({
		chart: {
			type: 'bar' as const,
			height: 350,
			toolbar: {
				show: false
			}
		},
		series: [
			{
				name: 'Estudiantes',
				data: data.distribucionCarreras?.map((c: DistribucionCarrera) => c.estudiantes) || []
			}
		],
		xaxis: {
			categories: data.distribucionCarreras?.map((c: DistribucionCarrera) => c.nombre) || [],
			title: {
				text: 'Carrera'
			}
		},
		yaxis: {
			title: {
				text: 'Estudiantes'
			}
		},
		colors: ['#1a56db']
	});

	// Gráfico de promedios por carrera
	let promediosOptions = $derived({
		chart: {
			type: 'line' as const,
			height: 350,
			toolbar: {
				show: false
			}
		},
		series: [
			{
				name: 'Promedio',
				data: data.promediosCarreras?.map((c: PromedioCarrera) => c.promedio) || []
			}
		],
		xaxis: {
			categories: data.promediosCarreras?.map((c: PromedioCarrera) => c.nombre) || [],
			title: {
				text: 'Carrera'
			}
		},
		yaxis: {
			min: 0,
			max: 20,
			title: {
				text: 'Promedio'
			}
		},
		colors: ['#16a34a'],
		stroke: {
			curve: 'smooth' as const,
			width: 3
		},
		markers: {
			size: 5
		}
	});
</script>

<div class="w-full p-4">
	<h2 class="text-2xl font-bold mb-4">Panel de Control</h2>

	<div class="grid md:grid-cols-6 gap-4 mb-6">
		<!-- Estadísticas -->
		<Card class="col-span-6 p-4 max-w-full">
			<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
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

				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<P weight="bold" class="text-3xl text-purple-600">{totalCarreras}</P>
					<P size="sm">Carreras</P>
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

		<!-- Últimas sesiones -->
		<Card class="col-span-2 p-4 max-w-full">
			<Heading tag="h3" class="mb-4">Actividad Reciente</Heading>
			{#if data.sesiones?.length > 0}
				<Table striped={true}>
					<TableHead>
						<TableHeadCell>Usuario</TableHeadCell>
						<TableHeadCell>Fecha</TableHeadCell>
						<TableHeadCell>Estado</TableHeadCell>
					</TableHead>
					<TableBody>
						{#each data.sesiones as sesion}
							<TableBodyRow>
								<TableBodyCell>{sesion.usuario}</TableBodyCell>
								<TableBodyCell>{sesion.fecha}</TableBodyCell>
								<TableBodyCell>
									<Badge color={sesion.estado === 'activa' ? 'green' : 'gray'}>
										{sesion.estado}
									</Badge>
								</TableBodyCell>
							</TableBodyRow>
						{/each}
					</TableBody>
				</Table>
			{:else}
				<Alert color="blue">No hay sesiones registradas</Alert>
			{/if}
		</Card>

		<!-- Últimos pagos -->
		<Card class="col-span-2 p-4 max-w-full">
			<Heading tag="h3" class="mb-4">Últimos Pagos</Heading>
			{#if data.pagos?.length > 0}
				<Table striped={true}>
					<TableHead>
						<TableHeadCell>Estudiante</TableHeadCell>
						<TableHeadCell>Monto</TableHeadCell>
						<TableHeadCell>Estado</TableHeadCell>
					</TableHead>
					<TableBody>
						{#each data.pagos as pago}
							<TableBodyRow>
								<TableBodyCell>{pago.estudiante}</TableBodyCell>
								<TableBodyCell>${pago.monto}</TableBodyCell>
								<TableBodyCell>
									<Badge color={pago.estado === 'aprobado' ? 'green' : 'yellow'}>
										{pago.estado}
									</Badge>
								</TableBodyCell>
							</TableBodyRow>
						{/each}
					</TableBody>
				</Table>
			{:else}
				<Alert color="blue">No hay pagos registrados</Alert>
			{/if}
		</Card>

		<!-- Peticiones pendientes -->
		<Card class="col-span-2 p-4 max-w-full">
			<Heading tag="h3" class="mb-4">Peticiones Pendientes</Heading>
			{#if data.peticiones?.length > 0}
				<Table striped={true}>
					<TableHead>
						<TableHeadCell>Estudiante</TableHeadCell>
						<TableHeadCell>Tipo</TableHeadCell>
						<TableHeadCell>Estado</TableHeadCell>
					</TableHead>
					<TableBody>
						{#each data.peticiones as peticion}
							<TableBodyRow>
								<TableBodyCell>{peticion.estudiante}</TableBodyCell>
								<TableBodyCell>{peticion.tipo}</TableBodyCell>
								<TableBodyCell>
									<Badge color="yellow">{peticion.estado}</Badge>
								</TableBodyCell>
							</TableBodyRow>
						{/each}
					</TableBody>
				</Table>
			{:else}
				<Alert color="blue">No hay peticiones pendientes</Alert>
			{/if}
		</Card>
	</div>
</div>