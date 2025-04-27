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
	modalidad: string;
	maximo: number;
	id_docente: number;
};

export type Matricula = {
	id: number;
	cod_materia: number | object;
	cedula_estudiante: number | object;
	notas: number[];
	uc: number;
	ciclo: string;
};

export type Metodo_pago = {
	id: number;
	nombre: string;
};

export type Pago = {
	id: number;
	cedula_estudiante: number | object;
	metodo_pago: number | object;
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
	id_estudiante: number | object;
	id_materia: number | object;
	campo: string;
};

export type SesionActiva = {
	id: number;
	usuario: number | object;
	jti: string;
	creado_en: string;
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
	ruta_foto?: string;
	fecha_creacion: string;
	ultima_sesion?: string;
	rol: { id: number; nombre: string };
};

export type MateriaInscrita = {
	id: string;
	nombre: string;
	codigo: string;
	ciclo: string;
	docente: string;
	horario: {
		dia: string;
		hora_inicio: string;
		hora_fin: string;
	}[];
};

export type MateriaHistorico = {
	id: string;
	nombre: string;
	codigo: string;
	ciclo: string;
	docente: string;
	nota_final: number;
	estatus: 'Aprobada' | 'Reprobada' | 'Cursando';
};

export type MateriaDisponible = {
	id: string;
	nombre: string;
	codigo: string;
	creditos: number;
	prelacion: string | null;
	carrera: {
		id: string;
		nombre: string;
	};
};

declare global {
	namespace App {
		interface Locals {
			usuario: Usuario | null;
		}
	}
}
