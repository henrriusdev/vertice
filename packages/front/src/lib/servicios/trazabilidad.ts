import type { Trazabilidad } from '../../app';
import type { FiltroTrazabilidad } from '$lib';

const API = 'http://127.0.0.1:8000/api/trazabilidad';

export async function filtrarTrazabilidad(
	filtros: FiltroTrazabilidad,
	fetch: typeof globalThis.fetch
): Promise<Trazabilidad[]> {
	try {
		const res = await fetch(`${API}`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(filtros)
		});
		const trazabilidad = await res.json();
		return trazabilidad.data as Trazabilidad[];
	} catch (error) {
		console.error('Error al filtrar los datos de trazabilidad:', error);
		throw error;
	}
}
