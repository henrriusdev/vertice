<script lang="ts">
	// Componente reusable SOLO PARA VISUALIZAR la grilla de materias
	import { Card } from 'flowbite-svelte';
	import { ClockOutline } from 'flowbite-svelte-icons';

	let {
		materias: mats = [],
		docente = false
	}: {
		materias: {
			id: string;
			nombre: string;
			dia: 'Lunes' | 'Martes' | 'Miércoles' | 'Jueves' | 'Viernes' | 'Sábado';
			hora_inicio: string;
			hora_fin: string;
			color?: string;
			conflicto?: boolean;
		}[];
		docente: boolean;
	} = $props();

	const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
	const horas = Array.from({ length: 14 }, (_, i) => `${(i + 7).toString().padStart(2, '0')}:00`);

	function horaAMinutos(hora: string): number {
		const [h, m] = hora.split(':').map(Number);
		return h * 60 + m;
	}

	function calcularPosicionMateria(materia: (typeof materias)[0]) {
		const inicio = horaAMinutos(materia.hora_inicio);
		const fin = horaAMinutos(materia.hora_fin);
		const top = ((inicio - 420) / 60) * 4; // 7:00 AM = 420min
		const height = ((fin - inicio) / 60) * 4;
		const diaIndex = dias.indexOf(materia.dia);
		const colWidth = 97 / 6;
		return {
			top: `${top}rem`,
			height: `${height}rem`,
			left: `calc(${diaIndex * colWidth}% + 60px)`,
			width: `${colWidth}%`
		};
	}

	function formatearHorario(inicio: string, fin: string) {
		return `${inicio} - ${fin}`;
	}

	function getColorClass(color: string, conflicto?: boolean): string {
		const base = conflicto ? 'border-2 border-dashed border-red-500' : '';
		const map = {
			blue: 'bg-blue-100',
			green: 'bg-green-100',
			purple: 'bg-purple-100',
			yellow: 'bg-yellow-100',
			red: 'bg-red-100',
			pink: 'bg-pink-100',
			indigo: 'bg-indigo-100',
			gray: 'bg-gray-100',
			orange: 'bg-orange-100',
			cyan: 'bg-cyan-100',
			teal: 'bg-teal-100',
			violet: 'bg-violet-100',
			lime: 'bg-lime-100',
			sky: 'bg-sky-100',
			amber: 'bg-amber-100'
		};
		return `${base} ${map[color] || 'bg-gray-100'}`;
	}

	const colorMap = new Map<string, string>();

	function getColorById(id: string): string {
		if (colorMap.has(id)) return colorMap.get(id)!;

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
			'amber',
			'rose',
			'emerald',
			'fuchsia',
			'stone'
		];

		let hash = 0;
		for (let i = 0; i < id.length; i++) {
			hash = id.charCodeAt(i) + ((hash << 5) - hash);
		}
		const index = Math.abs(hash) % colors.length;
		const color = colors[index];

		colorMap.set(id, color);
		return color;
	}

	let materias = $derived(
		verificarConflictos(
			mats.map((m) => ({
				...m,
				color: m.color || getColorById(m.id)
			}))
		)
	);

	function verificarConflictos(materias: typeof mats): typeof materias {
		const actualizadas = materias.map((m) => ({ ...m, conflicto: false }));

		for (let i = 0; i < actualizadas.length; i++) {
			for (let j = i + 1; j < actualizadas.length; j++) {
				const a = actualizadas[i];
				const b = actualizadas[j];

				if (a.dia === b.dia) {
					const aInicio = horaAMinutos(a.hora_inicio);
					const aFin = horaAMinutos(a.hora_fin);
					const bInicio = horaAMinutos(b.hora_inicio);
					const bFin = horaAMinutos(b.hora_fin);

					if (aInicio < bFin && aFin > bInicio) {
						a.conflicto = true;
						b.conflicto = true;
					}
				}
			}
		}

		return actualizadas;
	}
</script>

<div class="container mx-auto p-4 bg-white">
	{#if docente}
		<h1 class="text-xl font-bold text-center mb-4">Horario</h1>
	{/if}

	<div class="overflow-x-auto">
		<div class="min-w-[768px] relative">
			<div class="grid custom-cols border-b">
				<div class="p-2 text-center font-semibold border-r w-20">Hora</div>
				{#each dias as dia}
					<div class="p-2 text-center font-semibold border-r">{dia}</div>
				{/each}
			</div>

			<div class="relative">
				{#each horas as hora}
					<div class="grid custom-cols border-b">
						<div class="p-2 text-sm text-center border-r w-20">{hora}</div>
						{#each dias as _}
							<div class="h-16 border-r"></div>
						{/each}
					</div>
				{/each}

				{#each materias as materia}
					{@const pos = calcularPosicionMateria(materia)}
					<div
						class="absolute px-1 py-1"
						style="top: {pos.top}; height: {pos.height}; left: {pos.left}; width: {pos.width};"
					>
						<Card
							padding="sm"
							class="{materia.color ? getColorClass(materia.color, materia.conflicto) : ''} h-full"
							href={docente ? `/materias/${materia.id}` : undefined}
						>
							<div class="flex flex-col h-full justify-between">
								<h5 class="text-sm font-bold text-gray-900">{materia.nombre}</h5>
								<div class="flex items-center text-xs mt-1">
									<ClockOutline class="w-3 h-3 mr-1" />
									<span>{formatearHorario(materia.hora_inicio, materia.hora_fin)}</span>
								</div>
							</div>
						</Card>
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>

<style>
	.custom-cols {
		grid-template-columns: 4rem repeat(6, 1fr);
	}
</style>
