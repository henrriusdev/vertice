import { crearPago, generarReporte, obtenerEstudiantes } from '$lib';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	const estudiantes = await obtenerEstudiantes(fetch);
	return { estudiantes: estudiantes.map((est) => est.cedula) };
};

export const actions: Actions = {
	crear: async ({ request, fetch }) => {
		const formData = await request.formData();

		const student = formData.get('student') as string;
		const concept = formData.get('payment-concept') as string;
		const method = formData.get('payment-method') as 'cash' | 'transfer' | 'point';
		const amount = formData.get('amount') as string;
		const fecha_pago = formData.get('fecha_pago') as string;
		const referencia = formData.get('referencia_transferencia') as string | null;
		const billetesRaw = formData.getAll('billetes');

		if (!student || !concept || !method || !amount || !fecha_pago) {
			return {
				type: 'failure',
				message: 'Por favor completa todos los campos'
			};
		}

		let billetes = undefined;
		if (method === 'cash') {
			try {
				billetes = billetesRaw.map((b) => JSON.parse(b as string));
			} catch {
				return {
					type: 'failure',
					message: 'Error al procesar los billetes'
				};
			}
		}

		const payload = {
			student,
			concept,
			method,
			amount: parseFloat(amount),
			date: fecha_pago,
			reference: method === 'transfer' ? referencia : undefined,
			billetes
		};

		try {
			await crearPago(fetch, payload);
			return {
				type: 'success',
				message: 'Pago registrado exitosamente',
				invalidate: true
			};
		} catch (e: any) {
			console.error('Error al registrar el pago:', e);
			return {
				type: 'failure',
				message: e.message
			};
		}
	},
	generarReporte: async ({ fetch, request }) => {
		const formData = await request.formData();

		const tipo = formData.get('tipo');
		const filtro = formData.get('filtro');
		const fecha = formData.get('fecha');
		const fi = formData.get('fi');
		const ff = formData.get('ff');

		const params = new URLSearchParams();
		if (tipo) params.set('tipo', tipo.toString());
		if (filtro && filtro !== 'todos') params.set('f', filtro.toString());
		if (tipo === 'dia' && fecha) params.set('d', fecha.toString());
		if ((tipo === 'fechas' || tipo === 'monto') && fi && ff) {
			params.set('fi', fi.toString());
			params.set('ff', ff.toString());
		}

		try {
			const { base64 } = await generarReporte(fetch, params.toString());
			return {
				base64,
				type: 'application/pdf',
				message: 'Reporte generado exitosamente',
				invalidate: true
			};
		} catch (e: any) {
			console.error('Error al generar reporte:', e);
			return {
				type: 'failure',
				message: e.message
			};
		}
	}
};