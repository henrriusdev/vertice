import { inscribirMaterias, obtenerConfiguracion, obtenerMateriasInscritas } from '$lib';
import { obtenerMateriasDisponibles } from '$lib/servicios/materias';
import { isAfter } from 'date-fns';
import type { Actions, PageServerLoad } from './$types';
import type { MateriaDisponible, MateriaInscrita } from '../../../../app';

export const load: PageServerLoad = async ({ fetch, locals: { usuario } }) => {
	const config = await obtenerConfiguracion(fetch);
	const { horario_inicio: inicio, horario_fin: fin }: { horario_inicio: Date; horario_fin: Date } =
		config;
	const materiasInscritas = await obtenerMateriasInscritas(fetch);
	console.log(fin)
	console.log(isAfter(inicio, new Date()), isAfter(new Date(), fin), materiasInscritas.length > 0);
	if (isAfter(inicio, new Date()) || isAfter(new Date(), fin)) {
		return {
			materiasDisponibles: [] as MateriaDisponible[],
			materiasInscritas,
			inscripcionAbierta: false
		};
	}

	if (materiasInscritas.length > 0) {
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
		console.log(form.getAll('materias'));
		for (const materia of form.getAll('materias')) {
			if (!materias.includes(materia)) {
				materias.push(materia.toString());
			}
		}

		try {
			const payload = {
				materias: materias
			};

			const res = await inscribirMaterias(fetch, payload);
			return { success: true };
		} catch (e) {
			console.log(e);
		}
	}
};
