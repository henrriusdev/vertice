import {
	actualizarDocente,
	actualizarUsuario,
	crearDocente,
	crearUsuario,
	eliminarDocente,
	obtenerDocentes,
	type DocenteReq
} from '$lib';
import type { Usuario } from '../../../../app';
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



export const load: PageServerLoad = async ({ fetch }) => {
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
		console.log(errores);
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
			return { errores: { form: 'Error al crear el usuario' } as ErroresDocente };
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
			return { docente: usuario.nombre };
		} catch (e) {
			console.error(e);
			return { errores: { form: 'Error al crear el docente' } as ErroresDocente };
		}
	},

	edit: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as DocenteReq &
			Usuario & { id_docente: number };
		
		console.log(payload);
		const errores = validarPayload(payload as unknown as Record<string, string | number | boolean>, true);
		if (Object.keys(errores).length > 0) {
			return { errores };
		}
		console.log(errores);

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
			return { errores: { form: 'Error al editar el usuario' } as ErroresDocente };
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
			return { docente: usuario.nombre };
		} catch (e) {
			console.error(e);
			return { errores: { form: 'Error al editar el docente' } as ErroresDocente };
		}
	},

	delete: async ({ request, fetch }) => {
		const formData = await request.formData();
		const cedula = formData.get('cedula')?.toString() || '';

		try {
			const res = await eliminarDocente(fetch, cedula);
			console.log('carrera eliminada', res);
			return { exito: true };
		} catch (error) {
			console.error('Error al eliminar carrera:', error);
			return { errores: { form: 'Error al eliminar la carrera' } as ErroresDocente };
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
