import { obtenerCarreras } from "$lib";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch }) => {
  try {
    const res = await obtenerCarreras(fetch);
    return { carreras: res };
  } catch (error) {
    console.error('Error al obtener carreras:', error);
    return { carreras: [] };
  }
};
