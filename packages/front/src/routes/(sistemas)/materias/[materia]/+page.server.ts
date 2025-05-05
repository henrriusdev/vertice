import { obtenerMateria } from '$lib';
import type { PageServerLoad } from './$types';

export const load = (async ({ fetch, params }) => {
    const materia = await obtenerMateria(fetch, params.materia)
    return {materia};
}) satisfies PageServerLoad;