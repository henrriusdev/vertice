// src/lib/servicios/autenticacion.ts
import type { Usuario } from '../../app.d';
import { apiCall, apiJson } from '$lib/utilidades/api';

const API = 'http://127.0.0.1:8000/api/usuario/';

export async function login(
	fetch: typeof window.fetch,
	correo: string,
	password: string
): Promise<{ usuario: Usuario; token: string }> {
	const data = await apiJson(fetch, `${API}login`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ correo, password })
	});

	const usuario = data.data.usuario as Usuario;

	// Extra: asegurar que rol sea string
	usuario.rol = typeof usuario.rol === 'object' ? usuario.rol : usuario.rol;

	return {
		usuario,
		token: data.data.access_token
	};
}

export async function refresh(fetch: typeof window.fetch, token: string): Promise<Usuario> {
	const response = await apiCall(fetch, `${API}refresh`, {
		method: 'GET',
		headers: {
			Authorization: token
		}
	});

	if (!response.ok) throw new Error('Token inválido');

	const json = await response.json();
	return json.data as Usuario;
}

export async function logout(fetch: typeof window.fetch, token: string): Promise<boolean> {
	const response = await apiCall(fetch, `${API}logout`, {
		method: 'POST',
		headers: {
			Authorization: token,
			'Content-Type': 'application/json'
		}
	});

	if (!response.ok) {
		const err = await response.json();
		throw new Error(err?.data?.message || 'Error al cerrar sesión');
	}

	return true;
}

export async function crearUsuario(
	fetch: typeof window.fetch,
	usuario: Partial<Usuario>
) {
	const res = await fetch(`${API}register`, {
		method: 'POST',
		body: JSON.stringify(usuario),
		headers: {
			'Content-Type': 'application/json'
		}
	});
	if (!res.ok) {
		const err = await res.json();
		throw new Error(err?.message ?? 'Error al crear usuario');
	}

	return await res.json();
}

export async function actualizarUsuario(
	fetch: typeof window.fetch,
	id: number,
	usuario: Partial<Usuario>
) {
	const res = await fetch(`${API}update/${id}`, {
		method: 'PUT',
		body: JSON.stringify(usuario),
		headers: {
			'Content-Type': 'application/json'
		}
	});
	if (!res.ok) {
		const err = await res.json();
		throw new Error(err?.message ?? 'Error al crear usuario');
	}

	return await res.json();
}

export async function eliminarUsuario(fetch: typeof window.fetch, cedula: string) {
	const res = await fetch(`${API}delete/${cedula}`, {
		method: 'DELETE'
	});
	if (!res.ok) {
		const err = await res.json();
		throw new Error(err?.message ?? 'Error al crear usuario');
	}

	return await res.json();
}

export async function obtenerUsuarios(fetch: typeof window.fetch) {
	const res = await fetch(`${API}`);
	if (!res.ok) {
		const err = await res.json();
		throw new Error(err?.message ?? 'Error al crear usuario');
	}

	const data = await res.json();
	return data.data as Usuario[];
}

// Toggle usuario status
export async function toggleUsuarioStatus(fetch: typeof window.fetch, cedula: string): Promise<Usuario> {
	const response = await apiCall(fetch, `${API}toggle-status/${cedula}`, {
		method: 'GET',
		credentials: 'include'
	});

	if (!response.ok) throw new Error('Error al cambiar el estado del usuario');
	const json = await response.json();
	return json.data as Usuario;
}

export async function obtenerUsuario(fetch: typeof window.fetch, cedula: string) {
	const res = await fetch(`${API}${cedula}`);
	if (!res.ok) {
		const err = await res.json();
		throw new Error(err?.message ?? 'Error al crear usuario');
	}

	const data = await res.json();
	return data.data as Usuario;
}

export async function cambiarPassword(fetch: typeof window.fetch, currentPassword: string, newPassword: string) {
	const result = await apiJson(fetch, `${API}change-password`, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			current_password: currentPassword,
			new_password: newPassword
		})
	});

	return result.data;
}

export async function forzarCambioPassword(fetch: typeof window.fetch, newPassword: string) {
	const response = await fetch(`${API}first-reset-password`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			password: newPassword
		})
	});

	const result = await response.json();

	if (!result.ok) {
		throw new Error(result.data.message);
	}

	return result.data;
}

export async function recuperarContrasena(
	fetch: typeof window.fetch,
	correo: string,
	password: string
) {
	const res = await fetch(`${API}force-password`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ correo, password })
	});

	if (!res.ok) {
		const err = await res.json();
		throw new Error(err?.data?.message ?? 'Error al cambiar contraseña');
	}

	return await res.json();
}
