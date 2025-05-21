import type { PageServerLoad } from './$types';
import { obtenerConfiguracion, obtenerHistoricoMaterias } from '$lib';

export const load: PageServerLoad = async ({fetch}) => {
	const historico = await obtenerHistoricoMaterias(fetch);
	const config = await obtenerConfiguracion(fetch);
	const materiasActuales = historico.filter(m => config?.ciclo ? m.ciclo === config?.ciclo : true);
	return {historico: materiasActuales};
};