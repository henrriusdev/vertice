import { actualizarCarrera, crearCarrera, eliminarCarrera, obtenerCarreras } from "$lib";
import type { Carrera } from "../../../../app";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch }) => {
  try {
    const res = await obtenerCarreras(fetch);
    console.log('carreras', res);
    return { carreras: res };
  } catch (error) {
    console.error('Error al obtener carreras:', error);
    return { carreras: [] };
  }
};

export const actions: Actions = {
  // Acción para crear una carrera
  create: async ({ request, fetch }) => {
    const formData = await request.formData();
    const carrera: Carrera = {
      id: 0,
      nombre: formData.get('nombre')?.toString() || '',
    };

    try {
      const res = await crearCarrera(fetch, carrera);
      console.log('carrera creada', res);
      return { exito: true };
    } catch (error) {
      console.error('Error al crear carrera:', error);
      return { errores: {nombre: 'Error al crear la carrera'} };
    }
  },

  edit: async ({ request, fetch }) => {
    const formData = await request.formData();
    const carrera: Carrera = {
      id: parseInt(formData.get('id')?.toString() || '0'),
      nombre: formData.get('nombre')?.toString() || '',
    };

    try {
      const res = await actualizarCarrera(fetch, carrera.id, carrera);
      console.log('carrera actualizada', res);
      return { exito: true };
    } catch (error) {
      console.error('Error al actualizar carrera:', error);
      return { errores: {nombre: 'Error al actualizar la carrera' } };
    }
  },

  delete: async ({ request, fetch }) => {
    const formData = await request.formData();
    const id = parseInt(formData.get('id')?.toString() || '0');

    try {
      const res = await eliminarCarrera(fetch, id);
      console.log('carrera eliminada', res);
      return { exito: true };
    } catch (error) {
      console.error('Error al eliminar carrera:', error);
      return { errores: { nombre: 'Error al eliminar la carrera' } };
    }
  }
};
