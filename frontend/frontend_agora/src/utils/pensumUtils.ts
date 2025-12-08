import type { MateriaPorSemestre } from '../services/domain/PensumModels';
import { normalizeText } from './textUtils';

export interface PensumMateriaResumen {
  materiaId: number;
  nombre: string;
  semestre: number;
  nombreNormalizado: string;
  esElectiva?: boolean;
  creditos?: number;
  orden: number;
}

export const buildPensumMateriasResumen = (
  materiasPorSemestre: MateriaPorSemestre[]
): PensumMateriaResumen[] => {
  const resumen: PensumMateriaResumen[] = [];

  const gruposOrdenados = [...materiasPorSemestre].sort((a, b) => a.semestre - b.semestre);

  gruposOrdenados.forEach((grupo) => {
    grupo.materias.forEach((materia) => {
      resumen.push({
        materiaId: materia.materia_id,
        nombre: materia.nombre_materia,
        semestre: materia.semestre,
        nombreNormalizado: normalizeText(materia.nombre_materia),
        esElectiva: materia.es_electiva,
        creditos: materia.creditos,
        orden: resumen.length,
      });
    });
  });

  return resumen;
};
