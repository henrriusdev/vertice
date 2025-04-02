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