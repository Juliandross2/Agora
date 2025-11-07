
/**
 * Modelo de electiva 
 */
export interface Electiva {
  electiva_id: number;
  programa_id: number;
  nombre_electiva: string;
  es_activa: boolean;
  created_at?: string;
  updated_at?: string;
}

/* Payloads y respuestas */
export interface ElectivaCreatePayload {
  programa_id: number;
  nombre_electiva: string;
  es_activa?: boolean;
}

export interface CrearElectivaResponse {
  message: string;
  electiva: Electiva;
}

export interface ElectivaUpdatePayload {
  nombre_electiva?: string;
  es_activa?: boolean;
  programa_id?: number;
}

export interface ActualizarElectivaResponse {
  message: string;
  electiva: Electiva;
}

export interface EliminarElectivaResponse {
  message: string;
}

export interface ListarElectivasResponse {
  message: string;
  electivas: Electiva[];
  total: number;
}