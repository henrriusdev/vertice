import { apiCall, apiJson } from '$lib/utilidades/api';

const API = 'http://127.0.0.1:8000/api/pregunta-seguridad';

export const PREGUNTAS_SEGURIDAD = [
    "¿Cuál es el nombre de tu primera mascota?",
    "¿En qué ciudad naciste?",
    "¿Cuál fue el nombre de tu primer colegio?",
    "¿Cuál es el segundo nombre de tu madre?",
    "¿Cuál es el nombre de tu mejor amigo de la infancia?",
    "¿En qué calle vivías cuando eras niño?"
];

export async function configurarPreguntaSeguridad(
    fetch: typeof window.fetch,
    preguntas: Array<{ pregunta: string; respuesta: string }>
) {
    return await apiJson(fetch, `${API}/configurar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(preguntas)
    });
}

export async function obtenerPreguntasSeguridad(
    fetch: typeof window.fetch,
    correo: string
) {
    return await apiJson(fetch, `${API}/obtener/${correo}`);
}


export async function verificarPreguntaSeguridad(
    fetch: typeof window.fetch,
    correo: string,
    respuesta: string,
    orden: number
) {
    return await apiJson(fetch, `${API}/verificar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo, respuesta, orden })
    });
}
