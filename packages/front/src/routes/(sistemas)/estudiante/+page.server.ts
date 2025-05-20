import {
	obtenerHistoricoMaterias,
	obtenerMateriasDisponibles,
	obtenerMateriasInscritas
} from '$lib';
import { error } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import type { MateriaDisponible } from '../../../app';
import { obtenerPlanificacion } from '$lib/servicios/archivos';

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
	default: async ({ request, fetch }) => {
		const formData = await request.formData();
		const materia = formData.get('materia') as string;

		try {
			const { base64, type } = await obtenerPlanificacion(fetch, materia);
			return {base64, type}
		} catch (error) {
			console.error(error);
			return { success: false, error: 'Error al inscribir materias' };
		}
	}
}