export interface PensumActual {
  pensum_id: number;
  programa_id: number;
  programa_nombre: string;
  anio_creacion: number;
  es_activo: boolean;
  creditos_obligatorios_totales: number;
  total_materias_obligatorias: number;
  total_materias_electivas: number;
}

export interface Materia {
  materia_id: number;
  nombre_materia: string;
  creditos: number;
  es_electiva: boolean;
  semestre: number;
}

export interface MateriaPorSemestre {
  semestre: number;
  materias: Materia[];
  creditos_totales: number;
}

export interface PensumProgramaResponse {
  programa_id: number;
  programa_nombre: string;
  pensum_actual: PensumActual | null;
  message?: string;
}

// Nueva interfaz para la respuesta del endpoint de materias
export interface MateriasPensumResponse {
  message: string;
  materias: Materia[];
  total: number;
}