import { inscribirMaterias, obtenerConfiguracion, obtenerMateriasInscritas } from '$lib';
import { obtenerMateriasDisponibles } from '$lib/servicios/materias';
import { isAfter } from 'date-fns';
import type { Actions, PageServerLoad } from './$types';
import type { MateriaDisponible, MateriaInscrita } from '../../../../app';
import { addToast } from '$lib';

export const load: PageServerLoad = async ({ fetch, locals: { usuario } }) => {
	const config = await obtenerConfiguracion(fetch);
	const { horario_inicio: inicio, horario_fin: fin }: { horario_inicio: Date; horario_fin: Date } =
		config;
	const materiasInscritas = await obtenerMateriasInscritas(fetch);
	if (isAfter(inicio, new Date()) || isAfter(new Date(), fin)) {
		return {
			materiasDisponibles: [] as MateriaDisponible[],
			materiasInscritas,
			inscripcionAbierta: false
		};
	}

	if (materiasInscritas.length > 0) {
		addToast({
			type: 'info',
			message: 'Ya tienes tu horario inscrito'
		});
		return {
			materiasDisponibles: [] as MateriaDisponible[],
			inscripcionAbierta: false,
			materiasInscritas
		};
	}
	const materiasDisponibles = await obtenerMateriasDisponibles(fetch, usuario?.cedula ?? '');

	return {
		materiasDisponibles,
		materiasInscritas,
		inscripcionAbierta: true
	};
};

export const actions: Actions = {
	default: async ({ request, fetch }) => {
		const form = await request.formData();
		const materias: string[] = [];
		for (const materia of form.getAll('materias')) {
			if (!materias.includes(materia)) {
				materias.push(materia.toString());
			}
		}

		try {
			const payload = {
				materias: materias
			};

			await inscribirMaterias(fetch, payload);
			return {
				type: 'success',
				message: 'Materias inscritas exitosamente',
				invalidate: true
			};
		} catch (e: any) {
			console.error('Error al inscribir materias:', e);
			return {
				type: 'failure',
				message: e.message
			};
		}
	}
};
