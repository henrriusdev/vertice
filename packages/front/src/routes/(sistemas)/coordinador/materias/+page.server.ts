import {
	actualizarMateria,
	crearMateria,
	obtenerCarreras,
	obtenerDocentes,
	obtenerMaterias,
	toggleMateriaStatus
} from '$lib';
import type { MateriaReq } from '$lib/types';
import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, parent }) => {
	const parentData = await parent();
	const { rol, nombre } = parentData;
	
	// Only coordinators can access this page
	if (rol !== 'coordinador') {
		redirect(302, '/' + rol);
	}

	try {
		const data = await obtenerMaterias(fetch);
		const carreras = await obtenerCarreras(fetch);
		const docentes = await obtenerDocentes(fetch);

		// Get coordinator's carrera_id if available from parent data
		const carrera_id = (parentData as any).carrera_id || null;

		return { 
			materias: data.materias, 
			carreras, 
			docentes, 
			rol,
			nombre,
			carrera_id
		};
	} catch (error) {
		console.error('Error al obtener las materias:', error);
		return { materias: [], carreras: [], docentes: [], rol, nombre, carrera_id: null };
	}
};

export const actions: Actions = {
	toggleStatus: async ({ request, fetch }) => {
		const formData = await request.formData();
		const id = formData.get('id') as string;
		
		try {
			const response = await toggleMateriaStatus(fetch, id);
			
			if (response.ok) {
				const data = await response.json();
				return {
					type: 'success',
					message: 'Estado de la materia actualizado exitosamente',
					activo: data.data.activo
				};
			}
			
			const error = await response.json();
			return {
				type: 'failure',
				message: error.data.message || 'Error al actualizar el estado de la materia'
			};
		} catch (error) {
			console.error('Error en toggleStatus:', error);
			return {
				type: 'failure',
				message: 'Error al actualizar el estado de la materia'
			};
		}
	},
	
	create: async ({ request, fetch }) => {
		const form = await request.formData();
		// Helper function for safe number conversion
		const safeNumber = (value: FormDataEntryValue | null, defaultValue = 0): number => {
			if (!value) return defaultValue;
			const num = Number(value);
			return isNaN(num) ? defaultValue : num;
		};

		const payload: MateriaReq = {
			id: form.get('id')?.toString() || '',
			nombre: form.get('nombre')?.toString() || '',
			prelacion: form.get('prelacion')?.toString() || '',
			unidad_credito: safeNumber(form.get('unidad_credito')),
			hp: safeNumber(form.get('hp')),
			ht: safeNumber(form.get('ht')),
			semestre: safeNumber(form.get('semestre'), 1),
			id_carrera: safeNumber(form.get('id_carrera')).toString(),
			horarios: JSON.parse(form.get('horarios')?.toString() || '[]'),
			ciclo: form.get('ciclo')?.toString() || '',
			maximo: safeNumber(form.get('maximo'), 30),
			id_docente: safeNumber(form.get('id_docente')).toString()
		};

		// Validate schedule conflicts
		const conflictos = await validarConflictosHorario(fetch, payload);
		if (conflictos.length > 0) {
			return {
				type: 'failure',
				message: `Conflicto de horario detectado: ${conflictos.join(', ')}`
			};
		}

		const errores = validarPayload(payload);
		if (Object.keys(errores).length > 0) {
			const errorMessages = Object.values(errores).join(', ');
			return {
				type: 'failure',
				message: errorMessages
			};
		}

		try {
			await crearMateria(fetch, payload);
			return {
				type: 'success',
				message: 'Materia creada exitosamente',
				invalidate: true
			};
		} catch (error) {
			console.error('Error al crear materia:', error);
			return { type: 'failure', message: error instanceof Error ? error.message : 'Error desconocido' };
		}
	},

	edit: async ({ request, fetch }) => {
		const form = await request.formData();
		// Helper function for safe number conversion
		const safeNumber = (value: FormDataEntryValue | null, defaultValue = 0): number => {
			if (!value) return defaultValue;
			const num = Number(value);
			return isNaN(num) ? defaultValue : num;
		};

		const payload: MateriaReq & { id: string } = {
			id: form.get('id')?.toString() as string,
			nombre: form.get('nombre')?.toString() as string,
			prelacion: form.get('prelacion')?.toString() as string,
			unidad_credito: safeNumber(form.get('unidad_credito')),
			hp: safeNumber(form.get('hp')),
			ht: safeNumber(form.get('ht')),
			semestre: safeNumber(form.get('semestre'), 1),
			id_carrera: safeNumber(form.get('id_carrera')).toString(),
			horarios: JSON.parse(form.get('horarios')?.toString() || '[]'),
			ciclo: form.get('ciclo')?.toString() as string,
			maximo: safeNumber(form.get('maximo'), 30),
			id_docente: safeNumber(form.get('id_docente')).toString()
		};

		// Validate schedule conflicts (excluding current materia)
		const conflictos = await validarConflictosHorario(fetch, payload, payload.id);
		if (conflictos.length > 0) {
			return {
				type: 'failure',
				message: `Conflicto de horario detectado: ${conflictos.join(', ')}`
			};
		}

		const errores = validarPayload(payload);
		if (Object.keys(errores).length > 0) {
			const errorMessages = Object.values(errores).join(', ');
			return {
				type: 'failure',
				message: errorMessages
			};
		}

		try {
			await actualizarMateria(fetch, payload.id, payload);
			return {
				type: 'success',
				message: 'Materia actualizada exitosamente',
				invalidate: true
			};
		} catch (error) {
			console.error('Error al editar materia:', error);
			return { type: 'failure', message: error instanceof Error ? error.message : 'Error desconocido' };
		}
	},
};

async function validarConflictosHorario(
	fetch: typeof window.fetch, 
	materia: MateriaReq, 
	excludeId?: string
): Promise<string[]> {
	try {
		const data = await obtenerMaterias(fetch);
		const materias = data.materias.filter(m => 
			m.semestre === materia.semestre && 
			m.id_carrera === Number(materia.id_carrera) &&
			m.id !== excludeId &&
			m.activo !== false
		);

		const conflictos: string[] = [];

		for (const horario of materia.horarios) {
			for (const otraMateria of materias) {
				for (const otroHorario of otraMateria.horarios) {
					if (horario.dia === otroHorario.dia) {
						const inicioA = horaAMinutos(horario.hora_inicio);
						const finA = horaAMinutos(horario.hora_fin);
						const inicioB = horaAMinutos(otroHorario.hora_inicio);
						const finB = horaAMinutos(otroHorario.hora_fin);

						if (inicioA < finB && finA > inicioB) {
							conflictos.push(`${otraMateria.nombre} (${horario.dia} ${horario.hora_inicio}-${horario.hora_fin})`);
						}
					}
				}
			}
		}

		return conflictos;
	} catch (error) {
		console.error('Error validating schedule conflicts:', error);
		return [];
	}
}

function horaAMinutos(hora: string): number {
	const [h, m] = hora.split(':').map(Number);
	return h * 60 + m;
}

function validarPayload(
	payload: Record<string, string | number | boolean>
): Record<string, string> {
	const errores: Record<string, string> = {};
	const camposBase: (keyof typeof payload)[] = [
		'nombre',
		'semestre',
		'id_carrera',
		'maximo'
	];

	for (const campo of camposBase) {
		const valor = payload[campo];
		if (!valor || valor.toString().trim() === '') {
			errores[campo] = `El campo ${campo} es requerido`;
		}
	}

	return errores;
}