import type { Carrera } from "../../app";

const API = 'http://127.0.0.1:8000/api/carreras';

export const obtenerCarreras = async (fetch: typeof window.fetch) => {
  const res = await fetch(`${API}`);
  const carreras = await res.json();
  return carreras.data.carreras as Carrera[];
};

export const obtenerCarrera = async (fetch: typeof window.fetch, id: number) => {
  const res = await fetch(`${API}/${id}`);
  const carrera = await res.json();
  return carrera.data.carrera as Carrera;
};

export const crearCarrera = async (fetch: typeof window.fetch, carrera: Carrera) => {
  const res = await fetch(`${API}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(carrera)
  });
  const carreraCreada = await res.json();
  return carreraCreada.data.carrera as Carrera;
};

export const actualizarCarrera = async (fetch: typeof window.fetch, id: number, carrera: Carrera) => {
  const res = await fetch(`${API}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(carrera)
  });
  const carreraActualizada = await res.json();
  return carreraActualizada.data.carrera as Carrera;
};

export const eliminarCarrera = async (fetch: typeof window.fetch, id: number) => {
  const res = await fetch(`${API}/${id}`, {
    method: 'DELETE'
  });
  const carreraEliminada = await res.json();
  return carreraEliminada.data.carrera as Carrera;
};