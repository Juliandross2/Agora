import { PensumProgramaResponse, MateriaPorSemestre, MateriasPensumResponse } from '../domain/PensumModels';
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

  if (!res.ok) {
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