import {
	crearMateria,
	actualizarMateria,
	eliminarMateria,
	obtenerMaterias,
	obtenerCarreras,
	obtenerDocentes
} from '$lib';
import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import type { MateriaReq } from '$lib/types';

export const load: PageServerLoad = async ({ fetch, parent }) => {
	const { rol } = await parent();
	if (!['caja', 'superusuario', 'coordinador'].includes(rol)) {
		redirect(302, '/' + rol);
	}

	try {
		const data = await obtenerMaterias(fetch);
		const carreras = await obtenerCarreras(fetch);
		const docentes = await obtenerDocentes(fetch);

		console.log('materias', data);
		return { materias: data.materias, carreras, docentes };
	} catch (error) {
		console.error('Error al obtener las materias:', error);
		return { materias: [], carreras: [], docentes: [] };
	}
};

export const actions: Actions = {
	// Acción para crear una materia
	create: async ({ request, fetch }) => {
		const form = await request.formData()
		const payload = Object.fromEntries(form) as unknown as MateriaReq;

		const errores = validarPayload(payload);
		if (Object.keys(errores).length > 0) {
			return { errores };
		}

		let horarios = JSON.parse(form.getAll('horarios') as unknown as string) as unknown as {
			dia: string;
			inicio: string;
			fin: string;
		}[];

		payload.horarios = horarios
		payload.prelacion = payload?.prelacion ?? ''

		try {
			await crearMateria(fetch, payload);
			return { materia: payload.nombre };
		} catch (error) {
			console.error('Error al crear materia:', error);
			return { errores: { form: 'Error al crear la materia' } };
		}
	},

	// Acción para editar una materia
	edit: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as MateriaReq & {
			id: string;
		};

		const errores = validarPayload(payload);
		if (Object.keys(errores).length > 0) {
			return { errores };
		}

		try {
			await actualizarMateria(fetch, payload.id, payload);
			return { materia: payload.nombre };
		} catch (error) {
			console.error('Error al editar materia:', error);
			return { errores: { form: 'Error al editar la materia' } };
		}
	},

	// Acción para eliminar una materia
	delete: async ({ request, fetch }) => {
		const formData = await request.formData();
		const id = formData.get('id')?.toString() || '';

		try {
			await eliminarMateria(fetch, id);
			console.log('Materia eliminada', id);
			return { exito: true };
		} catch (error) {
			console.error('Error al eliminar materia:', error);
			return { errores: { form: 'Error al eliminar la materia' } };
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
