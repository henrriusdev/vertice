import { actualizarUsuario, crearUsuario, eliminarUsuario, obtenerUsuarios } from '$lib';
import type { Usuario } from '../../../../app';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	try {
		const res = await obtenerUsuarios(fetch);
		return { usuarios: res };
	} catch (error) {
		console.error('Error al obtener carreras:', error);
		return { usuarios: [] };
	}
};

export const actions: Actions = {
	// Acción para crear un usuario y un usuario
	create: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as Usuario;

		const usuario: Partial<Usuario & { password: string; rol_id: number }> = {
			id: 0,
			cedula: payload.cedula,
			correo: payload.correo,
			activo: true,
			nombre: payload.nombre,
			password: payload.password,
			rol_id: 3
		};

		try {
			const { data }: { data: Usuario } = await crearUsuario(fetch, usuario);
			return { usuario: data.nombre };
		} catch (error) {
			console.error('Error al crear carrera:', error);
			return { errores: { form: 'Error al crear el usuario' } };
		}
	},

	edit: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as Omit<
			Usuario,
			'rol'
		> & {
			rol: number;
		};

		console.log(payload);

		const usuario: Partial<Usuario & { password: string; rol_id: number }> = {
			cedula: payload.cedula,
			correo: payload.correo,
			activo: true,
			nombre: payload.nombre,
			rol_id: payload.rol
		};

		try {
			await actualizarUsuario(fetch, payload.id, usuario);
			return { usuario: usuario.nombre };
		} catch (error) {
			console.error('Error al editar usuario:', error);
			return { errores: { form: 'Error al editar el usuario' } };
		}
	},

	delete: async ({ request, fetch }) => {
		const formData = await request.formData();
		const cedula = formData.get('cedula')?.toString() || '';

		try {
			const res = await eliminarUsuario(fetch, cedula);
			console.log('carrera eliminada', res);
			return { exito: true };
		} catch (error) {
			console.error('Error al eliminar carrera:', error);
			return { errores: { form: 'Error al eliminar la carrera' } };
		}
	}
};
