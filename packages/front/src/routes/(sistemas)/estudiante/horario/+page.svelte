<script lang="ts">
	import { Card, Button, Modal, Popover, Toast } from 'flowbite-svelte';
	import {
		CalendarWeekOutline,
		ClockOutline,
		CloseOutline,
		PlusOutline,
		XSolid
	} from 'flowbite-svelte-icons';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import type { PageData } from './$types';
	import type { MateriaDisponible } from '../../../../app';
	import { slide } from 'svelte/transition';

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
	let materias: HorarioMateria[] = $state([]);

	let openModal = $state(false);

	// Toast
	let mostrarToast = $state(false);
	let mensajeToast = $state('');

	const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
	const horas = Array.from({ length: 14 }, (_, i) => {
		const hora = i + 7;
		return hora < 10 ? `0${hora}:00` : `${hora}:00`;
	});

	function horaAMinutos(hora: string): number {
		const [horas, minutos] = hora.split(':').map(Number);
		return horas * 60 + minutos;
	}

	function calcularPosicionMateria(materia: HorarioMateria) {
		const inicioMinutos = horaAMinutos(materia.hora_inicio);
		const finMinutos = horaAMinutos(materia.hora_fin);
		const horaInicioHorario = 7 * 60; // 7:00 AM
		const top = ((inicioMinutos - horaInicioHorario) / 60) * 4; // 4rem por hora
		const duracionHoras = (finMinutos - inicioMinutos) / 60;
		const height = duracionHoras * 4; // 4rem por hora
		const diaIndex = dias.indexOf(materia.dia);
		const colWidth = 100 / 7;
		const leftOffset = colWidth;
		const left = leftOffset + diaIndex * colWidth;

		return {
			top: `${top}rem`,
			height: `${height}rem`,
			left: `${left}%`,
			width: `${colWidth}%`
		};
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

	function formatearHorario(inicio: string, fin: string): string {
		return `${inicio} - ${fin}`;
	}

	function getColorClass(color: string, isConflict: boolean): string {
		const baseClass = isConflict ? 'border-2 border-dashed ' : '';

		switch (color) {
			case 'blue':
				return `${baseClass}bg-blue-100 ${isConflict ? 'border-red-500' : ''}`;
			case 'green':
				return `${baseClass}bg-green-100 ${isConflict ? 'border-red-500' : ''}`;
			case 'purple':
				return `${baseClass}bg-purple-100 ${isConflict ? 'border-red-500' : ''}`;
			case 'yellow':
				return `${baseClass}bg-yellow-100 ${isConflict ? 'border-red-500' : ''}`;
			case 'red':
				return `${baseClass}bg-red-100 ${isConflict ? 'border-red-500' : ''}`;
			case 'pink':
				return `${baseClass}bg-pink-100 ${isConflict ? 'border-red-500' : ''}`;
			case 'indigo':
				return `${baseClass}bg-indigo-100 ${isConflict ? 'border-red-500' : ''}`;
			default:
				return `${baseClass}bg-gray-100 ${isConflict ? 'border-red-500' : ''}`;
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
				carrera: materia.carrera.nombre
			});
		});
		for (let i = 0; i < materias.length; i++) {
			materias[i].color = materias[0].color;
		}
		verificarConflictos();
	}

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
</script>

<!-- Vista -->
<div class="container mx-auto p-4 bg-white">
	<h1 class="text-2xl font-bold text-center mb-6">Horario de clases</h1>

	<div class="overflow-x-auto mb-6">
		<div class="min-w-[768px] relative">
			<div class="grid grid-cols-7 border-b">
				<div class="p-2 font-semibold text-center border-r w-16"></div>
				<!-- Fijamos w-16 -->
				{#each dias as dia, index}
					<div class="p-2 font-semibold text-center border-r {index === 0 ? 'text-left' : ''}">{dia}</div>
				{/each}
			</div>

			<div class="relative">
				{#each horas as hora}
					<div class="grid grid-cols-7 border-b">
						<div class="p-2 text-sm text-center border-r w-16">{hora}</div>
						<!-- También w-16 -->
						{#each dias as dia}
							<div class="h-16 border-r"></div>
						{/each}
					</div>
				{/each}

				{#each materias as materia}
					{@const posicion = calcularPosicionMateria(materia)}
					<div
						class="absolute px-1 py-1"
						style="top: {posicion.top}; height: {posicion.height}; left: {posicion.left}; width: {posicion.width};"
					>
						<Card
							padding="sm"
							class="{getColorClass(
								materia.color,
								materia.conflicto
							)} h-full overflow-hidden relative"
						>
							<Button
								color="none"
								class="absolute -top-0 right-0 p-1!"
								pill
								on:click={() => quitarMateriaPorID(materia.id)}
								><CloseOutline class="w-6 h-6" /></Button
							>
							<div class="flex flex-col h-full justify-between">
								<h5 class="text-sm font-bold tracking-tight text-gray-900 truncate">
									{materia.nombre}
								</h5>
								<div class="flex items-center text-xs mt-1">
									<ClockOutline class="w-3 h-3 mr-1" />
									<span>{formatearHorario(materia.hora_inicio, materia.hora_fin)}</span>
								</div>
								{#if materia.conflicto}
									<div class="text-xs text-red-600 font-semibold mt-1">¡Conflicto!</div>
								{/if}
							</div>
						</Card>
					</div>
				{/each}
			</div>
		</div>
	</div>

	<!-- Botones -->
	<div class="flex flex-wrap justify-center gap-4 mt-6">
		<Button color="blue" on:click={() => (openModal = true)}>
			<CalendarWeekOutline class="mr-2 h-5 w-5" />
			Seleccionar Materias
		</Button>
		<Button color="green" disabled={materias.some((m) => m.conflicto)}>
			<CalendarWeekOutline class="mr-2 h-5 w-5" />
			Registrar Horario
		</Button>
	</div>

	<!-- Modal Seleccionar Materias -->
	<Modal bind:open={openModal} size="xl" class="min-h-[500px]">
		<div slot="header" class="text-lg font-semibold">Seleccionar Materias</div>

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
									on:click={() => quitarMateriaPorID(materia.id)}>Quitar</Button
								>
							{:else}
								<Button
									size="xs"
									class="mt-2"
									type="button"
									on:click={() => agregarMateria(materia)}>Agregar</Button
								>
							{/if}
						</div>
					</Popover>
				</div>
			{/each}
		</div>

		<div slot="footer" class="flex justify-end p-4">
			<Button color="alternative" on:click={() => (openModal = false)}>Cerrar</Button>
		</div>
	</Modal>

	<!-- Toast Conflicto -->
	{#if mostrarToast}
		<Toast on:close={() => (mostrarToast = false)} color="primary" class="fixed bottom-4 right-4">
			{mensajeToast}
		</Toast>
	{/if}
</div>
