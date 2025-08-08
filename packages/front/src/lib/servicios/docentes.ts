import type { DocenteReq } from '$lib/types';
import { apiCall } from '$lib/utilidades';
import type { Docente, MateriaDocente } from '../../app';

const API = 'http://127.0.0.1:8000/api/docentes/';

export const obtenerDocentes = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}`);
	const docentes = await res.json();
	return docentes.data as Docente[];
};

export const obtenerDocente = async (fetch: typeof window.fetch, id: number) => {
	const res = await fetch(`${API}/${id}`);
	const docente = await res.json();
	return docente.data as Docente;
};

export const crearDocente = async (fetch: typeof window.fetch, docente: DocenteReq) => {
	const res = await fetch(`${API}add`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(docente)
	});
	const docenteCreado = await res.json();
	return docenteCreado.data as Docente;
};

export const actualizarDocente = async (
	fetch: typeof window.fetch,
	id: number,
	docente: DocenteReq
) => {
	const res = await fetch(`${API}update/${id}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(docente)
	});
	const docenteActualizado = await res.json();
	return docenteActualizado.data as Docente;
};

export const eliminarDocente = async (fetch: typeof window.fetch, cedula: string) => {
	const res = await fetch(`${API}delete/${cedula}`, {
		method: 'DELETE'
	});
	const docenteEliminado = await res.json();
	return docenteEliminado.data as Docente;
};

export const obtenerMateriasAsignadas = async (fetch: typeof window.fetch) => {
	const res = await apiCall(fetch, `${API}materias`, {
		method: 'GET',
		credentials: 'include'
	});
	const response = await res.json();
	return response.data as MateriaDocente[];
};

export async function toggleDocenteStatus(fetch: typeof window.fetch, cedula: string): Promise<Docente> {
    const response = await apiCall(fetch, `${API}toggle-status/${cedula}`, {
        method: 'GET',
        credentials: 'include'
    });

    if (!response.ok) throw new Error('Error al cambiar el estado del docente');
    const json = await response.json();
    return json.data as Docente;
}