<script lang="ts">
	import {
		Alert,
		Badge,
		Card,
		Button
	} from 'flowbite-svelte';
	import { ArrowLeftOutline } from 'flowbite-svelte-icons';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
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
				<h2 class="text-2xl font-bold">Información del Estudiante</h2>
				<p class="text-gray-600">{data.estudiante.nombre} - {data.estudiante.cedula}</p>
			</div>
		</div>
	</div>

	<div class="grid md:grid-cols-2 gap-6 mb-6">
		<!-- Student Information -->
		<Card class="p-6">
			<h3 class="text-lg font-semibold mb-4">Información Personal</h3>
			<div class="space-y-3">
				<div class="flex justify-between">
					<span class="font-medium">Nombre:</span>
					<span>{data.estudiante.nombre}</span>
				</div>
				<div class="flex justify-between">
					<span class="font-medium">Cédula:</span>
					<span>{data.estudiante.cedula}</span>
				</div>
				<div class="flex justify-between">
					<span class="font-medium">Correo:</span>
					<span>{data.estudiante.correo}</span>
				</div>
				<div class="flex justify-between">
					<span class="font-medium">Dirección:</span>
					<span>{data.estudiante.direccion || 'N/A'}</span>
				</div>
				<div class="flex justify-between">
					<span class="font-medium">Edad:</span>
					<span>{data.estudiante.edad || 'N/A'}</span>
				</div>
				<div class="flex justify-between">
					<span class="font-medium">Fecha de Nacimiento:</span>
					<span>{data.estudiante.fecha_nacimiento || 'N/A'}</span>
				</div>
				<div class="flex justify-between">
					<span class="font-medium">Sexo:</span>
					<span>{data.estudiante.sexo || 'N/A'}</span>
				</div>
			</div>
		</Card>

		<!-- Academic Information -->
		<Card class="p-6">
			<h3 class="text-lg font-semibold mb-4">Información Académica</h3>
			<div class="space-y-3">
				<div class="flex justify-between">
					<span class="font-medium">Carrera:</span>
					<span>{data.estudiante.carrera?.nombre || 'N/A'}</span>
				</div>
				<div class="flex justify-between">
					<span class="font-medium">Semestre:</span>
					<span>{data.estudiante.semestre || 'N/A'}</span>
				</div>
				<div class="flex justify-between">
					<span class="font-medium">Promedio:</span>
					<span>{data.estudiante.promedio || 'N/A'}</span>
				</div>
				<div class="flex justify-between">
					<span class="font-medium">Estado:</span>
					<span>
						{#if data.estudiante.activo}
							<Badge color="green">Activo</Badge>
						{:else}
							<Badge color="red">Inactivo</Badge>
						{/if}
					</span>
				</div>
			</div>
		</Card>
	</div>

	<!-- Information Notice -->
	<Alert color="blue" class="mb-4">
		<span class="font-medium">Nota:</span> La información académica detallada (materias inscritas, histórico académico) 
		no está disponible en esta vista. Esta funcionalidad requiere endpoints adicionales en el backend.
	</Alert>
</div>