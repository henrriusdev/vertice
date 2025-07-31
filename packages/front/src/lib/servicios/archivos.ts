import type { ExportacionParams } from '$lib';

const API = 'http://127.0.0.1:8000/api/archivos';

export const subirPlanificacion = async (fetch: typeof window.fetch, formData: FormData) => {
	const res = await fetch(`${API}/planificacion`, {
		method: 'POST',
		body: formData
	});

	if (!res.ok) throw new Error('Error al subir la planificación');
	return await res.json();
};

export const obtenerReporteNotas = async (fetch: typeof window.fetch, id_materia: string) => {
	const res = await fetch(`${API}/notas/${id_materia}/reporte`);
	if (!res.ok) throw new Error('Error al obtener el reporte de notas');
	const contentType = res.headers.get('Content-Type') || 'application/octet-stream';
	const arrayBuffer = await res.arrayBuffer();
	const base64 = Buffer.from(arrayBuffer).toString('base64');

	return {
		base64,
		type: contentType
	};
};

export const obtenerPlanificacion = async (fetch: typeof window.fetch, id_materia: string) => {
	const res = await fetch(`${API}/download/${id_materia}`);
	if (!res.ok) {
		if (res.status === 404) {
			throw new Error('Planificación aún no subida');
		}

		throw new Error('Error al obtener la planificación');
	}

	const contentType = res.headers.get('Content-Type') || 'application/octet-stream';
	const arrayBuffer = await res.arrayBuffer();
	const base64 = Buffer.from(arrayBuffer).toString('base64');

	return {
		base64,
		type: contentType
	};
};

export const obtenerConstancia = async (fetch: typeof window.fetch, cedula: string) => {
	const res = await fetch(`${API}/estudiantes/${cedula}/constancia`);
	if (!res.ok) throw new Error('Error al obtener la planificación');

	const contentType = res.headers.get('Content-Type') || 'application/octet-stream';
	const arrayBuffer = await res.arrayBuffer();
	const base64 = Buffer.from(arrayBuffer).toString('base64');

	return {
		base64,
		type: contentType
	};
};

// Función para exportar los datos en diferentes formatos
export const exportarTrazabilidad = async (
	params: ExportacionParams,
	fetch: typeof globalThis.fetch
) => {
	try {
		// Preparar los parámetros para la llamada al backend
		const body = JSON.stringify({
			formato: params.formato,
			busqueda: params.busqueda || '',
			fechaDesde: params.fechaDesde || '',
			fechaHasta: params.fechaHasta || '',
			rol: params.rol || ''
		});

		const res = await fetch(`${API}/trazabilidad/exportar`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body
		});
		if (!res.ok) throw new Error('Error al obtener la planificación');

		const contentType = res.headers.get('Content-Type') || 'application/octet-stream';
		const arrayBuffer = await res.arrayBuffer();
		const base64 = Buffer.from(arrayBuffer).toString('base64');

		return {
			base64,
			type: contentType
		};
	} catch (error) {
		console.error('Error al exportar archivo:', error);
		throw error;
	}
};

export const descargarExcel = async (fetch: typeof globalThis.fetch) => {
	const res = await fetch(`${API}/excel`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
		}
	});

	if (!res.ok) throw new Error('Error al descargar el archivo Excel');

	const contentType = res.headers.get('Content-Type') || 'application/octet-stream';
	const arrayBuffer = await res.arrayBuffer();
	const base64 = Buffer.from(arrayBuffer).toString('base64');

	return {
		base64,
		type: contentType
	};
}

export const subirExcelUsuarios = async (fetch: typeof window.fetch, formData: FormData) => {
	const res = await fetch(`${API}/usuarios/importar`, {
		method: 'POST',
		body: formData
	});
	if (!res.ok) throw new Error('Error al subir el archivo Excel');
	return await res.json();
};
