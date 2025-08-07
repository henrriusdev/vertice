export type Carrera = {
	id: number;
	nombre: string;
};

export type Configuracion = {
	id?: number;
	ciclo: string;
	num_porcentaje: number;
	num_cuotas: number;
	horario_inicio: Date | string;
	horario_fin: Date | string;
	cuotas: Date[] | string[];
	porcentajes: number[];
};

export type Coordinador = {
	cedula: string;
	nombre: string;
	correo: string;
	usuario: number;
	carrera: number;
	telefono: string;
	activo: boolean;
};

export type Docente = {
	id?: number;
	cedula: string;
	nombre: string;
	correo: string;
	usuario: number;
	titulo: string;
	dedicacion: string;
	estatus: string;
	fecha_ingreso: string;
	observaciones: string;
	activo: boolean;
};

export type Estudiante = {
	usuario: Usuario;
	semestre: number;
	carrera: Carrera;
	promedio: number;
	direccion: string;
	fecha_nac: string;
	edad: number;
	sexo: string;
	cedula?: string;
	nombre?: string;
	correo?: string;
	activo?: boolean;
};

export type Horario = {
	dia: string;
	hora_inicio: string;
	hora_fin: string;
};

export type Asignacion = {
	id: number;
	nombre: string;
	horarios: Horario[];
	profesor: {
		id: number;
		nombre: string;
	} | null;
};

export type Materia = {
	id: string;
	nombre: string;
	prelacion: string;
	unidad_credito: number;
	hp: number;
	ht: number;
	semestre: number;
	id_carrera: number;
	ciclo: string;
	maximo: number;
	activo: boolean;
	asignaciones: Asignacion[];
};

export type Metodo_pago = {
	id: number;
	nombre: string;
};

export type Pago = {
	id: number;
	cedula_estudiante: number | Estudiante;
	metodo_pago: Metodo_pago | number;
	monto: number;
	concepto: string;
	fecha_pago: string;
	referencia_transferencia: string;
	ciclo: string;
	tasa_divisa?: number;
};

export type Peticion = {
	id: number;
	id_docente: number | object;
	descripcion: string;
	estado: string;
	id_estudiante: number | string | object;
	id_materia: string | object;
	campo: string;
	valor: number;
};

export type Trazabilidad = {
	id: number;
	accion: string;
	usuario: number | object;
	fecha: string;
	modulo: string;
	nivel_alerta: number;
	rol: string;
};

export type Usuario = {
	password?: string;
	id: number;
	cedula: string;
	nombre: string;
	correo: string;
	foto?: string | null;
	activo: boolean;
	fecha_creacion: string;
	cambiar_clave: boolean;
	pregunta_configurada: boolean;
	rol: { id: number; nombre: string };
};

export type MateriaInscrita = {
	id: string;
	nombre: string;
	codigo: string;
	ciclo: string;
	docente: string;
	horarios: {
		dia: string;
		hora_inicio: string;
		hora_fin: string;
	}[];
};

export type MateriaHistorico = {
	id: string;
	nombre: string;
	ciclo: string;
	docente: string;
	promedio: number;
	estatus: 'Aprobada' | 'Reprobada' | 'Cursando';
};

export type MateriaDisponible = {
	id: string;
	nombre: string;
	unidad_credito: number;
	prelacion: string | null;
	carrera: {
		id: string;
		nombre: string;
	};
};

export type MateriaDocente = {
	id: string;
	nombre: string;
	dia: string;
	hora_inicio: string;
	hora_fin: string;
	color: null;
	conflicto: false;
};

export interface MateriaCiclo {
	ciclo: string;
	materia: MateriaNota;
}

export interface MateriaNota {
	carrera: string;
	estudiantes: Nota[];
	id: string;
	nombre: string;
}

export interface Nota {
	cedula: string;
	nombre: string;
	notas: number[];
	promedio: number;
}

export interface PreguntaSeguridad {
	pregunta: string;
	respuesta: string;
	orden: number;
}

declare global {
	namespace App {
		interface Locals {
			usuario: Usuario | null;
		}
	}
}
