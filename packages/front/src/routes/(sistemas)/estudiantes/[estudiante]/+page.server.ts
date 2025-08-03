import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { obtenerEstudiantes } from '$lib';

export const load: PageServerLoad = async ({ params, fetch, parent }) => {
	const { rol } = await parent();
	
	// Only allow these roles to view student details
	if (!['caja', 'administrador', 'coordinador', 'control'].includes(rol)) {
		redirect(302, '/' + rol);
	}

	const cedula = params.estudiante;

	try {
		// Get all students and find the one with the matching cedula
		const estudiantes = await obtenerEstudiantes(fetch);
		const estudiante = estudiantes.find(est => est.cedula === cedula);

		if (!estudiante) {
			throw error(404, 'Estudiante no encontrado');
		}

		// For now, return basic student data
		// TODO: Add functions to get student's academic history
		return {
			estudiante,
			materiasInscritas: [], // TODO: fetch student's enrolled subjects
			historicoMaterias: [], // TODO: fetch student's academic history
			materiasDisponibles: [], // TODO: fetch available subjects for student
			inscripcionAbierta: false
		};
	} catch (err) {
		console.error('Error loading student data:', err);
		throw error(500, 'Error cargando datos del estudiante');
	}
};