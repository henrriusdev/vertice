import {
	crearMateria,
	actualizarMateria,
	eliminarMateria,
	obtenerMaterias,
	obtenerCarreras,
	obtenerDocentes,
	addToast
} from '$lib';
import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import type { MateriaReq } from '$lib/types';

export const load: PageServerLoad = async ({ fetch, parent }) => {
	const { rol } = await parent();
	if (!['control', 'superusuario', 'coordinador'].includes(rol)) {
		redirect(302, '/' + rol);
	}

	try {
		const data = await obtenerMaterias(fetch);
		const carreras = await obtenerCarreras(fetch);
		const docentes = await obtenerDocentes(fetch);

		return { materias: data.materias, carreras, docentes };
	} catch (error) {
		console.error('Error al obtener las materias:', error);
		return { materias: [], carreras: [], docentes: [] };
	}
};

export const actions: Actions = {
	// Acción para crear una materia
	create: async ({ request, fetch }) => {
		const form = await request.formData();
		const payload = Object.fromEntries(form) as unknown as MateriaReq;

		const errores = validarPayload(payload);
		if (Object.keys(errores).length > 0) {
			return {
				type: 'failure',
				message: 'Errores en los datos del formulario'
			};
		}

		const horarios = JSON.parse(form.getAll('horarios') as unknown as string) as unknown as {
			dia: string;
			inicio: string;
			fin: string;
		}[];

		payload.horarios = horarios;
		payload.prelacion = payload?.prelacion ?? '';

		try {
			await crearMateria(fetch, payload);
			return {
				type: 'success',
				message: 'Materia creada exitosamente',
				invalidate: true
			};
		} catch (error: any) {
			console.error('Error al crear materia:', error);
			return {
				type: 'failure',
				message: error.message
			};
		}
	},

	// Acción para editar una materia
	edit: async ({ request, fetch }) => {
		const form = await request.formData();
		const payload = Object.fromEntries(form) as unknown as MateriaReq & {
			id: string;
		};

		const errores = validarPayload(payload);
		if (Object.keys(errores).length > 0) {
			return {
				type: 'failure',
				message: 'Errores en los datos del formulario'
			};
		}

		const horarios = JSON.parse(form.getAll('horarios') as unknown as string) as unknown as {
			dia: string;
			inicio: string;
			fin: string;
		}[];

		payload.horarios = horarios;
		payload.prelacion = payload?.prelacion ?? '';

		try {
			await actualizarMateria(fetch, payload.id, payload);
			return {
				type: 'success',
				message: 'Materia actualizada exitosamente',
				invalidate: true
			};
		} catch (error: any) {
			console.error('Error al editar materia:', error);
			return {
				type: 'failure',
				message: error.message
			};
		}
	},

	// Acción para eliminar una materia
	delete: async ({ request, fetch }) => {
		const formData = await request.formData();
		const id = formData.get('id')?.toString() || '';

		try {
			await eliminarMateria(fetch, id);
			return {
				type: 'success',
				message: 'Materia eliminada exitosamente',
				invalidate: true
			};
		} catch (error: any) {
			console.error('Error al eliminar materia:', error);
			return {
				type: 'failure',
				message: error.message
			};
		}
	}
};

function validarPayload(
	payload: Record<string, string | number | boolean>
): Record<string, string> {
	const errores: Record<string, string> = {};
	const camposBase: (keyof typeof payload)[] = [
		'nombre',
		'unidad_credito',
		'hp',
		'ht',
		'semestre',
		'id_carrera',
		'modalidad',
		'maximo'
	];

	for (const campo of camposBase) {
		const valor = payload[campo];
		if (!valor || valor.toString().trim() === '') {
			errores[campo] = `El campo ${campo} es requerido`;
		}
	}

	return errores;
}
