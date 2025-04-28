import { obtenerHistoricoMaterias, obtenerMateriasDisponibles, obtenerMateriasInscritas } from "$lib";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({fetch, locals:{usuario}}) => {
	try {
		// Obtener datos
		const materiasInscritas = await obtenerMateriasInscritas(fetch);
		const historicoMaterias = await obtenerHistoricoMaterias(fetch);
		const materiasDisponibles = await obtenerMateriasDisponibles(fetch, usuario?.cedula ?? '');

    console.log(materiasDisponibles);
    console.log(historicoMaterias);


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
