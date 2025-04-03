import type { Carrera } from "../../app";

const API = 'http://127.0.0.1:8000/api/carreras';

export const obtenerCarreras = async (fetch: typeof window.fetch) => {
  const res = await fetch(`${API}`);
  const carreras = await res.json();
  return carreras.data as Carrera[];
};

export const obtenerCarrera = async (fetch: typeof window.fetch, id: number) => {
  const res = await fetch(`${API}/${id}`);
  const carrera = await res.json();
  return carrera.data.carrera as Carrera;
};

export const crearCarrera = async (fetch: typeof window.fetch, carrera: Carrera) => {
  const res = await fetch(`${API}/add`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(carrera)
  });
  const carreraCreada = await res.json();
  console.log('carreraCreada', carreraCreada);
  return carreraCreada.data.carrera as Carrera;
};

export const actualizarCarrera = async (fetch: typeof window.fetch, id: number, carrera: Carrera) => {
  const res = await fetch(`${API}/update/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({nombre: carrera.nombre})
  });
  const carreraActualizada = await res.json();
  return carreraActualizada;
};

export const eliminarCarrera = async (fetch: typeof window.fetch, id: number) => {
  const res = await fetch(`${API}/delete/${id}`, {
    method: 'DELETE'
  });
  const carreraEliminada = await res.json();
  return carreraEliminada;
};