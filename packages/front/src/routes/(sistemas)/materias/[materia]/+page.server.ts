import { actualizarNota, obtenerMateria } from '$lib';
import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { crearPeticion } from '$lib/servicios/peticiones';
import type { Peticion } from '../../../../app';

export const load = (async ({ fetch, parent, params }) => {
	const { rol } = await parent();
	if (['estudiante', 'caja'].includes(rol)) {
		throw redirect(302, '/' + rol);
	}

	const materia = await obtenerMateria(fetch, params.materia);
	return { materia };
}) satisfies PageServerLoad;

export const actions: Actions = {
	default: async ({ fetch, request, locals:{usuario} }) => {
		const form = await request.formData();

		let payload = Object.fromEntries(form) as unknown as {
			cedula_estudiante: string;
			nombre_campo: string;
			valor: string | number;
			materia: string;
			peticion?: string;
			observacion?: string;
		};
		console.log(payload)

		const { peticion, observacion } = payload;

		payload = {
			...payload,
			peticion: undefined,
			observacion: undefined,
			valor: Number(payload.valor)
		};

		if (peticion === 'true') {
			const body: Omit<Peticion, "id"> = {
				campo: payload.nombre_campo,
				descripcion: observacion!,
				estado: "Pendiente",
				id_docente: usuario?.id ?? 1,
				id_estudiante: payload.cedula_estudiante,
				id_materia: payload.materia,
			};

			const res = await crearPeticion(fetch, body);
			console.log(res);
			return { success: true };
		}

		const res = await actualizarNota(fetch, payload);
		console.log(res);
		return { success: true };
	}
};
