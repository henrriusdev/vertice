import {
	crearMateria,
	actualizarMateria,
	eliminarMateria,
	obtenerMaterias,
	obtenerCarreras,
	obtenerDocentes,
} from '$lib';
import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import type { MateriaReq } from '$lib/types';

export const load: PageServerLoad = async ({ fetch, parent }) => {
	const { rol } = await parent();
	if (!['control', 'administrador', 'coordinador'].includes(rol)) {
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
	async crear({ request, fetch }) {
		try {
			const data = await request.formData();
			const materia: MateriaReq = {
				id: data.get('id')?.toString() || '',
				nombre: data.get('nombre')?.toString() || '',
				prelacion: data.get('prelacion')?.toString() || '',
				unidad_credito: Number(data.get('unidad_credito')),
				hp: Number(data.get('hp')),
				ht: Number(data.get('ht')),
				semestre: Number(data.get('semestre')),
				id_carrera: data.get('id_carrera')?.toString() || '',
				horarios: JSON.parse(data.get('horarios')?.toString() || '[]'),
				ciclo: data.get('ciclo')?.toString() || '',
				modalidad: data.get('modalidad')?.toString() || '',
				maximo: Number(data.get('maximo')),
				id_docente: data.get('id_docente')?.toString() || ''
			};
			await crearMateria(materia, fetch);
			return { success: true, invalidate: true };
		} catch (error) {
			return { success: false, message: error instanceof Error ? error.message : 'Error desconocido' };
		}
	},

	// Acción para editar una materia
	edit: async ({ request, fetch }) => {
		const form = await request.formData();
		const payload: MateriaReq & { id: string } = {
			id: form.get('id')?.toString() as string,
			nombre: form.get('nombre')?.toString() as string,
			prelacion: form.get('prelacion')?.toString() as string,
			unidad_credito: Number(form.get('unidad_credito')),
			hp: Number(form.get('hp')),
			ht: Number(form.get('ht')),
			semestre: Number(form.get('semestre')),
			id_carrera: form.get('carrera')?.toString() || '',
			horarios: JSON.parse(form.get('horarios')?.toString() || '[]'),
			ciclo: form.get('ciclo')?.toString() as string,
			modalidad: form.get('modalidad')?.toString() as string,
			maximo: Number(form.get('maximo')),
			id_docente: form.get('docente')?.toString() || ''
		};

		const errores = validarPayload(payload);
		if (Object.keys(errores).length > 0) {
			return {
				type: 'failure',
				message: 'Errores en los datos del formulario'
			};
		}

		try {
			await actualizarMateria(fetch, payload.id, payload);
			return {
				type: 'success',
				message: 'Materia actualizada exitosamente',
				invalidate: true
			};
		} catch (error) {
			console.error('Error al editar materia:', error);
			return { type: 'failure', message: error instanceof Error ? error.message : 'Error desconocido' };
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
		} catch (error) {
			console.error('Error al eliminar materia:', error);
			return { type: 'failure', message: error instanceof Error ? error.message : 'Error desconocido' };
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
