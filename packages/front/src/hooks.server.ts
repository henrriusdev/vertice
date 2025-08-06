import { type Handle } from '@sveltejs/kit';

const rutasPublicas = ['/login',  '/api/usuario/refresh'];

export const handle: Handle = async ({ event, resolve }) => {
	const token = event.cookies.get('sesion');

	// Evitar refresh en rutas públicas (incluyendo donde haces redirect)
	if (rutasPublicas.includes(event.url.pathname)) {
		return resolve(event);
	}

	const originalFetch = event.fetch;
	event.fetch = async (input, init = {}) => {
		// Clona headers y añade Authorization si no existe
		init.headers = new Headers(init.headers);
		if (token && !init.headers.has('Authorization')) {
			init.headers.set('Authorization', token);
		}
		return originalFetch(input, init);
	};

	// ⛔ No refresques token en rutas públicas
	if (rutasPublicas.includes(event.url.pathname)) {
		return resolve(event);
	}

	if (token) {
		try {
			// Call refresh endpoint to extend session and get updated token
			const response = await event.fetch(`http://127.0.0.1:8000/api/usuario/refresh`, {
				method: 'GET',
				headers: {
					Authorization: token
				}
			});

			if (response.ok) {
				const json = await response.json();
				const usuario = json.data.usuario;
				event.locals.usuario = usuario;

				// Update cookie with new token if provided (sliding window)
				if (json.data.access_token) {
					event.cookies.set('sesion', json.data.access_token, {
						path: '/',
						httpOnly: true,
						sameSite: 'lax',
						secure: false, // true en producción
						maxAge: 60 * 60 * 24 * 7 // 7 days to match JWT expiration
					});
				}
			} else {
				event.locals.usuario = null;
			}

		} catch {
			event.locals.usuario = null;
		}
	} else {
		event.locals.usuario = null;
	}

	return resolve(event);
};