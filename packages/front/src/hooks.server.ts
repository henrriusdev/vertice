// src/hooks.server.ts
import { refresh } from '$lib';
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
			init.headers.set('Authorization', `Bearer ${token}`);
		}
		return originalFetch(input, init);
	};

	// ⛔ No refresques token en rutas públicas
	if (rutasPublicas.includes(event.url.pathname)) {
		return resolve(event);
	}

	if (token) {
		try {
			const usuario = await refresh(event.fetch, token);
			event.locals.usuario = usuario;

		} catch {
			event.cookies.delete('sesion', { path: '/' });
			event.locals.usuario = null;
		}
	} else {
		event.locals.usuario = null;
	}

	return resolve(event);
};
