import type { MateriaReq } from '$lib/types';
import type { Materia, MateriaCiclo, MateriaDisponible } from '../../app';

const API = 'http://127.0.0.1:8000/api/materias/';

export const obtenerMaterias = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}`);
	const materias = await res.json();
	return materias.data as { materias: Materia[] };
};

export const obtenerMateria = async (fetch: typeof window.fetch, id: string) => {
	const res = await fetch(`${API}${id}`);
	const materia = await res.json();
	return materia.data as MateriaCiclo;
};

export const crearMateria = async (fetch: typeof window.fetch, materia: MateriaReq) => {
	const res = await fetch(`${API}add`, {
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
	const res = await fetch(`${API}update/${id}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(materia)
	});
	const materiaActualizada = await res.json();
	return materiaActualizada.data as Materia;
};

export const eliminarMateria = async (fetch: typeof window.fetch, id: string) => {
	const res = await fetch(`${API}delete/${id}`, {
		method: 'DELETE'
	});
	const materiaEliminada = await res.json();
	return materiaEliminada.data as Materia;
};

export const obtenerMateriasDisponibles = async (fetch: typeof window.fetch, cedula: string) => {
	try {
		const res = await fetch(`${API}inscribir/${cedula}`);
		
		// Manejar específicamente el caso 204 (No Content)
		if (res.status === 204) {
			console.log('El servidor respondió con 204 No Content');
			return [];
		}
		
		// Verificar el estado de la respuesta antes de intentar analizar el JSON
		if (!res.ok) {
			console.error(`Error al obtener materias disponibles: ${res.status} ${res.statusText}`);
			return [];
		}
		
		// Verificar si la respuesta está vacía
		const text = await res.text();
		if (!text || text.trim() === '') {
			console.log('La respuesta del servidor está vacía');
			return [];
		}
		
		// Intentar analizar el JSON
		const materias = JSON.parse(text);
		return materias.data as MateriaDisponible[];
	} catch (error) {
		console.error('Error al procesar materias disponibles:', error);
		return [];
	}
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
	const res = await fetch(`${API}upload`, {
		method: 'PATCH',
		body: JSON.stringify(payload),
		headers: {
			'Content-Type': 'application/json'
		}
	});
	return res;
};

export const toggleMateriaStatus = async (
	fetch: typeof window.fetch,
	id: string
) => {
	const res = await fetch(`${API}toggle-status/${id}`, {
		method: 'PUT'
	});
	return res;
};
