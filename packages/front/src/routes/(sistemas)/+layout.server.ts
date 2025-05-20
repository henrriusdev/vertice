import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
	if (!locals.usuario) {
		throw redirect(302, '/');
	}

	return {
		nombre: locals.usuario.nombre,
		rol: locals.usuario.rol.nombre,
		correo: locals.usuario.correo
	}
};
