export type Billete = {
	id: number;
	serial: string;
	monto: number;
	pago_id: number;
};

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
};

export type Docente = {
	id?: number;
	cedula: string;
	nombre: string;
	correo: string;
	usuario: number;
	titulo: string;
	dedicacion: string;
	especialidad: string;
	estatus: string;
	fecha_ingreso: string;
	observaciones: string;
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
};

export type Horario = {
	dia: string;
	hora_inicio: string;
	hora_fin: string;
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
	horarios: Horario[];
        ciclo: string;
        maximo: number;
        id_docente: number;
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
};

export type Peticion = {
	id: number;
	id_docente: number | object;
	descripcion: string;
	estado: string;
	id_estudiante: number | string | object;
	id_materia: string | object;
	campo: string;
	valor: number
};

export type Trazabilidad = {
	id: number;
	accion: string;
	usuario: number | object;
	fecha: string;
	modulo: string;
	nivel_alerta: number;
};

export type Usuario = {
	password?: string;
	id: number;
	cedula: string;
	nombre: string;
	correo: string;
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
	conflicto: false,
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

export interface PreguntaSeguridad{
	pregunta: string
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
