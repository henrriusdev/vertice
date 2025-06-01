import { fail } from '@sveltejs/kit';
import type { Actions } from './$types';
import { obtenerPreguntaSeguridad, verificarPreguntaSeguridad } from '$lib/servicios/pregunta-seguridad';
import { recuperarContrasena } from '$lib/servicios/autenticacion';

// Almacenamiento en memoria de intentos por correo
const intentosPorCorreo = new Map<string, { count: number; lastAttempt: Date }>();

function checkIntentos(correo: string): boolean {
	const now = new Date();
	const intentos = intentosPorCorreo.get(correo);

	if (!intentos) {
		intentosPorCorreo.set(correo, { count: 0, lastAttempt: now });
		return true;
	}

	// Si ha pasado más de 24 horas, reiniciar contador
	if (now.getTime() - intentos.lastAttempt.getTime() > 24 * 60 * 60 * 1000) {
		return true;
	}

	// Si hay más de 3 intentos en las últimas 24 horas, bloquear
	if (intentos.count >= 3) {
		return false;
	}

	return true;
}

// Función para incrementar intentos
function incrementarIntentos(correo: string): void {
	const intentos = intentosPorCorreo.get(correo);
	if (intentos) {
		intentosPorCorreo.set(correo, {
			count: intentos.count + 1,
			lastAttempt: new Date()
		});
	}
}

export const actions = {
	default: async ({ request, fetch }) => {
		const data = await request.formData();
		const correo = data.get('correo')?.toString();
		const respuesta = data.get('respuesta')?.toString();
		const newPassword = data.get('newPassword')?.toString();

		// Si viene correo, obtener pregunta
		if (correo && !respuesta && !newPassword) {
			try {
				const result = await obtenerPreguntaSeguridad(fetch, correo);
				return {
					type: 'success',
					message: 'Pregunta de seguridad obtenida',
					pregunta: result.data.pregunta
				};
			} catch (e) {
				return {
					type: 'failure',
					message: e instanceof Error ? e.message : 'Error al obtener la pregunta de seguridad'
				};
			}
		}

		// Si viene respuesta, verificarla
		if (correo && respuesta && !newPassword) {
			// Verificar intentos primero
			if (!checkIntentos(correo)) {
				return fail(400, {
					error: 'Has excedido el número máximo de intentos. Intenta de nuevo mañana.'
				});
			}

			try {
				await verificarPreguntaSeguridad(fetch, correo, respuesta);
				return {
					type: 'success',
					message: 'Respuesta verificada correctamente'
				};
			} catch (e) {
				incrementarIntentos(correo);
				return {
					type: 'failure',
					message: e instanceof Error ? e.message : 'Error al verificar la respuesta'
				};
			}
		}

		// Si viene nueva contraseña, actualizarla
		if (correo && newPassword) {
			try {
				await recuperarContrasena(fetch, correo, newPassword);
				return {
					type: 'success',
					message: 'Contraseña actualizada correctamente',
					location: '/'
				};
			} catch (e) {
				return {
					type: 'failure',
					message: e instanceof Error ? e.message : 'Error al cambiar la contraseña'
				};
			}
		}

		return {};
	}
} satisfies Actions;
