import { actualizarConfiguracion, crearConfiguracion, obtenerConfiguracion } from '$lib';
import { fail, redirect } from '@sveltejs/kit';
import type { Configuracion } from '../../../app';
import type { Actions, PageServerLoad } from './$types';
import { format } from 'date-fns';

export const load = (async ({ fetch, locals: { usuario } }) => {
	if (!['superusuario', 'coordinador'].includes(usuario!.rol.nombre)) {
		throw redirect(302, '/' + usuario!.rol.nombre);
	}
	const configuracion = await obtenerConfiguracion(fetch);
	console.log(configuracion);
	return { configuracion };
}) satisfies PageServerLoad;

export const actions: Actions = {
	default: async ({ request, fetch }) => {
		const data = await request.formData();

		const ciclo = `${data.get('cicloYear')}-${data.get('cicloPeriodo')}`;
		const num_porcentaje = Number(data.get('num_porcentaje'));
		const num_cuotas = Number(data.get('num_cuotas'));

		const porcentajes = Array.from({ length: num_porcentaje }, (_, i) =>
			Number(data.get(`porcentajes[${i}]`))
		);

		const cuotas = data.getAll('cuotas').map((cuota) => cuota.toString());

		const horario_inicio = new Date(data.get('horario_inicio')!.toString());
		const horario_fin = new Date(data.get('horario_fin')!.toString());
		
		const payload: Configuracion = {
			ciclo,
			num_porcentaje,
			num_cuotas,
			porcentajes,
			cuotas: cuotas,
			horario_inicio: format(horario_inicio, 'dd/MM/yyyy'),
			horario_fin: format(horario_fin, 'dd/MM/yyyy')
		};
		
		console.log(payload);

		// Verificamos si ya existe config para decidir acción
		const configActual = await obtenerConfiguracion(fetch);
		try {
			if (configActual) {
				await actualizarConfiguracion(fetch, payload);
			} else {
				await crearConfiguracion(fetch, payload);
			}
		} catch (e) {
			console.error(e);
			return fail(500, { message: 'No se pudo guardar la configuración.' });
		}
	}
};