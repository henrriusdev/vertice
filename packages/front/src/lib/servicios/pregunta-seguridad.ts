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
    pregunta: string,
    respuesta: string
) {
    const res = await fetch(`${API}/configurar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta, respuesta })
    });

    if (!res.ok) {
        const err = await res.json();
        throw new Error(err?.data?.message ?? 'Error al configurar pregunta');
    }

    return await res.json();
}

export async function obtenerPreguntaSeguridad(
    fetch: typeof window.fetch,
    correo: string
) {
    const res = await fetch(`${API}/obtener/${correo}`);
    
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err?.data?.message ?? 'Error al obtener pregunta');
    }

    return await res.json();
}

export async function verificarPreguntaSeguridad(
    fetch: typeof window.fetch,
    correo: string,
    respuesta: string
) {
    const res = await fetch(`${API}/verificar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo, respuesta })
    });

    if (!res.ok) {
        const err = await res.json();
        throw new Error(err?.data?.message ?? 'Error al verificar respuesta');
    }

    return await res.json();
}
