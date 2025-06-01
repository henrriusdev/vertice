<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button, Card, Modal, Popover, Spinner, Toast } from 'flowbite-svelte';
	import {
		CalendarWeekOutline,
		ClockOutline,
		CloseOutline,
		PlusOutline
	} from 'flowbite-svelte-icons';
	import { slide } from 'svelte/transition';
	import type { MateriaDisponible } from '../../../../app';
	import type { PageData } from './$types';
	import { GrillaHorario } from '$lib';
	import { resolver } from '$lib/utilidades/resolver';
	import type { SubmitFunction } from '@sveltejs/kit';

	// Tipos
	type HorarioMateria = {
		id: string;
		nombre: string;
		dia: 'Lunes' | 'Martes' | 'Miércoles' | 'Jueves' | 'Viernes' | 'Sábado';
		hora_inicio: string;
		hora_fin: string;
		color?: string;
		conflicto?: boolean;
		unidad_credito?: number;
		prelacion?: string | null;
		carrera?: string;
	};

	let { data }: { data: PageData } = $props();

	let materiasDisponibles = $state<MateriaDisponible[]>(data.materiasDisponibles);
	let materias: (HorarioMateria & { editable: boolean })[] = $state([]);

	let openModal = $state(false);
	let isLoading = $state(false);

	const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

	function horaAMinutos(hora: string): number {
		const [horas, minutos] = hora.split(':').map(Number);
		return horas * 60 + minutos;
	}

	function verificarConflictos() {
		let conflictoDetectado = false;

		for (let i = 0; i < materias.length; i++) {
			materias[i].conflicto = false;
		}

		for (let i = 0; i < materias.length; i++) {
			for (let j = i + 1; j < materias.length; j++) {
				const materiaA = materias[i];
				const materiaB = materias[j];

				if (materiaA.dia === materiaB.dia) {
					const inicioA = horaAMinutos(materiaA.hora_inicio);
					const finA = horaAMinutos(materiaA.hora_fin);
					const inicioB = horaAMinutos(materiaB.hora_inicio);
					const finB = horaAMinutos(materiaB.hora_fin);

					if ((inicioA < finB && finA > inicioB) || (inicioB < finA && finB > inicioA)) {
						materiaA.conflicto = true;
						materiaB.conflicto = true;
						conflictoDetectado = true;
					}
				}
			}
		}

		if (conflictoDetectado) {
			mensajeToast = 'Hay conflictos en tu horario. Corrige antes de registrar.';
			mostrarToast = true;
		}
	}

	function agregarMateria(materia: any) {
		const horarios = materia.horarios || [];
		horarios.forEach((horario: any) => {
			materias.push({
				id: materia.id,
				nombre: materia.nombre,
				dia: horario.dia,
				hora_inicio: horario.hora_inicio,
				hora_fin: horario.hora_fin,
				color: getRandomColor(),
				conflicto: false,
				unidad_credito: materia.creditos,
				prelacion: materia.prelacion,
				carrera: materia.carrera.nombre,
				editable: true
			});
		});
		replaceMateriaColor();
		verificarConflictos();
	}

	function replaceMateriaColor() {
		for (let i = 0; i < materias.length; i++) {
			let m = materias.find((mat) => mat.id === materias[i].id);
			materias[i].color = m?.color;
		}
	}

	$effect(() => {
		if (data.materiasInscritas.length > 0 && materias.length === 0) {
			data.materiasInscritas.forEach((materia) => {
				const horarios = materia.horarios || [];
				horarios.forEach((horario: any) => {
					materias.push({
						id: materia.id,
						nombre: materia.nombre,
						dia: horario.dia,
						hora_inicio: horario.hora_inicio,
						hora_fin: horario.hora_fin,
						color: getRandomColor(),
						conflicto: false,
						editable: false
					});
				});
			});
			replaceMateriaColor();
			verificarConflictos();
		}
	});

	function quitarMateriaPorID(materiaId: string) {
		materias = materias.filter((m) => m.id !== materiaId);
		verificarConflictos();
	}

	function getRandomColor() {
		const colors = [
			'blue',
			'green',
			'purple',
			'yellow',
			'red',
			'pink',
			'indigo',
			'gray',
			'orange',
			'cyan',
			'teal',
			'violet',
			'lime',
			'sky',
			'amber'
		];
		return colors[Math.floor(Math.random() * colors.length)];
	}

	const handleSubmit: SubmitFunction = () => {
		return resolver(() => (isLoading = false));
	};
</script>

<!-- Vista -->
<div class="container mx-auto p-4 bg-white">
	<h1 class="text-2xl font-bold text-center mb-6">Horario de clases</h1>

	<GrillaHorario {materias} docente={false} />

	<!-- Botones -->
	<div class="flex flex-wrap justify-center gap-4 mt-6">
		<Button color="blue" onclick={() => (openModal = true)} disabled={!data.inscripcionAbierta}>
			<CalendarWeekOutline class="mr-2 h-5 w-5" />
			Seleccionar Materias
		</Button>
		<form use:enhance={handleSubmit} method="post">
			{#each materias as materia}
				<input type="hidden" name="materias" value={materia.id} />
			{/each}
			<Button
				type="submit"
				color="green"
				disabled={materias.some((m) => m.conflicto) ||
					!data.inscripcionAbierta ||
					materias.length === 0 ||
					isLoading}
			>
				{#if isLoading}
					<Spinner class="me-3" size="4" color="gray" />
					Cargando ...
				{:else}
					<CalendarWeekOutline class="mr-2 h-5 w-5" />
					Registrar Horario
				{/if}
			</Button>
		</form>
	</div>

	<!-- Modal Seleccionar Materias -->
	<Modal bind:open={openModal} size="xl" class="min-h-[500px]">
		{#snippet header()}
			<div class="text-lg font-semibold">Seleccionar Materias</div>
		{/snippet}

		<div class="p-4 flex flex-wrap justify-start gap-4">
			{#each materiasDisponibles as materia}
				<div class="relative">
					<Button color="light" type="button" id="materia-{materia.id}">
						<PlusOutline class="mr-2 h-5 w-5" />
						{materia.nombre}
					</Button>

					<Popover
						triggeredBy="#materia-{materia.id}"
						placement="bottom"
						class="w-64 text-sm"
						transition={slide}
					>
						<div class="p-2">
							<p><span class="font-semibold">Créditos:</span> {materia.creditos}</p>
							<p><span class="font-semibold">Prelación:</span> {materia.prelacion || 'Ninguna'}</p>
							<p><span class="font-semibold">Carrera:</span> {materia.carrera.nombre}</p>
							{#if materias.some((m) => m.id === materia.id)}
								<Button
									size="xs"
									class="mt-2"
									type="button"
									onclick={() => quitarMateriaPorID(materia.id)}>Quitar</Button
								>
							{:else}
								<Button size="xs" class="mt-2" type="button" onclick={() => agregarMateria(materia)}
									>Agregar</Button
								>
							{/if}
						</div>
					</Popover>
				</div>
			{/each}
		</div>

		{#snippet footer()}
			<div class="flex justify-end p-4">
				<Button color="alternative" onclick={() => (openModal = false)}>Cerrar</Button>
			</div>
		{/snippet}
	</Modal>
</div>

<style>
	.custom-cols {
		grid-template-columns: 4rem repeat(6, 1fr);
	}
</style>
