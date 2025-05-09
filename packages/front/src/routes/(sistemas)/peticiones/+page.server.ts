import { actualizarPeticion, obtenerPeticiones } from '$lib/servicios/peticiones';
import type { Actions, PageServerLoad } from './$types';
import { obtenerDocentes, obtenerEstudiantes } from '$lib';

export const load = (async ({ fetch, }) => {
	const peticiones = await obtenerPeticiones(fetch);
	const docentes = await obtenerDocentes(fetch);
	const estudiantes = await obtenerEstudiantes(fetch);
	return { peticiones, docentes, estudiantes };
}) satisfies PageServerLoad;

export const actions: Actions = {
	aprobar: async ({fetch,request})=> {
		try {
			const data = await request.formData();
			const id = Number(data.get('id'));
			const res = actualizarPeticion(fetch, id, {estado: 'Aprobado'})
			return {success: true}
		} catch (e) {
			console.log(e)
			return {success: false}
		}
	},

	denegar: async ({fetch, request}) => {
		try {
			const data = await request.formData();
			const id = Number(data.get('id'));
			const res = actualizarPeticion(fetch, id, {estado: 'Denegado'})
			return {success: true}
		} catch (e) {
			console.log(e)
			return {success: false}
		}
	}
}