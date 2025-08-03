import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { 
	obtenerEstudiantes,
	obtenerEstudiantePorCedula,
	obtenerMateriasInscritasPorCedula,
	obtenerHistoricoMateriasPorCedula
} from '$lib';

export const load: PageServerLoad = async ({ params, fetch, parent }) => {
	const { rol } = await parent();
	
	// Only allow these roles to view student details
	if (!['caja', 'administrador', 'coordinador', 'control'].includes(rol)) {
		redirect(302, '/' + rol);
	}

	const cedula = params.estudiante;

	try {
		let estudiante;
		
		// Try to get student by cedula, fallback to searching all students
		try {
			estudiante = await obtenerEstudiantePorCedula(fetch, cedula);
		} catch (e) {
			console.warn('Direct student lookup failed, searching all students:', e);
			const estudiantes = await obtenerEstudiantes(fetch);
			estudiante = estudiantes.find(est => est.cedula === cedula);
			
			if (!estudiante) {
				throw error(404, 'Estudiante no encontrado');
			}
		}

		return {
			estudiante,
			materiasInscritas: await obtenerMateriasInscritasPorCedula(fetch, cedula).catch(() => []),
			historicoMaterias: await obtenerHistoricoMateriasPorCedula(fetch, cedula).catch(() => [])
		};
	} catch (err) {
		console.error('Error loading student data:', err);
		
		// If it's already an error with status, re-throw
		if (err.status) {
			throw err;
		}
		
		// Otherwise create a 404 error
		throw error(404, 'Estudiante no encontrado');
	}
};