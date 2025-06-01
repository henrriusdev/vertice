import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { cambiarPassword } from '$lib/servicios/autenticacion';
import { configurarPreguntaSeguridad } from '$lib/servicios/pregunta-seguridad';

export const load = (async ({locals: { usuario } }) => {
	return {
		usuario
	}
}) satisfies PageServerLoad;

export const actions: Actions = {
	cambiarPassword: async ({ request, fetch }) => {
		const data = await request.formData();
		const currentPassword = data.get('currentPassword') as string;
		const newPassword = data.get('newPassword') as string;
		const confirmPassword = data.get('confirmPassword') as string;

		if (!currentPassword || !newPassword || !confirmPassword) {
			return fail(400, {
				type: 'error',
				message: 'Todos los campos son requeridos'
			});
		}

		if (newPassword !== confirmPassword) {
			return fail(400, {
				type: 'error',
				message: 'Las contraseñas no coinciden'
			});
		}

		try {
			await cambiarPassword(fetch, currentPassword, newPassword);
			return {
				type: 'success',
				message: 'Contraseña actualizada correctamente'
			};
		} catch (e) {
			console.error(e);
			return fail(400, {
				type: 'error',
				message: e instanceof Error ? e.message : 'Error al actualizar la contraseña'
			});
		}
	},

	configurarPregunta: async ({ request, fetch }) => {
		const data = await request.formData();
		const pregunta = data.get('pregunta') as string;
		const respuesta = data.get('respuesta') as string;
		const password = data.get('password') as string;

		if (!pregunta || !respuesta || !password) {
			return fail(400, {
				type: 'error',
				message: 'Todos los campos son requeridos'
			});
		}

		try {
			// Primero verificamos la contraseña actual
			await cambiarPassword(fetch, password, password);
			
			// Si la contraseña es correcta, configuramos la pregunta
			await configurarPreguntaSeguridad(fetch, pregunta, respuesta);

			return {
				type: 'success',
				message: 'Pregunta de seguridad configurada correctamente'
			};
		} catch (e) {
			console.error(e);
			return fail(400, {
				type: 'error',
				message: e instanceof Error ? e.message : 'Error al configurar la pregunta de seguridad'
			});
		}
	}
};
