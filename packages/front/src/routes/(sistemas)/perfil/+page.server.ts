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
		const preguntas = [];

		// Recolectar las 3 preguntas y respuestas
		for (let i = 0; i < 3; i++) {
			const pregunta = data.get(`pregunta${i}`) as string;
			const respuesta = data.get(`respuesta${i}`) as string;

			if (!pregunta || !respuesta) {
				return {
					type: 'failure',
					message: 'Todas las preguntas y respuestas son requeridas'
				}
			}

			preguntas.push({ pregunta, respuesta });
		}

		try {
			// Configurar todas las preguntas en un solo request
			await configurarPreguntaSeguridad(fetch, preguntas);

			return {
				type: 'success',
				message: 'Preguntas de seguridad configuradas correctamente'
			};
		} catch (e) {
			console.error(e);
			return {
				type: 'failure',
				message: e instanceof Error ? e.message : 'Error al configurar las preguntas de seguridad'
			};
		}
	}
};
