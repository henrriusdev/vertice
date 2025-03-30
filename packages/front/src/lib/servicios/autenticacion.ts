// src/lib/servicios/autenticacion.ts
import type { Usuario } from '../../app.d';

const API = 'http://127.0.0.1:8000/api/usuario';

export async function login(
	fetch: typeof window.fetch,
	correo: string,
	password: string
): Promise<{ usuario: Usuario; token: string }> {
	const res = await fetch(`${API}/login`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ correo, password })
	});

	if (!res.ok) {
		const errorData = await res.json();
		throw new Error(errorData?.data?.message || 'Error al iniciar sesión');
	}

	const data = await res.json();
	const usuario = data.data.usuario as Usuario;

	// Extra: asegurar que rol sea string
	usuario.rol = typeof usuario.rol === 'object' ? usuario.rol : usuario.rol;

	return {
		usuario,
		token: data.data.access_token
	};
}

export async function refresh(fetch: typeof window.fetch, token: string): Promise<Usuario> {
	const res = await fetch(`${API}/refresh`, {
		method: 'GET',
		headers: {
			Authorization: token
		}
	});

	if (!res.ok) throw new Error('Token inválido');

	const json = await res.json();
	const usuario = json.data as Usuario;
	usuario.rol = typeof usuario.rol === 'object' ? usuario.rol : usuario.rol;
	return usuario;
}


export async function logout(fetch: typeof window.fetch, token: string): Promise<boolean> {
	const res = await fetch(`${API}/logout`, {
		method: 'POST',
		headers: {
			Authorization: token,
			'Content-Type': 'application/json'
		}
	});

	if (!res.ok) {
		const err = await res.json();
		throw new Error(err?.data?.message || 'Error al cerrar sesión');
	}

	return true;
}