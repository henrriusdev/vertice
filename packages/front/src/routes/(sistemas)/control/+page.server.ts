import type { PageServerLoad } from './$types';
import type { PageData } from './types';
import { obtenerEstudiantes } from '$lib/servicios/estudiantes';
import { obtenerDocentes } from '$lib/servicios/docentes';
import { obtenerMaterias } from '$lib/servicios/materias';
import { obtenerCarreras } from '$lib/servicios/carreras';
import { obtenerPagosPorDia } from '$lib/servicios/pagos';
import { obtenerPeticiones } from '$lib/servicios/peticiones';
import { filtrarTrazabilidad } from '$lib/servicios/trazabilidad';

export const load = (async ({ fetch }) => {
    // Obtener datos para estadísticas
    const [estudiantes, docentes, { materias }, carreras] = await Promise.all([
        obtenerEstudiantes(fetch),
        obtenerDocentes(fetch),
        obtenerMaterias(fetch),
        obtenerCarreras(fetch)
    ]);

    // Calcular estadísticas
    const estadisticas = {
        estudiantes: estudiantes.length,
        docentes: docentes.length,
        materias: materias.length,
        carreras: carreras.length
    };

    // Calcular distribución por carrera
    const distribucionCarreras = carreras.map(carrera => ({
        nombre: carrera.nombre,
        estudiantes: estudiantes.filter(e => e.carrera.id === carrera.id).length
    }));

    // Calcular promedios por carrera
    const promediosCarreras = carreras.map(carrera => {
        const estudiantesCarrera = estudiantes.filter(e => e.carrera.id === carrera.id);
        const promedio = estudiantesCarrera.reduce((acc, e) => acc + (e.promedio || 0), 0) / estudiantesCarrera.length;
        return {
            nombre: carrera.nombre,
            promedio: promedio || 0
        };
    });

    // Obtener últimas sesiones (trazabilidad)
    const sesiones = await filtrarTrazabilidad({
        busqueda: 'sesion'
    }, fetch);

    // Obtener últimos pagos
    const pagos = await obtenerPagosPorDia(fetch, 5);

    // Obtener peticiones pendientes
    const peticiones = await obtenerPeticiones(fetch);

    return {
        estadisticas,
        distribucionCarreras,
        promediosCarreras,
        sesiones: sesiones.slice(0, 5).map(s => ({
            usuario: 'Usuario',
            fecha: s.fecha,
            estado: 'activa'
        })),
        pagos: Object.entries(pagos).map(([fecha, monto]) => ({
            estudiante: fecha,
            monto: Number(monto),
            estado: 'aprobado' as const
        })).slice(0, 5),
        peticiones: peticiones.slice(0, 5).map(p => ({
            estudiante: p.estudiante.nombre,
            tipo: p.peticion.campo,
            estado: p.peticion.estado
        }))
    } satisfies PageData;
}) satisfies PageServerLoad;