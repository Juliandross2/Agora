import React from 'react';

interface Materia {
  materia_id: number;
  nombre_materia: string;
  creditos: number;
  es_electiva: boolean;
}

interface CardSemestreMateriasProps {
  semestre: number;
  materias: Materia[];
  creditosTotales: number;
}

const CardSemestreMaterias: React.FC<CardSemestreMateriasProps> = ({
  semestre,
  materias,
  creditosTotales
}) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
      <div className="bg-blue-900 text-white px-4 py-3">
        <h3 className="font-semibold text-center">Semestre {semestre}</h3>
        <div className="text-xs text-blue-200 text-center">
          {creditosTotales > 0 ? `${creditosTotales} créditos` : '0 créditos'}
        </div>
      </div>
      <div className="p-4 space-y-3">
        {materias.length === 0 ? (
          <div className="text-center text-gray-400 py-4">
            <div className="text-sm">Sin materias</div>
          </div>
        ) : (
          materias.map((materia) => (
            <div
              key={materia.materia_id}
              className={`border rounded p-3 ${
                materia.es_electiva
                  ? 'bg-orange-50 border-orange-200'
                  : 'bg-green-50 border-green-200'
              }`}
            >
              <div className={`font-medium text-sm ${
                materia.es_electiva ? 'text-orange-800' : 'text-green-800'
              }`}>
                {materia.nombre_materia}
              </div>
              <div className={`text-xs ${
                materia.es_electiva ? 'text-orange-600' : 'text-green-600'
              }`}>
                {materia.creditos} Creditos
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default CardSemestreMaterias;