<script lang="ts">
	import {
		Alert,
		Badge,
		Card,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		Button
	} from 'flowbite-svelte';
	import { ArrowLeftOutline } from 'flowbite-svelte-icons';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	// Calculate statistics
	let creditosObtenidos = $derived(
		data.historicoMaterias
			?.filter((materia) => materia.estatus === 'Aprobada')
			?.reduce((total, materia) => total + (materia.creditos || 0), 0) || 0
	);

	let materiasAplazadas = $derived(
		data?.historicoMaterias.filter((materia) => materia.estatus === 'Reprobada').length || 0
	);

	let promedioGeneral = $derived(
		data.historicoMaterias
			?.filter((materia) => materia.estatus === 'Aprobada')
			?.reduce((sum, materia) => sum + materia.promedio, 0) /
			Math.max(data.historicoMaterias.filter((materia) => materia.estatus === 'Aprobada').length, 1) || 0
	);
</script>

<div class="w-full p-4">
	<div class="flex justify-between items-center mb-6">
		<div class="flex items-center gap-4">
			<Button 
				color="light" 
				onclick={() => window.history.back()}
				class="flex items-center gap-2"
			>
				<ArrowLeftOutline class="h-4 w-4" />
				Volver
			</Button>
			<div>
				<h2 class="text-2xl font-bold">Historial Académico</h2>
				<p class="text-gray-600">{data.estudiante.nombre} - {data.estudiante.cedula}</p>
			</div>
		</div>
	</div>

	<div class="grid md:grid-cols-6 gap-4 mb-6">
		<!-- Academic Summary -->
		<Card class="col-span-2 p-4 max-w-full">
			<h3 class="text-lg font-semibold mb-4">Resumen Académico</h3>

			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<p class="text-3xl font-bold text-primary-700">{creditosObtenidos}</p>
					<p class="text-sm">Créditos Obtenidos</p>
				</div>

				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<p class="text-3xl font-bold text-red-600">{materiasAplazadas}</p>
					<p class="text-sm">Materias Aplazadas</p>
				</div>

				<div class="bg-gray-50 p-4 rounded-lg text-center">
					<p class="text-3xl font-bold text-primary-700">{promedioGeneral.toFixed(2)}</p>
					<p class="text-sm">Promedio General</p>
				</div>
			</div>

			<div class="mt-4">
				<h4 class="text-md font-semibold mb-2">Información del Estudiante</h4>
				<div class="space-y-1 text-sm">
					<p><strong>Carrera:</strong> {data.estudiante.carrera?.nombre || 'N/A'}</p>
					<p><strong>Semestre:</strong> {data.estudiante.semestre}</p>
					<p><strong>Promedio Actual:</strong> {data.estudiante.promedio}</p>
					<p><strong>Estado:</strong> 
						{#if data.estudiante.activo}
							<Badge color="green">Activo</Badge>
						{:else}
							<Badge color="red">Inactivo</Badge>
						{/if}
					</p>
				</div>
			</div>
		</Card>

		<!-- Enrolled Subjects -->
		<Card class="mb-6 p-4 max-w-full col-span-2">
			<h3 class="text-lg font-semibold mb-4">Materias Inscritas</h3>

			{#if data.materiasInscritas.length > 0}
				<Table striped={true}>
					<TableHead>
						<TableHeadCell>Materia</TableHeadCell>
						<TableHeadCell>Código</TableHeadCell>
						<TableHeadCell>Docente</TableHeadCell>
						<TableHeadCell>Créditos</TableHeadCell>
					</TableHead>
					<TableBody>
						{#each data.materiasInscritas as materia}
							<TableBodyRow>
								<TableBodyCell>{materia.nombre}</TableBodyCell>
								<TableBodyCell>{materia.id}</TableBodyCell>
								<TableBodyCell>{materia.docente}</TableBodyCell>
								<TableBodyCell>{materia.unidad_credito || 'N/A'}</TableBodyCell>
							</TableBodyRow>
						{/each}
					</TableBody>
				</Table>
			{:else}
				<Alert color="primary">El estudiante no tiene materias inscritas actualmente</Alert>
			{/if}
		</Card>

		<!-- Academic History -->
		{#if data.historicoMaterias.length > 0}
			<Card class="col-span-2 max-w-full p-4">
				<h3 class="text-lg font-semibold mb-4">Histórico de Materias</h3>

				<Table striped={true} hoverable={true}>
					<TableHead>
						<TableHeadCell>Materia</TableHeadCell>
						<TableHeadCell>Ciclo</TableHeadCell>
						<TableHeadCell>Docente</TableHeadCell>
						<TableHeadCell>Promedio</TableHeadCell>
						<TableHeadCell>Estatus</TableHeadCell>
					</TableHead>
					<TableBody>
						{#each data.historicoMaterias as materia}
							<TableBodyRow>
								<TableBodyCell>{materia.nombre}</TableBodyCell>
								<TableBodyCell>{materia.ciclo}</TableBodyCell>
								<TableBodyCell>{materia.docente}</TableBodyCell>
								<TableBodyCell>{materia.promedio.toFixed(2)}</TableBodyCell>
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
		{:else}
			<Card class="col-span-2 max-w-full p-4">
				<h3 class="text-lg font-semibold mb-4">Histórico de Materias</h3>
				<Alert color="primary">No hay materias en el historial académico</Alert>
			</Card>
		{/if}

		<!-- Available Subjects -->
		{#if data.materiasDisponibles.length > 0}
			<Card class="col-span-2 max-w-full p-4">
				<h3 class="text-lg font-semibold mb-4">Materias Disponibles</h3>
				
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