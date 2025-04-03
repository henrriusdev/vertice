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
}