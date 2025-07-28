import { login } from '$lib';
import { redirect } from '@sveltejs/kit';

export const load = async ({ locals }) => {
	if (locals.usuario) {
		throw redirect(302, `/${locals.usuario.rol.nombre.toLowerCase()}`);
	}
};

export const actions = {
	default: async ({ request, fetch, cookies }) => {
		const data = await request.formData();
		const correo = data.get('correo') as string;
		const password = data.get('password') as string;

		let destino = '/';
		try {
			const { usuario, token } = await login(fetch, correo, password);

                        cookies.set('sesion', token, {
                                path: '/',
                                httpOnly: true,
                                sameSite: 'strict',
                                secure: false, // true en producción
                                maxAge: 60 * 60 * 8 // 8h
                        });

			destino = `/${usuario.rol.nombre.toLowerCase()}`;
			return {
				type: 'success',
				message: 'Inicio de sesión exitoso',
				invalidate: destino
			};
		} catch (e: any) {
			console.error('Error en inicio de sesión:', e);
			return {
				type: 'failure',
				message: e.message
			};
		}
	}
};
