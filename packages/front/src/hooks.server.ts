// src/hooks.server.ts
import { refresh } from '$lib/servicios/autenticacion';
import { type Handle } from '@sveltejs/kit';

const rutasPublicas = ['/login',  '/api/usuario/refresh'];

export const handle: Handle = async ({ event, resolve }) => {
	const token = event.cookies.get('sesion');

	// Evitar refresh en rutas públicas (incluyendo donde haces redirect)
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
