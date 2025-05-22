import {
	actualizarDocente,
	actualizarUsuario,
	crearDocente,
	crearUsuario,
	eliminarDocente,
	obtenerDocentes,
	type DocenteReq
} from '$lib';
import { redirect } from '@sveltejs/kit';
import type { Usuario } from '../../../app';
import type { Actions, PageServerLoad } from './$types';

export type ErroresDocente = {
	cedula?: string;
	nombre?: string;
	correo?: string;
	password?: string;
	titulo?: string;
	especialidad?: string;
	dedicacion?: string;
	estatus?: string;
	fecha_ingreso?: string;
	observaciones?: string;
	activo?: string;
};



export const load: PageServerLoad = async ({ fetch, parent }) => {
	const { rol } = await parent();
	if (!['control', 'superusuario', 'coordinador'].includes(rol)) {
		redirect(302, '/' + rol);
	}
	try {
		const res = await obtenerDocentes(fetch);
		return { docentes: res };
	} catch (error) {
		console.error('Error al obtener carreras:', error);
		return { carreras: [], docentes: [] };
	}
};

export const actions: Actions = {
	// Acción para crear un usuario y un docente
	create: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as DocenteReq &
			Usuario;
		
		const errores = validarPayload(payload as unknown as Record<string, string | number | boolean>, false);
		if (Object.keys(errores).length > 0) {
			return {
				type: 'failure',
				message: 'Errores en los datos del formulario'
			};
		}
		const usuario: Partial<Usuario & { password: string; rol_id: number }> = {
			id: 0,
			cedula: payload.cedula,
			correo: payload.correo,
			activo: true,
			nombre: payload.nombre,
			password: payload.password,
			rol_id: 6
		};

		try {
			const { data }: { data: Usuario } = await crearUsuario(fetch, usuario);
			usuario.id = data.id;
		} catch (error: any) {
			console.error('Error al crear usuario:', error);
			return {
				type: 'failure',
				message: error.message
			};
		}

		const docente: DocenteReq = {
			titulo: payload.titulo,
			dedicacion: payload.dedicacion,
			especialidad: payload.especialidad,
			estatus: payload.estatus,
			fecha_ingreso: payload.fecha_ingreso,
			observaciones: payload.observaciones,
			usuario_id: usuario.id,
		};

		try {
			await crearDocente(fetch, docente);
			return {
				type: 'success',
				message: `Docente ${usuario.nombre} creado exitosamente`,
				invalidate: true
			};
		} catch (e: any) {
			console.error('Error al crear docente:', e);
			return {
				type: 'failure',
				message: e.message
			};
		}
	},

	edit: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as DocenteReq &
			Usuario & { id_docente: number };
		
		const errores = validarPayload(payload as unknown as Record<string, string | number | boolean>, true);
		if (Object.keys(errores).length > 0) {
			return {
				type: 'failure',
				message: 'Errores en los datos del formulario'
			};
		}

		const usuario: Partial<Usuario & { password: string; rol_id: number }> = {
			cedula: payload.cedula,
			correo: payload.correo,
			activo: true,
			nombre: payload.nombre,
			rol_id: 6
		};

		try {
			await actualizarUsuario(fetch, payload.id, usuario);
		} catch (error: any) {
			console.error('Error al editar usuario:', error);
			return {
				type: 'failure',
				message: error.message
			};
		}

		const docente: DocenteReq = {
			titulo: payload.titulo,
			dedicacion: payload.dedicacion,
			especialidad: payload.especialidad,
			estatus: payload.estatus,
			fecha_ingreso: payload.fecha_ingreso,
			observaciones: payload.observaciones,
			usuario_id: payload.id,
			password: payload.password
		};

		try {
			await actualizarDocente(fetch, payload.id_docente, docente);
			return {
				type: 'success',
				message: `Docente ${usuario.nombre} actualizado exitosamente`,
				invalidate: true
			};
		} catch (e: any) {
			console.error('Error al actualizar docente:', e);
			return {
				type: 'failure',
				message: e.message
			};
		}
	},

	delete: async ({ request, fetch }) => {
		const formData = await request.formData();
		const cedula = formData.get('cedula')?.toString() || '';

		try {
			await eliminarDocente(fetch, cedula);
			return {
				type: 'success',
				message: 'Docente eliminado exitosamente',
				invalidate: true
			};
		} catch (error: any) {
			console.error('Error al eliminar docente:', error);
			return {
				type: 'failure',
				message: error.message
			};
		}
	}
};

function validarPayload(
	payload: Record<string, string | number | boolean>,
	isEditing: boolean
): ErroresDocente {
	const errores: ErroresDocente = {};

	// Campos requeridos comunes
	const camposBase: (keyof ErroresDocente)[] = [
		'cedula',
		'nombre',
		'correo',
		'titulo',
		'especialidad',
		'dedicacion',
		'estatus',
		'fecha_ingreso',
		'observaciones'
	];

	if (!isEditing) camposBase.push('password');

	for (const campo of camposBase) {
		const valor = payload[campo];
		if (!valor || valor.toString().trim() === '') {
			errores[campo] = `El campo ${campo} es requerido`;
		}
	}

	// Validaciones específicas
	if (payload.correo && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.correo as string)) {
		errores.correo = 'Correo inválido';
	}

	return errores;
}
