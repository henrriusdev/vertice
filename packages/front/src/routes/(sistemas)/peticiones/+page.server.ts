import { obtenerPeticiones } from '$lib/servicios/peticiones';
import type { PageServerLoad } from './$types';

export const load = (async ({ fetch, }) => {
	const peticiones = await obtenerPeticiones(fetch);
	console.log(peticiones);
	return { peticiones };
}) satisfies PageServerLoad;
