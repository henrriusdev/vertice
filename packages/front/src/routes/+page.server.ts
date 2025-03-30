// src/routes/+page.server.ts
import { login } from '$lib/servicios/autenticacion';
import { redirect, fail } from '@sveltejs/kit';

export const load = async ({ locals }) => {
	console.log('locals', locals);
	if (locals.usuario) {
		throw redirect(302, `/${locals.usuario.rol.nombre.toLowerCase()}`);
	}
};

export const actions = {
	default: async ({ request, fetch, cookies }) => {
		const data = await request.formData();
		const correo = data.get('correo') as string;
		const password = data.get('password') as string;

		try {
			const { usuario, token } = await login(fetch, correo, password);

			cookies.set('sesion', token, {
				path: '/',
				httpOnly: true,
				sameSite: 'strict',
				secure: false, // true en producción
				maxAge: 60 * 60 * 2 // 2h
			});

			const destino = `/${usuario.rol.nombre.toLowerCase()}`;
			redirect(302, destino);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
		} catch (e: any) {
			return fail(401, { mensaje: e.message });
		}
	}
};
