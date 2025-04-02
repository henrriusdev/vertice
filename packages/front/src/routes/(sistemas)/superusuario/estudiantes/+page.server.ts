import { actualizarEstudiante, actualizarUsuario, crearEstudiante, crearUsuario, eliminarEstudiante, obtenerCarreras, obtenerEstudiantes, type EstudianteReq } from "$lib";
import type { Usuario } from "../../../../app";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch }) => {
	try {
		const res = await obtenerEstudiantes(fetch);
		const carreras = await obtenerCarreras(fetch);
		return { carreras, estudiantes: res };
	} catch (error) {
		console.error('Error al obtener carreras:', error);
		return { carreras: [], estudiantes: [] };
	}
};

export const actions: Actions = {
	// Acción para crear un usuario y un estudiante
	create: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as EstudianteReq & (Usuario & {password:string})
		const usuario: Partial<Usuario & {password: string, rol_id: number}> = {
			id: 0,
			cedula: payload.cedula,
			correo: payload.correo,
			activo: true,
			nombre: payload.nombre,
			password: payload.password,
			rol_id: 5,
		}

		try {
			const {data}: {data: Usuario} = await crearUsuario(fetch, usuario);
			usuario.id = data.id;
		} catch (error) {
			console.error('Error al crear carrera:', error);
			return { errores: {nombre: 'Error al crear la carrera'} };
		}

		const estudiante: EstudianteReq = {
			carrera: payload.carrera,
			edad: payload.edad,
			fecha_nac: payload.fecha_nac,
			direccion: payload.direccion,
			semestre: payload.semestre,
			sexo: payload.sexo,
			promedio: payload.promedio,
			usuario: usuario.id,
		}

		try {
			 await crearEstudiante(fetch, estudiante)
			return {estudiante: usuario.nombre}
		} catch (e) {
			console.error(e)
		}
	},

	edit: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as EstudianteReq &
			Usuario & {id_estudiante: number};
		const usuario: Partial<Usuario & { password: string; rol_id: number }> = {
			cedula: payload.cedula,
			correo: payload.correo,
			activo: true,
			nombre: payload.nombre,
			rol_id: 5
		};

		try {
			await actualizarUsuario(fetch, payload.id, usuario);
		} catch (error) {
			console.error('Error al crear carrera:', error);
			return { errores: { nombre: 'Error al crear la carrera' } };
		}

		const estudiante: EstudianteReq = {
			carrera: payload.carrera,
			edad: payload.edad,
			fecha_nac: payload.fecha_nac,
			direccion: payload.direccion,
			semestre: payload.semestre,
			sexo: payload.sexo,
			promedio: payload.promedio,
			usuario: payload.id
		};

		try {
			await actualizarEstudiante(fetch, payload.id_estudiante, estudiante);
			return { estudiante: usuario.nombre };
		} catch (e) {
			console.error(e);
		}
	},

	delete: async ({ request, fetch }) => {
		const formData = await request.formData();
		const cedula = parseInt(formData.get('cedula')?.toString() || '0');

		try {
			const res = await eliminarEstudiante(fetch, cedula);
			console.log('carrera eliminada', res);
			return { exito: true };
		} catch (error) {
			console.error('Error al eliminar carrera:', error);
			return { errores: { nombre: 'Error al eliminar la carrera' } };
		}
	}
};

