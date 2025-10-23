
export interface Programa {
    programa_id: number;    
    nombre_programa: string;
    es_activo: boolean;
}

export interface apiProgramaResponse {
    message: string;
    programas: Programa[];
    total: number;
}