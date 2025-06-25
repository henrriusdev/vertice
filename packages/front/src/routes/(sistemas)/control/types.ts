// Tipos para las estadísticas generales
export interface Estadisticas {
    estudiantes: number;
    docentes: number;
    materias: number;
    carreras: number;
}

// Tipos para la distribución de estudiantes por carrera
export interface DistribucionCarrera {
    nombre: string;
    estudiantes: number;
}

// Tipos para los promedios por carrera
export interface PromedioCarrera {
    nombre: string;
    promedio: number;
}


// Tipos para los pagos
export interface Pago {
    estudiante: string;
    monto: number;
    estado: 'aprobado' | 'pendiente';
}

// Tipos para las peticiones
export interface Peticion {
    estudiante: string;
    tipo: string;
    estado: string;
}

// Tipo principal para los datos de la página
export interface PageData {
    estadisticas: Estadisticas;
    distribucionCarreras: DistribucionCarrera[];
    promediosCarreras: PromedioCarrera[];
    pagos: Pago[];
    peticiones: Peticion[];
}
