import type { Materia, Peticion } from '../../app';
import type { Peticion as PeticionGet } from '$lib/types';

const API = 'http://127.0.0.1:8000/api/peticiones/';

export const crearPeticion = async (fetch: typeof window.fetch, payload: Omit<Peticion, 'id'>) => {
	const res = await fetch(`${API}add`, {
		method: 'POST',
		body: JSON.stringify(payload),
		headers: {
			'Content-Type': 'application/json'
		}
	});
	return await res.json();
};

export const obtenerPeticiones = async (fetch: typeof window.fetch) => {
  const res = await fetch(`${API}`)
  const response = await res.json();
  return response.data as PeticionGet[]
}

export const actualizarPeticion = async (
	fetch: typeof window.fetch,
	id: number,
	payload: any
) => {
	const res = await fetch(`${API}update/${id}`, {
		method: 'PATCH',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload)
	});
	const peticion = await res.json();
	return peticion.data as Materia;
};