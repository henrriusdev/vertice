import type { MateriaReq } from '$lib/types';
import type { Materia, MateriaCiclo, MateriaDisponible } from '../../app';

const API = 'http://127.0.0.1:8000/api/materias';

export const obtenerMaterias = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}`);
	const materias = await res.json();
	return materias.data as { materias: Materia[] };
};

export const obtenerMateria = async (fetch: typeof window.fetch, id: string) => {
	const res = await fetch(`${API}/${id}`);
	const materia = await res.json();
	return materia.data as MateriaCiclo;
};

export const crearMateria = async (fetch: typeof window.fetch, materia: MateriaReq) => {
	const res = await fetch(`${API}/add`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(materia)
	});
	const materiaCreada = await res.json();
	return materiaCreada.data as Materia;
};

export const actualizarMateria = async (
	fetch: typeof window.fetch,
	id: string,
	materia: MateriaReq
) => {
	const res = await fetch(`${API}/update/${id}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(materia)
	});
	const materiaActualizada = await res.json();
	return materiaActualizada.data as Materia;
};

export const eliminarMateria = async (fetch: typeof window.fetch, id: string) => {
	const res = await fetch(`${API}/delete/${id}`, {
		method: 'DELETE'
	});
	const materiaEliminada = await res.json();
	return materiaEliminada.data as Materia;
};

export const obtenerMateriasDisponibles = async (fetch: typeof window.fetch, cedula: string) => {
	const res = await fetch(`${API}/inscribir/${cedula}`);
	const materias = await res.json();
	if (res.status === 401) return [];
	return materias.data as MateriaDisponible[];
};

export const actualizarNota = async (
	fetch: typeof window.fetch,
	payload: {
		cedula_estudiante: string;
		nombre_campo: string;
		valor: string | number;
		materia: string;
	}
) => {
	const res = await fetch(`${API}/upload`, {
		method: 'PATCH',
		body: JSON.stringify(payload),
		headers: {
			'Content-Type': 'application/json'
		}
	});
	return res;
};