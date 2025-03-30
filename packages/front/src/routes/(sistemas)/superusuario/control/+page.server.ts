import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';


interface EstudianteCompleto {
	id?: number;
	cedula: string;
	nombre: string;
	correo: string;
	activo: boolean;
	ruta_foto: string;
	fecha_creacion?: string;
	ultima_sesion?: string;
	rol?: { id: number; nombre: string };
	semestre: number;
	carrera: number | { id: number; nombre: string };
	promedio: number;
	direccion: string;
	fecha_nac: string;
	edad: number;
	sexo: string;
}

// Datos de ejemplo para carreras
const carreras = [
	{ id: 1, nombre: 'Ingeniería Informática' },
	{ id: 2, nombre: 'Ingeniería Civil' },
	{ id: 3, nombre: 'Medicina' },
	{ id: 4, nombre: 'Derecho' },
	{ id: 5, nombre: 'Administración de Empresas' }
];

// Datos de ejemplo para estudiantes (en una aplicación real, esto vendría de una base de datos)
let estudiantes: EstudianteCompleto[] = [
	{
		id: 1,
		cedula: '12345678',
		nombre: 'Juan Pérez',
		correo: 'juan.perez@ejemplo.com',
		activo: true,
		ruta_foto: '/placeholder.svg?height=40&width=40',
		fecha_creacion: '2023-01-15',
		ultima_sesion: '2023-12-01',
		rol: { id: 3, nombre: 'estudiante' },
		semestre: 5,
		carrera: { id: 1, nombre: 'Ingeniería Informática' },
		promedio: 8.7,
		direccion: 'Calle Principal #123, Ciudad',
		fecha_nac: '2000-05-20',
		edad: 23,
		sexo: 'M'
	},
	{
		id: 2,
		cedula: '87654321',
		nombre: 'María García',
		correo: 'maria.garcia@ejemplo.com',
		activo: true,
		ruta_foto: '/placeholder.svg?height=40&width=40',
		fecha_creacion: '2023-02-10',
		ultima_sesion: '2023-11-28',
		rol: { id: 3, nombre: 'estudiante' },
		semestre: 3,
		carrera: { id: 3, nombre: 'Medicina' },
		promedio: 9.2,
		direccion: 'Avenida Central #456, Ciudad',
		fecha_nac: '2001-08-15',
		edad: 22,
		sexo: 'F'
	},
	{
		id: 3,
		cedula: '23456789',
		nombre: 'Carlos Rodríguez',
		correo: 'carlos.rodriguez@ejemplo.com',
		activo: false,
		ruta_foto: '/placeholder.svg?height=40&width=40',
		fecha_creacion: '2023-03-05',
		ultima_sesion: '2023-10-15',
		rol: { id: 3, nombre: 'estudiante' },
		semestre: 7,
		carrera: { id: 2, nombre: 'Ingeniería Civil' },
		promedio: 7.8,
		direccion: 'Calle Secundaria #789, Ciudad',
		fecha_nac: '1999-11-30',
		edad: 24,
		sexo: 'M'
	},
	{
		id: 4,
		cedula: '34567890',
		nombre: 'Ana Martínez',
		correo: 'ana.martinez@ejemplo.com',
		activo: true,
		ruta_foto: '/placeholder.svg?height=40&width=40',
		fecha_creacion: '2023-04-20',
		ultima_sesion: '2023-11-30',
		rol: { id: 3, nombre: 'estudiante' },
		semestre: 2,
		carrera: { id: 4, nombre: 'Derecho' },
		promedio: 8.5,
		direccion: 'Avenida Principal #321, Ciudad',
		fecha_nac: '2002-03-25',
		edad: 21,
		sexo: 'F'
	},
	{
		id: 5,
		cedula: '45678901',
		nombre: 'Pedro López',
		correo: 'pedro.lopez@ejemplo.com',
		activo: true,
		ruta_foto: '/placeholder.svg?height=40&width=40',
		fecha_creacion: '2023-05-12',
		ultima_sesion: '2023-11-25',
		rol: { id: 3, nombre: 'estudiante' },
		semestre: 9,
		carrera: { id: 5, nombre: 'Administración de Empresas' },
		promedio: 8.9,
		direccion: 'Calle Terciaria #654, Ciudad',
		fecha_nac: '1998-07-10',
		edad: 25,
		sexo: 'M'
	}
];

// Función para validar los datos del estudiante
function validarEstudiante(formData: FormData) {
	const cedula = formData.get('cedula')?.toString();
	const nombre = formData.get('nombre')?.toString();
	const correo = formData.get('correo')?.toString();
	const semestre = parseInt(formData.get('semestre')?.toString() || '0');
	const carreraId = parseInt(formData.get('carrera')?.toString() || '0');
	const promedio = parseFloat(formData.get('promedio')?.toString() || '0');
	const direccion = formData.get('direccion')?.toString();
	const fecha_nac = formData.get('fecha_nac')?.toString();
	const sexo = formData.get('sexo')?.toString();

	const errores: Record<string, string> = {};

	if (!cedula || cedula.length < 5) {
		errores.cedula = 'La cédula es requerida y debe tener al menos 5 caracteres';
	}

	if (!nombre || nombre.length < 3) {
		errores.nombre = 'El nombre es requerido y debe tener al menos 3 caracteres';
	}

	if (!correo || !correo.includes('@')) {
		errores.correo = 'El correo electrónico es requerido y debe ser válido';
	}

	if (!semestre || semestre < 1 || semestre > 10) {
		errores.semestre = 'El semestre debe estar entre 1 y 10';
	}

	if (!carreraId || !carreras.some((c) => c.id === carreraId)) {
		errores.carrera = 'Debe seleccionar una carrera válida';
	}

	if (promedio < 0 || promedio > 10) {
		errores.promedio = 'El promedio debe estar entre 0 y 10';
	}

	if (!fecha_nac) {
		errores.fecha_nac = 'La fecha de nacimiento es requerida';
	}

	if (!sexo || (sexo !== 'M' && sexo !== 'F')) {
		errores.sexo = 'Debe seleccionar un sexo válido';
	}

	return errores;
}

// Cargar datos para la página
export const load: PageServerLoad = async () => {
	return {
		estudiantes,
		carreras
	};
};

// Acciones del servidor
export const actions: Actions = {
	// Acción para crear un nuevo estudiante
	create: async ({ request }) => {
		const formData = await request.formData();
		const errores = validarEstudiante(formData);

		if (Object.keys(errores).length > 0) {
			return fail(400, { errores, values: Object.fromEntries(formData) });
		}

		try {
			// Obtener datos del formulario
			const cedula = formData.get('cedula')?.toString() || '';
			const nombre = formData.get('nombre')?.toString() || '';
			const correo = formData.get('correo')?.toString() || '';
			const activo = formData.get('activo') === 'on';
			const semestre = parseInt(formData.get('semestre')?.toString() || '1');
			const carreraId = parseInt(formData.get('carrera')?.toString() || '1');
			const promedio = parseFloat(formData.get('promedio')?.toString() || '0');
			const direccion = formData.get('direccion')?.toString() || '';
			const fecha_nac = formData.get('fecha_nac')?.toString() || '';
			const sexo = formData.get('sexo')?.toString() || 'M';

			// Calcular edad
			const hoy = new Date();
			const fechaNac = new Date(fecha_nac);
			let edad = hoy.getFullYear() - fechaNac.getFullYear();
			const mes = hoy.getMonth() - fechaNac.getMonth();
			if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())) {
				edad--;
			}

			// Encontrar la carrera por ID
			const carreraObj = carreras.find((c) => c.id === carreraId);
			if (!carreraObj) {
				return fail(400, { error: 'Carrera no encontrada' });
			}

			// Crear nuevo estudiante
			const nuevoId = Math.max(...estudiantes.map((est) => est.id || 0)) + 1;
			const nuevoEstudiante: EstudianteCompleto = {
				id: nuevoId,
				cedula,
				nombre,
				correo,
				activo,
				ruta_foto: '/placeholder.svg?height=40&width=40',
				fecha_creacion: new Date().toISOString().split('T')[0],
				ultima_sesion: '',
				rol: { id: 3, nombre: 'estudiante' },
				semestre,
				carrera: carreraObj,
				promedio,
				direccion,
				fecha_nac,
				edad,
				sexo
			};

			// Agregar a la lista (en una aplicación real, esto sería una inserción en la base de datos)
			estudiantes = [...estudiantes, nuevoEstudiante];

			return { success: true, message: 'Estudiante creado exitosamente' };
		} catch (error) {
			console.error('Error al crear estudiante:', error);
			return fail(500, { error: 'Error al crear el estudiante' });
		}
	},

	// Acción para editar un estudiante existente
	edit: async ({ request }) => {
		const formData = await request.formData();
		const errores = validarEstudiante(formData);

		if (Object.keys(errores).length > 0) {
			return fail(400, { errores, values: Object.fromEntries(formData) });
		}

		try {
			const id = parseInt(formData.get('id')?.toString() || '0');
			if (!id) {
				return fail(400, { error: 'ID de estudiante no válido' });
			}

			// Verificar si el estudiante existe
			const index = estudiantes.findIndex((est) => est.id === id);
			if (index === -1) {
				return fail(404, { error: 'Estudiante no encontrado' });
			}

			// Obtener datos del formulario
			const cedula = formData.get('cedula')?.toString() || '';
			const nombre = formData.get('nombre')?.toString() || '';
			const correo = formData.get('correo')?.toString() || '';
			const activo = formData.get('activo') === 'on';
			const semestre = parseInt(formData.get('semestre')?.toString() || '1');
			const carreraId = parseInt(formData.get('carrera')?.toString() || '1');
			const promedio = parseFloat(formData.get('promedio')?.toString() || '0');
			const direccion = formData.get('direccion')?.toString() || '';
			const fecha_nac = formData.get('fecha_nac')?.toString() || '';
			const sexo = formData.get('sexo')?.toString() || 'M';

			// Calcular edad
			const hoy = new Date();
			const fechaNac = new Date(fecha_nac);
			let edad = hoy.getFullYear() - fechaNac.getFullYear();
			const mes = hoy.getMonth() - fechaNac.getMonth();
			if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())) {
				edad--;
			}

			// Encontrar la carrera por ID
			const carreraObj = carreras.find((c) => c.id === carreraId);
			if (!carreraObj) {
				return fail(400, { error: 'Carrera no encontrada' });
			}

			// Actualizar estudiante
			const estudianteActualizado: EstudianteCompleto = {
				...estudiantes[index],
				cedula,
				nombre,
				correo,
				activo,
				semestre,
				carrera: carreraObj,
				promedio,
				direccion,
				fecha_nac,
				edad,
				sexo
			};

			// Actualizar en la lista
			estudiantes[index] = estudianteActualizado;
			estudiantes = [...estudiantes]; // Para forzar la actualización

			return { success: true, message: 'Estudiante actualizado exitosamente' };
		} catch (error) {
			console.error('Error al actualizar estudiante:', error);
			return fail(500, { error: 'Error al actualizar el estudiante' });
		}
	},

	// Acción para eliminar un estudiante
	delete: async ({ request }) => {
		const formData = await request.formData();
		const id = parseInt(formData.get('id')?.toString() || '0');

		if (!id) {
			return fail(400, { error: 'ID de estudiante no válido' });
		}

		try {
			// Verificar si el estudiante existe
			const index = estudiantes.findIndex((est) => est.id === id);
			if (index === -1) {
				return fail(404, { error: 'Estudiante no encontrado' });
			}

			// Eliminar de la lista
			estudiantes = estudiantes.filter((est) => est.id !== id);

			return { success: true, message: 'Estudiante eliminado exitosamente' };
		} catch (error) {
			console.error('Error al eliminar estudiante:', error);
			return fail(500, { error: 'Error al eliminar el estudiante' });
		}
	}
};
