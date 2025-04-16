import { obtenerConfiguracion } from '$lib/servicios/configuracion';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load = (async ({ fetch, locals: { usuario } }) => {
    if (!['superusuario', 'coordinador'].includes(usuario!.rol.nombre)) {
        throw redirect(302, '/'+usuario!.rol.nombre);
    }
    const configuracion = await obtenerConfiguracion(fetch);
    return {configuracion};
}) satisfies PageServerLoad;