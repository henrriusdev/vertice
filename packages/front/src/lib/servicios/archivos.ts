const API = 'http://127.0.0.1:8000/api/archivos';

export const subirPlanificacion = async (
	fetch: typeof window.fetch,
	formData: FormData
) => {
	const res = await fetch(`${API}/planificacion`, {
		method: 'POST',
		body: formData,
	});

	if (!res.ok) throw new Error('Error al subir la planificación');
	return await res.json();
};

export const obtenerReporteNotas = async (
	fetch: typeof window.fetch,
	id_materia: string
) => {
	const res = await fetch(`${API}/notas/${id_materia}/reporte`);
	if (!res.ok) throw new Error('Error al obtener el reporte de notas');
	const arrayBuffer = await res.arrayBuffer();
	const base64 = Buffer.from(arrayBuffer).toString('base64');

	return {
		base64
	};
}

export const obtenerPlanificacion = async (
	fetch: typeof window.fetch,
	id_materia: string
) => {
	const res = await fetch(`${API}/download/${id_materia}`);
	if (!res.ok) throw new Error('Error al obtener la planificación');

	const contentType = res.headers.get("Content-Type") || "application/octet-stream";
	const arrayBuffer = await res.arrayBuffer();
	const base64 = Buffer.from(arrayBuffer).toString('base64');

	return {
		base64,
		type: contentType
	};
}

export const obtenerConstancia = async (
	fetch: typeof window.fetch,
	cedula: string
) => {
	const res = await fetch(`${API}/estudiantes/${cedula}/constancia`);
	if (!res.ok) throw new Error('Error al obtener la planificación');

	const arrayBuffer = await res.arrayBuffer();
	const base64 = Buffer.from(arrayBuffer).toString('base64');

	return {
		base64,
	};
}