import { obtenerMateria } from '$lib';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load = (async ({ fetch, parent, params }) => {
	const { rol } = await parent();
	if (['estudiante','caja'].includes(rol)) {
		throw redirect(302, '/' + rol);
	}

	const materia = await obtenerMateria(fetch, params.materia);
	return { materia };
}) satisfies PageServerLoad;
