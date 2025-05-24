export type EstudianteReq = {
	id?: number | null;
	usuario: number;
	semestre: number;
	carrera: number;
	promedio: number;
	direccion: string;
	fecha_nac: string;
	edad: number;
	sexo: string;
};

export type DocenteReq = {
	usuario_id: number;
	titulo: string;
	dedicacion: string;
	password?: string;
	especialidad: string;
	estatus: string;
	fecha_ingreso: string;
	observaciones: string;
};

export type CoordinadorReq = {
	usuario_id?: number;
	carrera_id: number;
	telefono: string;
	password?: string;
};

export type Billete = {
	denominacion: string; // Bs. 5.00, 10.00, etc.
	cantidad: number; // siempre será 1 en tu backend actual
};

export type Pago = {
	id: number;
	fecha: string; // formateado dd-mm-YYYY
	monto: string; // Bs. como string, ej: "300.00"
	metodo: string; // "Transferencia", "Billete", etc.
	descripcion: string;
	ciclo: string;
	referencia?: string;
	estudiante: string; // nombre completo
	billetes?: Billete[]; // solo si el método es "Billete"
};

export type PagosEstudianteResponse = {
	nombre: string;
	pagos: Pago[];
};

export type MateriaReq = {
	id: string;
	nombre: string;
	prelacion: string;
	unidad_credito: number;
	hp: number;
	ht: number;
	semestre: number;
	id_carrera: string;
	ciclo: string;
	modalidad?: string;
	maximo?: number;
	id_docente?: string;
	horarios: { dia: string; inicio: string; fin: string }[];
}

export type Peticion = {
  docente: {
    cedula: string
    nombre: string
  }
  estudiante: {
    cedula: string
    nombre: string
  }
  materia: {
    id: string
    nombre: string
  }
  peticion: {
    campo: string
    descripcion: string
    estado: string
    id: number
    id_docente: number
    id_estudiante: number
    id_materia: string
  }
}

export type FiltroTrazabilidad = {
	busqueda?: string
	fechaDesde?: string
	fechaHasta?: string
	rol?: string
}

// Interfaz para los parámetros de exportación
export interface ExportacionParams {
	formato: string
	busqueda?: string
	fechaDesde?: string
	fechaHasta?: string
	rol?: string
}
