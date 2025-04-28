import { obtenerConfiguracion } from '$lib';
import { obtenerMateriasDisponibles } from '$lib/servicios/materias';
import { isAfter } from 'date-fns';
import type { PageServerLoad } from './$types';
import type { MateriaDisponible } from '../../../../app';

export const load: PageServerLoad = async ({ fetch, locals: { usuario } }) => {
    const config = await obtenerConfiguracion(fetch);
    const { horario_inicio: inicio, horario_fin: fin }: { horario_inicio: Date, horario_fin: Date } = config;
    console.log(inicio, fin);
    console.log(isAfter(inicio, new Date()));
    if (isAfter(inicio, new Date())) {
        return {
            materiasDisponibles: [] as MateriaDisponible[],
            inscripcionAbierta: false
        }
    }

    // if (isAfter(new Date(), fin)) {
    // }
    const materiasDisponibles = await obtenerMateriasDisponibles(fetch, usuario?.cedula ?? '');

	return {
		materiasDisponibles
	};
};
