import {
	obtenerHistoricoMaterias,
	obtenerMateriasDisponibles,
	obtenerMateriasInscritas
} from '$lib';
import { error } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import type { MateriaDisponible } from '../../../app';
import { obtenerConstancia, obtenerPlanificacion } from '$lib/servicios/archivos';

export const load: PageServerLoad = async ({ fetch, locals: { usuario } }) => {
	try {
		// Obtener datos
		const materiasInscritas = await obtenerMateriasInscritas(fetch);
		const historicoMaterias = await obtenerHistoricoMaterias(fetch);
		console.log(historicoMaterias)
		if (materiasInscritas.length > 2) {
			return {
				estudiante: usuario,
				materiasInscritas,
				historicoMaterias,
				inscripcionAbierta: false,
				materiasDisponibles: [] as MateriaDisponible[]
			};
		}

		const materiasDisponibles = await obtenerMateriasDisponibles(fetch, usuario?.cedula ?? '');
		console.log(historicoMaterias)
		return {
			estudiante: usuario,
			materiasInscritas,
			historicoMaterias,
			materiasDisponibles,
			inscripcionAbierta: true
		};
	} catch (err) {
		console.error(err);
		throw error(500, 'Error cargando datos del estudiante');
	}
};

export const actions: Actions = {
	planificacion: async ({ request, fetch }) => {
		const formData = await request.formData();
		const materia = formData.get('materia') as string;

		try {
			const { base64, type } = await obtenerPlanificacion(fetch, materia);
			return { base64, type }
		} catch (error) {
			console.error(error);
			return { success: false, error: 'Error al inscribir materias' };
		}
	},

	constancia: async ({ locals: {usuario}, fetch }) => {
		const cedula = usuario?.cedula ?? '';
		try {
			const { base64 } = await obtenerConstancia(fetch, cedula);
			return { base64 }
		} catch (error) {
			console.error(error);
			return { success: false, error: 'Error al inscribir materias' };
		}
	}
}