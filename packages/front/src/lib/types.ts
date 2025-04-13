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