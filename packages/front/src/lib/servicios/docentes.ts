// import type { DocenteReq } from "$lib/types";
import type { DocenteReq } from "$lib/types";
import type { Docente } from "../../app";

const API = 'http://127.0.0.1:8000/api/docentes';

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
  const res = await fetch(`${API}/add`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(docente)
  });
  const docenteCreado = await res.json();
  return docenteCreado.data as Docente;
};

export const actualizarDocente = async (fetch: typeof window.fetch, id: number, docente: DocenteReq) => {
  const res = await fetch(`${API}/update/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(docente)
  });
  const docenteActualizado = await res.json();
  return docenteActualizado.data as Docente;
};

export const eliminarDocente = async (fetch: typeof window.fetch, cedula: string) => {
  const res = await fetch(`${API}/delete/${cedula}`, {
    method: 'DELETE'
  });
  const docenteEliminado = await res.json();
  return docenteEliminado.data as Docente;
};