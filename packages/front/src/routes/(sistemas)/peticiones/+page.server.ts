import type { Peticion } from '../../../app';
import type { PageServerLoad } from './$types';

export const load = (async ({locals:{usuario}}) => {
  const peticiones: Peticion[] = [{
    id: 1,
    id_estudiante: 2,
    id_docente: usuario?.id ?? 3,
    id_materia: 3,
    estado: 'pendiente',
    descripcion: 'hola',
    campo: '1'
  }]
    return {peticiones};
}) satisfies PageServerLoad;