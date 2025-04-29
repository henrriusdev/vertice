import {
	obtenerHistoricoMaterias,
	obtenerMateriasDisponibles,
	obtenerMateriasInscritas
} from '$lib';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { MateriaDisponible } from '../../../app';

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
