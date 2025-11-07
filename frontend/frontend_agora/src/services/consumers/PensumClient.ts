import { PensumProgramaResponse, MateriaPorSemestre, MateriasPensumResponse, PensumEstadisticas } from '../domain/PensumModels';
import { getToken } from './Auth';
const BASE_URL = 'http://localhost:8000/api/pensum';
const MATERIA_BASE_URL = 'http://localhost:8000/api/materia';

/** Obtener pensum actual (activo) de un programa */
export const obtenerPensumActual = async (programa_id: number): Promise<PensumProgramaResponse> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}/programa/${programa_id}/actual/`, {
    method: 'GET',
    headers,
  });

  // Intentar parseo seguro
  let data: any;
  try {
    data = await res.json();
  } catch (err) {
    // respuesta no JSON
    throw new Error('Invalid response from pensum API');
  }

  // Si el backend responde 404 cuando no existe pensum, devolver un objeto válido con pensum_actual = null
  if (!res.ok) {
    if (res.status === 404) {
      return {
        programa_id,
        programa_nombre: data?.programa_nombre || '',
        pensum_actual: null,
        message: data?.message || data?.error || 'No hay pensum activo'
      } as PensumProgramaResponse;
    }
    const msg = data?.error || data?.detail || data?.message || 'Error fetching pensum actual';
    throw new Error(msg);
  }

  return data as PensumProgramaResponse;
};

/** Obtener materias por pensum usando el endpoint de materias */
export const obtenerMateriasPorSemestre = async (pensum_id: number): Promise<MateriaPorSemestre[]> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${MATERIA_BASE_URL}/pensum/${pensum_id}/`, {
    method: 'GET',
    headers,
  });

  let data: any;
  try {
    data = await res.json();
  } catch (err) {
    throw new Error('Invalid response from materias API');
  }

  if (!res.ok) {
    const msg = data?.error || data?.detail || data?.message || 'Error fetching materias por pensum';
    throw new Error(msg);
  }

  const response = data as MateriasPensumResponse;
  
  // Normalizar: si el backend no provee `es_electiva` pero sí `es_obligatoria`,
  // marcar como electiva cuando `es_obligatoria === false`.
  response.materias = response.materias.map((m: any) => ({
    ...m,
    es_electiva:
      typeof m.es_electiva === 'boolean'
        ? m.es_electiva
        : (typeof m.es_obligatoria === 'boolean' ? !m.es_obligatoria : false),
  }));
  
  // Agrupar materias por semestre
  const materiasPorSemestre: MateriaPorSemestre[] = [];
  
  // Crear un mapa para agrupar por semestre
  const semestreMap = new Map<number, MateriaPorSemestre>();
  
  response.materias.forEach(materia => {
    const semestre = materia.semestre;
    
    if (!semestreMap.has(semestre)) {
      semestreMap.set(semestre, {
        semestre,
        materias: [],
        creditos_totales: 0
      });
    }
    
    const semestreData = semestreMap.get(semestre)!;
    semestreData.materias.push(materia);
    semestreData.creditos_totales += materia.creditos;
  });
  
  // Convertir el mapa a array y ordenar por semestre
  return Array.from(semestreMap.values()).sort((a, b) => a.semestre - b.semestre);
};

/** Obtener estadísticas de un pensum */
export const obtenerEstadisticasPensum = async (pensum_id: number): Promise<PensumEstadisticas> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}/${pensum_id}/estadisticas/`, {
    method: 'GET',
    headers,
  });

  let data: any;
  try {
    data = await res.json();
  } catch (err) {
    throw new Error('Invalid response from pensum estadisticas API');
  }

  if (!res.ok) {
    const msg = data?.error || data?.detail || data?.message || 'Error fetching pensum estadisticas';
    throw new Error(msg);
  }

  return data as PensumEstadisticas;
};

/** Crear nuevo pensum */
export const crearPensum = async (payload: {
  programa_id: number;
  anio_creacion?: number;
  es_activo?: boolean;
}): Promise<{ message: string; pensum: import('../domain/PensumModels').PensumActual }> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}/crear/`, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload),
  });

  let data: any;
  try {
    data = await res.json();
  } catch (err) {
    throw new Error('Invalid response from crear pensum API');
  }

  if (res.status === 201) {
    // éxito: devolver mensaje y objeto pensum
    return {
      message: data?.message || 'Pensum creado correctamente',
      pensum: data?.pensum as import('../domain/PensumModels').PensumActual,
    };
  }

  // manejar errores de validación / negocio
  const msg = data?.error || data?.detail || data?.message || 'Error creating pensum';
  throw new Error(msg);
}