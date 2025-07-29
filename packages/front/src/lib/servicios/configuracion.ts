import { parse } from "date-fns";
import type { Configuracion } from "../../app";
import { apiCall, apiJson } from '$lib/utilidades/api';

const API = 'http://127.0.0.1:8000/api/configuracion/';

export const obtenerConfiguracion = async (fetch: typeof window.fetch) => {
  const res = await apiCall(fetch, `${API}`);
  if (res.status === 204) return null;
  const configuraciones = await res.json();
  return {...configuraciones.data, horario_inicio: new Date(configuraciones.data.horario_inicio), horario_fin: new Date(configuraciones.data.horario_fin), cuotas: configuraciones.data.cuotas.map((cuota: string) => parse(cuota, 'dd/MM/yyyy', new Date()))} as Configuracion;
};

export const actualizarConfiguracion = async (fetch: typeof window.fetch, configuracion: Configuracion) => {
  const configuraciones = await apiJson(fetch, `${API}update`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(configuracion)
  });
  return configuraciones.data as Configuracion;
};

export const crearConfiguracion = async (fetch: typeof window.fetch, configuracion: Configuracion) => {
  const configuraciones = await apiJson(fetch, `${API}add`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(configuracion)
  });
  return configuraciones.data as Configuracion;
};