// import type { DocenteReq } from "$lib/types";
import type { Docente } from "../../app";

const API = 'http://127.0.0.1:8000/api/docentes';

export const obtenerDocentes = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}`);
	const estudiantes = await res.json();
	return estudiantes.data as Docente[];
};

export const obtenerDocente = async (fetch: typeof window.fetch, id: number) => {
  const res = await fetch(`${API}/${id}`);
  const estudiante = await res.json();
  return estudiante.data as Docente;
};

export const crearDocente = async (fetch: typeof window.fetch, docente: unknown) => {
  const res = await fetch(`${API}/add`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(docente)
  });
  const estudianteCreado = await res.json();
  return estudianteCreado.data as Docente;
};

export const actualizarDocente = async (fetch: typeof window.fetch, id: number, estudiante: unknown) => {
  const res = await fetch(`${API}/update/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(estudiante)
  });
  const estudianteActualizado = await res.json();
  return estudianteActualizado.data as Docente;
};

export const eliminarDocente = async (fetch: typeof window.fetch, cedula: string) => {
  const res = await fetch(`${API}/delete/${cedula}`, {
    method: 'DELETE'
  });
  const estudianteEliminado = await res.json();
  return estudianteEliminado.data as Docente;
};