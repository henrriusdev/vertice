import type { Estudiante } from "../../app";

const API = 'http://127.0.0.1:8000/api/estudiantes';

export const obtenerEstudiantes = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}`);
	const estudiantes = await res.json();
	return estudiantes.data.estudiantes as Estudiante[];
};

export const obtenerEstudiante = async (fetch: typeof window.fetch, id: number) => {
  const res = await fetch(`${API}/${id}`);
  const estudiante = await res.json();
  return estudiante.data.estudiante as Estudiante;
};

export const crearEstudiante = async (fetch: typeof window.fetch, estudiante: Estudiante) => {
  const res = await fetch(`${API}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(estudiante)
  });
  const estudianteCreado = await res.json();
  return estudianteCreado.data.estudiante as Estudiante;
};

export const actualizarEstudiante = async (fetch: typeof window.fetch, id: number, estudiante: Estudiante) => {
  const res = await fetch(`${API}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(estudiante)
  });
  const estudianteActualizado = await res.json();
  return estudianteActualizado.data.estudiante as Estudiante;
};

export const eliminarEstudiante = async (fetch: typeof window.fetch, id: number) => {
  const res = await fetch(`${API}/${id}`, {
    method: 'DELETE'
  });
  const estudianteEliminado = await res.json();
  return estudianteEliminado.data.estudiante as Estudiante;
};