// import type { CoordinadorReq } from "$lib/types";
import type { CoordinadorReq } from "$lib/types";
import type { Coordinador } from "../../app";

const API = 'http://127.0.0.1:8000/api/coordinadores';

export const obtenerCoordinadores = async (fetch: typeof window.fetch) => {
	const res = await fetch(`${API}`);
	const coordinadors = await res.json();
	return coordinadors.data as Coordinador[];
};

export const obtenerCoordinador = async (fetch: typeof window.fetch, id: number) => {
  const res = await fetch(`${API}/${id}`);
  const coordinador = await res.json();
  return coordinador.data as Coordinador;
};

export const crearCoordinador = async (fetch: typeof window.fetch, coordinador: CoordinadorReq) => {
  const res = await fetch(`${API}/add`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(coordinador)
  });
  const coordinadorCreado = await res.json();
  return coordinadorCreado.data as Coordinador;
};

export const actualizarCoordinador = async (fetch: typeof window.fetch, id: number, coordinador: CoordinadorReq) => {
  const res = await fetch(`${API}/update/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(coordinador)
  });
  const coordinadorActualizado = await res.json();
  return coordinadorActualizado.data as Coordinador;
};

export const eliminarCoordinador = async (fetch: typeof window.fetch, cedula: string) => {
  const res = await fetch(`${API}/delete/${cedula}`, {
    method: 'DELETE'
  });
  const coordinadorEliminado = await res.json();
  return coordinadorEliminado.data as Coordinador;
};