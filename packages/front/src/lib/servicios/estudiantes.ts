import type { EstudianteReq } from '$lib/types';
import type { Estudiante, MateriaHistorico, MateriaInscrita } from '../../app';

const API = 'http://127.0.0.1:8000/api/estudiantes';

export const obtenerEstudiantes = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}`);
	const estudiantes = await res.json();
	return estudiantes.data as Estudiante[];
};

export const obtenerEstudiante = async (fetch: typeof window.fetch, id: number) => {
	const res = await fetch(`${API}/${id}`);
	const estudiante = await res.json();
	return estudiante.data as Estudiante;
};

export const crearEstudiante = async (fetch: typeof window.fetch, estudiante: EstudianteReq) => {
	const res = await fetch(`${API}/add`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(estudiante)
	});
	const estudianteCreado = await res.json();
	return estudianteCreado.data as Estudiante;
};

export const actualizarEstudiante = async (
	fetch: typeof window.fetch,
	id: number,
	estudiante: EstudianteReq
) => {
	const res = await fetch(`${API}/update/${id}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(estudiante)
	});
	const estudianteActualizado = await res.json();
	return estudianteActualizado.data as Estudiante;
};

export const eliminarEstudiante = async (fetch: typeof window.fetch, cedula: string) => {
	const res = await fetch(`${API}/delete/${cedula}`, {
		method: 'DELETE'
	});
	const estudianteEliminado = await res.json();
	return estudianteEliminado.data as Estudiante;
};

export const obtenerMateriasInscritas = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}/horario`);
	const materias = await res.json();
	return materias.data.materias as MateriaInscrita[];
};

export const obtenerHistoricoMaterias = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}/historico`);
	const materias = await res.json();
	return materias.data.notas as MateriaHistorico[];
};

export const inscribirMaterias = async (
	fetch: typeof window.fetch,
	payload: { materias: string[] }
) => {
	const res = await fetch(`${API}/add-materia`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload)
	});

	const response = await res.json();
	return response;
};
