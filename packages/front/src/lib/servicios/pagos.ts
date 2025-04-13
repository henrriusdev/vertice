import type { Pago } from "../../app";

const API = 'http://127.0.0.1:8000/api/pagos';

export const obtenerPagosPorCedula = async (fetch: typeof window.fetch, cedula: string) => {
	const res = await fetch(`${API}/estudiante/${cedula}`);
	if (!res.ok) throw new Error('Error al obtener pagos');
	const data = await res.json();
	return data.data as Pago[];
};

export const crearPago = async (fetch: typeof window.fetch, pago: Pago) => {
	const res = await fetch(`${API}/add`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(pago)
	});
	if (!res.ok) throw new Error('Error al crear el pago');
	const data = await res.json();
	return data.data as Pago;
};
