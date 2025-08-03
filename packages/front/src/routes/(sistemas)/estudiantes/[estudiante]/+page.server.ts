import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { 
	obtenerEstudiantes,
	obtenerEstudiantePorCedula, 
	obtenerMateriasInscritasPorCedula, 
	obtenerHistoricoMateriasPorCedula,
	obtenerMateriasDisponibles
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
		
		// Get student's academic data with fallbacks
		let materiasInscritas = [];
		let historicoMaterias = [];
		let materiasDisponibles = [];

		try {
			materiasInscritas = await obtenerMateriasInscritasPorCedula(fetch, cedula);
		} catch (e) {
			console.warn('Error fetching enrolled subjects for student, using empty array:', e);
		}

		try {
			historicoMaterias = await obtenerHistoricoMateriasPorCedula(fetch, cedula);
		} catch (e) {
			console.warn('Error fetching academic history for student, using empty array:', e);
		}

		try {
			materiasDisponibles = await obtenerMateriasDisponibles(fetch, cedula);
		} catch (e) {
			console.warn('Error fetching available subjects for student, using empty array:', e);
		}

		// Determine if inscription is open based on number of enrolled subjects
		const inscripcionAbierta = materiasInscritas.length <= 2;

		return {
			estudiante,
			materiasInscritas,
			historicoMaterias,
			materiasDisponibles,
			inscripcionAbierta
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