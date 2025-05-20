<script lang="ts">
	import type { PageData } from './$types';
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		Card,
		Button,
		Alert,
		Badge,
		Heading,
		P, Tooltip
	} from 'flowbite-svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { FileLinesOutline } from 'flowbite-svelte-icons';
	import {enhance} from '$app/forms';

	let { data }: { data: PageData } = $props();

	// Calcular estadísticas
	let creditosObtenidos = $derived(
		data.historicoMaterias
			?.filter((materia) => materia.estatus === 'Aprobada')
			?.reduce((total, materia) => total + materia.creditos, 0) || 0
	);

	let materiasAplazadas = $derived(
		data?.historicoMaterias.filter((materia) => materia.estatus === 'Reprobada').length || 0
	);

	let promedioGeneral = $derived(
		data.historicoMaterias
			?.filter((materia) => materia.estatus === 'Aprobada')
			?.reduce((sum, materia) => sum + materia.nota_final, 0) /
		data.historicoMaterias.filter((materia) => materia.estatus === 'Aprobada').length || 0
	);

	// Preparar datos para el gráfico
	let semestreLabels = $derived(
		Array.from(new Set(data.historicoMaterias?.map((materia) => materia.semestre)))
			.sort((a, b) => a - b)
			.map((semestre) => `Semestre ${semestre}`) || []
	);

	let promedioData = $derived(
		semestreLabels?.map((semestreLabel) => {
			const semestre = parseInt(semestreLabel.split(' ')[1]);
			const materiasSemestre = data.historicoMaterias.filter(
				(materia) => materia.semestre === semestre && materia.estatus === 'Aprobada'
			);

			const promedio =
				materiasSemestre.length > 0
					? materiasSemestre.reduce((sum, materia) => sum + materia.nota_final, 0) /
					materiasSemestre.length
					: 0;

			return parseFloat(promedio.toFixed(2));
		}) || []
	);

	// Configuración del gráfico
	let options = $derived({
		chart: {
			type: 'line',
			height: 350,
			toolbar: {
				show: false
			}
		},
		series: [
			{
				name: 'Promedio',
				data: promedioData
			}
		],
		stroke: {
			curve: 'smooth',
			width: 3
		},
		colors: ['#1a56db'],
		markers: {
			size: 5,
			colors: ['#1a56db'],
			strokeWidth: 2,
			strokeColors: '#fff'
		},
		xaxis: {
			categories: semestreLabels,
			title: {
				text: 'Semestre'
			}
		},
		yaxis: {
			min: 0,
			max: 20,
			title: {
				text: 'Promedio'
			}
		},
		tooltip: {
			y: {
				formatter: (value: number) => value.toFixed(2)
			}
		},
		title: {
			text: 'Evolución del Promedio por Semestre',
			align: 'left',
			style: {
				fontSize: '16px',
				fontWeight: 'bold'
			}
		}
	});
	let chart: any;


	onMount(async () => {
		if (browser) {
			const module = await import('svelte-apexcharts');
			chart = module.default;
		}
	});
</script>

<div class="w-full p-4">
	<h2 class="text-2xl font-bold mb-4">
		Hola de nuevo, {data.estudiante.nombre}!
	</h2>

	<div class="grid md:grid-cols-6 gap-6 mb-6">
		<!-- Resumen estadístico -->
		<Card padding="xl" size="none" class="col-span-2">
			<Heading tag="h3" class="mb-4">Resumen Académico</Heading>

			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<P weight="bold" class="text-3xl text-primary-700">{creditosObtenidos}</P>
					<P size="sm">Créditos Obtenidos</P>
				</div>

				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<P weight="bold" class="text-3xl text-red-600">{materiasAplazadas}</P>
					<P size="sm">Materias Aplazadas</P>
				</div>

				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<P weight="bold" class="text-3xl text-primary-700">{promedioGeneral.toFixed(2)}</P>
					<P size="sm">Promedio General</P>
				</div>
			</div>
		</Card>

		<!-- Gráfico de promedio por semestre -->
		<Card padding="xl" size="none" class="col-span-4">
			<Heading tag="h3" class="mb-4">Evolución del Promedio</Heading>

			{#if browser && chart}
				<div class="h-64" use:chart={options}></div>
			{/if}
		</Card>
		<div
			class={(!data.inscripcionAbierta ? 'col-span-3' : '') + " flex flex-col justify-center items-start mb-6 col-span-half"}>
			<h3 class="text-lg font-semibold mr-3">Estado de inscripción:</h3>
			{#if data.inscripcionAbierta}
				<Badge color="green">Abierta</Badge>
			{:else}
				<Badge color="red">Cerrada</Badge>
			{/if}
			<!-- Materias inscritas -->
			<Card padding="xl" class="mb-6" size="none">
				<Heading tag="h3" class="mb-4">Materias Inscritas</Heading>

				{#if data.materiasInscritas.length > 0}
					<Table striped={true} hoverable={true}>
						<TableHead>
							<TableHeadCell>Materia</TableHeadCell>
							<TableHeadCell>Código</TableHeadCell>
							<TableHeadCell>Docente</TableHeadCell>
							<TableHeadCell>Créditos</TableHeadCell>
							<TableHeadCell>Acciones</TableHeadCell>
						</TableHead>
						<TableBody>
							{#each data.materiasInscritas as materia}
								<TableBodyRow>
									<TableBodyCell>{materia.nombre}</TableBodyCell>
									<TableBodyCell>{materia.id}</TableBodyCell>
									<TableBodyCell>{materia.docente}</TableBodyCell>
									<TableBodyCell>{materia.unidad_credito}</TableBodyCell>
									<TableBodyCell>
										<form
											method="POST"
											use:enhance={({formData}) => {
												formData.set("materia", materia.id)
												return async ({ result, update }) => {
													const { base64, type } = result.data;

													const byteCharacters = atob(base64);
													const byteArrays = [new Uint8Array(byteCharacters.length)];

													for (let i = 0; i < byteCharacters.length; i++) {
														byteArrays[0][i] = byteCharacters.charCodeAt(i);
													}

													console.log(type)
													const blob = new Blob(byteArrays, { type });
													const extension = type.split("/")[1] || "bin";

													const url = URL.createObjectURL(blob);
													const a = document.createElement('a');
													a.href = url;
													a.download = `planificacion.${extension}`;
													a.click();
													URL.revokeObjectURL(url);
													await update();
												};
											}}
											class="space-y-6"
										>
											<Button color="primary" class="p-2! grid place-content-center" pill type="submit">
												<FileLinesOutline class="h-5 w-5" />
											</Button>
											<Tooltip>Descargar planificación</Tooltip>
										</form>
									</TableBodyCell>
								</TableBodyRow>
							{/each}
						</TableBody>
					</Table>
				{:else}
					<Alert color="info">No tienes materias inscritas actualmente</Alert>
				{/if}

				{#if data.inscripcionAbierta}
					<div class="mt-6">
						<Button color="primary" href="/estudiante/horario">Ir a inscripción de materias</Button>
					</div>
				{/if}
			</Card>
		</div>

		<!-- Histórico de materias -->
		{#if data.historicoMaterias.length > 0}
			<Card padding="xl" size="none" class={!data.inscripcionAbierta ? 'col-span-3' : 'col-span-2'}>
				<Heading tag="h3" class="mb-4">Histórico de Materias</Heading>

				<Table striped={true} hoverable={true}>
					<TableHead>
						<TableHeadCell>Materia</TableHeadCell>
						<TableHeadCell>Ciclo</TableHeadCell>
						<TableHeadCell>Docente</TableHeadCell>
						<TableHeadCell>Nota</TableHeadCell>
						<TableHeadCell>Estatus</TableHeadCell>
					</TableHead>
					<TableBody>
						{#each data.historicoMaterias as materia}
							<TableBodyRow>
								<TableBodyCell>{materia.id}</TableBodyCell>
								<TableBodyCell>{materia.ciclo}</TableBodyCell>
								<TableBodyCell>{materia.docente}</TableBodyCell>
								<TableBodyCell>{materia.promedio}</TableBodyCell>
								<TableBodyCell>
									{#if materia.estatus === 'Aprobada'}
										<Badge color="green">{materia.estatus}</Badge>
									{:else if materia.estatus === 'Reprobada'}
										<Badge color="red">{materia.estatus}</Badge>
									{:else}
										<Badge color="blue">{materia.estatus}</Badge>
									{/if}
								</TableBodyCell>
							</TableBodyRow>
						{/each}
					</TableBody>
				</Table>
			</Card>
		{/if}

		<!-- Materias disponibles -->
		{#if data.materiasDisponibles.length > 0}
			<Card padding="xl" size="none" class={data.historicoMaterias.length === 0 ? 'col-span-2' : ''}>
				<Heading tag="h3" class="mb-4">Materias Disponibles</Heading>

				<Table striped={true} hoverable={true}>
					<TableHead>
						<TableHeadCell>Materia</TableHeadCell>
						<TableHeadCell>Código</TableHeadCell>
						<TableHeadCell>U. C.</TableHeadCell>
						<TableHeadCell>Prelación</TableHeadCell>
						<TableHeadCell>Carrera</TableHeadCell>
					</TableHead>
					<TableBody>
						{#each data.materiasDisponibles as materia}
							<TableBodyRow>
								<TableBodyCell>{materia.nombre}</TableBodyCell>
								<TableBodyCell>{materia.id}</TableBodyCell>
								<TableBodyCell>{materia.unidad_credito}</TableBodyCell>
								<TableBodyCell>{materia.prelacion || 'Ninguna'}</TableBodyCell>
								<TableBodyCell>{materia.carrera.nombre}</TableBodyCell>
							</TableBodyRow>
						{/each}
					</TableBody>
				</Table>
			</Card>
		{/if}
	</div>
</div>

