import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { cambiarPassword } from '$lib/servicios/autenticacion';

export const actions: Actions = {
	default: async ({ request, locals, fetch, url }) => {
		if (!locals.usuario) {
			throw redirect(302, '/');
		}

		try {
			const data = await request.formData();
			const newPassword = data.get('new_password') as string;

			await cambiarPassword(fetch, newPassword);

			return {
				invalidate: true,
				type: 'success',
				message: 'Contraseña actualizada correctamente',
                location: url.pathname
			};
		} catch (e) {
			console.error(e);
			return {
				type: 'failure',
				message: e instanceof Error ? e.message : 'Error al actualizar la contraseña'
			};
		}
	}
};
