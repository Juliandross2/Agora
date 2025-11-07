
export interface Programa {
    programa_id: number;    
    nombre_programa: string;
    es_activo: boolean;
    pensum_activo_id?: number | null;
}

export interface apiProgramaResponse {
    message: string;
    programas: Programa[];
    total: number;
}