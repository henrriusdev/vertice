import { obtenerEstudiantes } from "$lib";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch }) => {
  const estudiantes = await obtenerEstudiantes(fetch)
  return {estudiantes: estudiantes.map(est => est.cedula)}
  
}