export interface Billete {
	id: number;
	serial: string;
	monto: number;
	pago_id: number;
}

export interface Carrera {
	id: number;
	nombre: string;
}

export interface Configuracion {
	id: number;
	ciclo: string;
	num_porcentaje: number;
	num_cuotas: number;
	horario_inicio: string;
	horario_fin: string;
	cuotas: number[];
	porcentajes: number[];
}

export interface Coordinador {
	usuario: number | object;
	carrera: number | object;
	telefono: string;
}

export interface Docente {
	usuario: number | object;
	titulo: string;
	dedicacion: string;
	especialidad: string;
	estatus: string;
	fecha_ingreso: string;
	observaciones: string;
}

export interface Estudiante {
	usuario: number | object;
	semestre: number;
	carrera: number | object;
	promedio: number;
	direccion: string;
	fecha_nac: string;
	edad: number;
	sexo: string;
}

export interface Horario {
	dia: string;
	hora_inicio: string;
	hora_fin: string;
}

export interface Materia {
	id: string;
	nombre: string;
	prelacion: string;
	unidad_credito: number;
	hp: number;
	ht: number;
	semestre: number;
	id_carrera: number | object;
	horarios: Horario[];
	ciclo: string;
	modalidad: string;
	maximo: number;
	id_docente: number | object;
}

export interface Matricula {
	id: number;
	cod_materia: number | object;
	cedula_estudiante: number | object;
	notas: number[];
	uc: number;
	ciclo: string;
}

export interface Metodo_pago {
	id: number;
	nombre: string;
}

export interface Pago {
	id: number;
	cedula_estudiante: number | object;
	metodo_pago: number | object;
	monto: number;
	concepto: string;
	fecha_pago: string;
	referencia_transferencia: string;
	ciclo: string;
}

export interface Peticion {
	id: number;
	id_docente: number | object;
	descripcion: string;
	estado: string;
	id_estudiante: number | object;
	id_materia: number | object;
	campo: string;
}

export interface Sesion_activa {
	id: number;
	usuario: number | object;
	jti: string;
	creado_en: string;
}

export interface Trazabilidad {
	id: number;
	accion: string;
	usuario: number | object;
	fecha: string;
	modulo: string;
	nivel_alerta: number;
}

export interface Usuario {
	id: number;
	cedula: string;
	nombre: string;
	correo: string;
	activo: boolean;
	ruta_foto: string;
	fecha_creacion: string;
	ultima_sesion: string;
	rol: { id: number; nombre: string };
}

declare global {
	namespace App {
		interface Locals {
			usuario: Usuario | null;
		}
	}
}