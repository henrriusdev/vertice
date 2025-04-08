import {
	actualizarEstudiante,
	actualizarUsuario,
	crearEstudiante,
	crearUsuario,
	eliminarEstudiante,
	obtenerCarreras,
	obtenerEstudiantes,
	type EstudianteReq
} from '$lib';
import { redirect } from '@sveltejs/kit';
import type { Usuario } from '../../../app';
import type { Actions, PageServerLoad } from './$types';

type ErroresEstudiante = {
	cedula?: string;
	nombre?: string;
	correo?: string;
	fecha_nac?: string;
	carrera?: string;
	sexo?: string;
	semestre?: string;
	promedio?: string;
	direccion?: string;
	password?: string;
	activo?: string;
};


export const load: PageServerLoad = async ({ fetch, parent }) => {
	const { rol } = await parent();
	if (!['caja', 'superusuario'].includes(rol)) {
		redirect(302, '/'+rol);
	}
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
		const payload = Object.fromEntries(await request.formData()) as unknown as EstudianteReq &
			(Usuario & { password: string });
		
		const errores = validarPayload(payload as unknown as Record<string, string | number | boolean>, false);
		if (Object.keys(errores).length > 0) {
			return { errores };
		}
		const usuario: Partial<Usuario & { password: string; rol_id: number }> = {
			id: 0,
			cedula: payload.cedula,
			correo: payload.correo,
			activo: true,
			nombre: payload.nombre,
			password: payload.password,
			rol_id: 5
		};

		try {
			const { data }: { data: Usuario } = await crearUsuario(fetch, usuario);
			usuario.id = data.id;
		} catch (error) {
			console.error('Error al crear carrera:', error);
			return { errores: { form: 'Error al crear el usuario' } as ErroresEstudiante };
		}

		const estudiante: EstudianteReq = {
			carrera: payload.carrera,
			edad: payload.edad,
			fecha_nac: payload.fecha_nac,
			direccion: payload.direccion,
			semestre: payload.semestre,
			sexo: payload.sexo,
			promedio: payload.promedio,
			usuario: usuario.id
		};

		try {
			await crearEstudiante(fetch, estudiante);
			return { estudiante: usuario.nombre };
		} catch (e) {
			console.error(e);
			return { errores: { form: 'Error al crear el estudiante' } as ErroresEstudiante };
		}
	},

	edit: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as EstudianteReq &
			Usuario & { id_estudiante: number };
		
		const errores = validarPayload(payload as unknown as Record<string, string | number | boolean>, true);
		if (Object.keys(errores).length > 0) {
			return { errores };
		}

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
			console.error('Error al editar usuario:', error);
			return { errores: { form: 'Error al editar el usuario' } as ErroresEstudiante };
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
			return { errores: { form: 'Error al editar el estudiante' } as ErroresEstudiante };
		}
	},

	delete: async ({ request, fetch }) => {
		const formData = await request.formData();
		const cedula = formData.get('cedula')?.toString() || '';

		try {
			const res = await eliminarEstudiante(fetch, cedula);
			console.log('carrera eliminada', res);
			return { exito: true };
		} catch (error) {
			console.error('Error al eliminar carrera:', error);
			return { errores: { form: 'Error al eliminar la carrera' } as ErroresEstudiante };
		}
	}
};

function validarPayload(payload: Record<string, string | number | boolean>, isEditing: boolean): ErroresEstudiante {
	const errores: ErroresEstudiante = {};

	const camposBase: (keyof ErroresEstudiante)[] = [
		'cedula',
		'nombre',
		'correo',
		'fecha_nac',
		'carrera',
		'sexo',
		'semestre',
		'promedio',
		'direccion'
	];

	if (!isEditing) camposBase.push('password');
	if (isEditing) camposBase.push('activo');

	for (const campo of camposBase) {
		const valor = payload[campo];
		if (!valor || valor.toString().trim() === '') {
			errores[campo] = `El campo ${campo} es requerido`;
		}
	}

	if (payload.correo && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.correo as string)) {
		errores.correo = 'Correo inválido';
	}

	if (
		payload.promedio &&
		(isNaN(payload.promedio as number) || Number(payload.promedio) < 0 || Number(payload.promedio) > 20)
	) {
		errores.promedio = 'Promedio debe estar entre 0 y 20';
	}

	return errores;
}
