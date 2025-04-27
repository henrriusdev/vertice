import type { MateriaReq } from '$lib/types';
import type { Materia, MateriaDisponible, MateriaHistorico, MateriaInscrita } from '../../app';

const API = 'http://127.0.0.1:8000/api/materias';

export const obtenerMaterias = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}`);
	const materias = await res.json();
	return materias.data as { materias: Materia[] };
};

export const obtenerMateria = async (fetch: typeof window.fetch, id: string) => {
	const res = await fetch(`${API}/${id}`);
	const materia = await res.json();
	return materia.data as Materia;
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

export const obtenerMateriasInscritas = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}/estudiante/inscritas`);
	const materias = await res.json();
	return materias.data as MateriaInscrita[];
};

export const obtenerHistoricoMaterias = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}/estudiante/historico`);
	const materias = await res.json();
	return materias.data as MateriaHistorico[];
};

export const obtenerMateriasDisponibles = async (fetch: typeof window.fetch, cedula: string) => {
	const res = await fetch(`${API}/materias/inscribir/${cedula}`);
	const materias = await res.json();
	return materias.data as MateriaDisponible[];
};