import * as XLSX from 'xlsx';

interface EstudianteResumen {
  id: string;
  nombre: string;
  programa: string;
  estado: 'APTO' | 'NO_APTO';
  porcentaje?: number;
  iniciales?: string;
}

interface Materia {
  id: string;
  nombre: string;
  estado: 'APROBADA' | 'NO_APROBADA' | 'NO_CURSADA';
  nota?: number;
}

interface EstudianteDetalle {
  id: string;
  nombre: string;
  programa: string;
  estado: 'APTO' | 'NO_APTO';
  materias: Materia[];
}

// Exportar resumen general a PDF (vía impresión)
export const exportResumenToPDF = (estudiantes: EstudianteResumen[]): void => {
  const totalEstudiantes = estudiantes.length;
  const aptos = estudiantes.filter(e => e.estado === 'APTO').length;
  const noAptos = estudiantes.filter(e => e.estado === 'NO_APTO').length;
  const porcentajeAptos = totalEstudiantes > 0 ? ((aptos / totalEstudiantes) * 100).toFixed(1) : '0';

  const htmlContent = `
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Reporte General - Sistema AGORA</title>
      <style>
        @media print {
          @page { margin: 1cm; size: A4; }
          body { margin: 0; }
        }
        
        body {
          font-family: Arial, sans-serif;
          line-height: 1.4;
          color: #333;
          max-width: 210mm;
          margin: 0 auto;
          padding: 20px;
        }
        
        .header {
          background: #1e3a8a;
          color: white;
          text-align: center;
          padding: 20px;
          margin: -20px -20px 20px -20px;
        }
        
        .header h1 {
          margin: 0 0 5px 0;
          font-size: 18px;
        }
        
        .header h2 {
          margin: 0;
          font-size: 16px;
          font-weight: normal;
        }
        
        .stats-section {
          background: #f3f4f6;
          padding: 15px;
          border-radius: 8px;
          margin-bottom: 25px;
        }
        
        .stats-section h3 {
          color: #1e3a8a;
          margin-top: 0;
          margin-bottom: 15px;
        }
        
        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 10px;
        }
        
        .stat-item {
          padding: 8px;
          background: white;
          border-radius: 4px;
          border-left: 4px solid #1e3a8a;
        }
        
        .table-container {
          margin-top: 20px;
          overflow-x: auto;
        }
        
        table {
          width: 100%;
          border-collapse: collapse;
          font-size: 12px;
        }
        
        th {
          background: #1e3a8a;
          color: white;
          padding: 12px 8px;
          text-align: left;
          font-weight: bold;
        }
        
        td {
          padding: 10px 8px;
          border-bottom: 1px solid #e5e7eb;
        }
        
        tr:nth-child(even) {
          background-color: #f9fafb;
        }
        
        .status-apto {
          color: #16a34a;
          font-weight: bold;
        }
        
        .status-no-apto {
          color: #dc2626;
          font-weight: bold;
        }
        
        .footer {
          margin-top: 30px;
          padding-top: 15px;
          border-top: 2px solid #1e3a8a;
          font-size: 11px;
          color: #6b7280;
          text-align: center;
        }
        
        .no-print {
          display: block;
        }
        
        @media print {
          .no-print {
            display: none !important;
          }
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Sistema AGORA - Universidad del Cauca</h1>
        <h2>Reporte General de Comparación de Pensum</h2>
      </div>
      
      <div class="stats-section">
        <h3>Resumen General</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <strong>Total de estudiantes:</strong> ${totalEstudiantes}
          </div>
          <div class="stat-item">
            <strong>Estudiantes aptos:</strong> ${aptos} (${porcentajeAptos}%)
          </div>
          <div class="stat-item">
            <strong>Estudiantes no aptos:</strong> ${noAptos} (${(100 - parseFloat(porcentajeAptos)).toFixed(1)}%)
          </div>
        </div>
      </div>
      
      <div class="table-container">
        <h3 style="color: #1e3a8a; margin-bottom: 15px;">Detalle por Estudiante</h3>
        <table>
          <thead>
            <tr>
              <th>ID Estudiante</th>
              <th>Nombre Completo</th>
              <th>Programa</th>
              <th>Estado</th>
              <th>% Completado</th>
            </tr>
          </thead>
          <tbody>
            ${estudiantes.map(estudiante => `
              <tr>
                <td>${estudiante.id}</td>
                <td>${estudiante.nombre}</td>
                <td>${estudiante.programa}</td>
                <td class="${estudiante.estado === 'APTO' ? 'status-apto' : 'status-no-apto'}">
                  ${estudiante.estado}
                </td>
                <td>${estudiante.porcentaje || 'N/A'}%</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      
      <div class="footer">
        <p>Generado el ${new Date().toLocaleDateString('es-CO', { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })}</p>
      </div>
      
      <div class="no-print" style="position: fixed; top: 10px; right: 10px; z-index: 1000;">
        <button onclick="window.print()" style="
          background: #1e3a8a; 
          color: white; 
          border: none; 
          padding: 10px 20px; 
          border-radius: 5px; 
          cursor: pointer;
          font-size: 14px;
        ">
          Guardar como PDF
        </button>
        <button onclick="window.close()" style="
          background: #6b7280; 
          color: white; 
          border: none; 
          padding: 10px 20px; 
          border-radius: 5px; 
          cursor: pointer;
          font-size: 14px;
          margin-left: 10px;
        ">
          Cerrar
        </button>
      </div>
      
      <script>
        // Auto-abrir el diálogo de impresión
        window.addEventListener('load', function() {
          setTimeout(() => {
            window.print();
          }, 500);
        });
      </script>
    </body>
    </html>
  `;

  // Abrir en nueva ventana
  const printWindow = window.open('', '_blank');
  if (printWindow) {
    printWindow.document.write(htmlContent);
    printWindow.document.close();
  }
};

// Exportar detalle de estudiante a PDF (vía impresión)
export const exportDetalleToPDF = (estudiante: EstudianteDetalle): void => {
  const materiasAprobadas = estudiante.materias.filter(m => m.estado === 'APROBADA').length;
  const materiasNoAprobadas = estudiante.materias.filter(m => m.estado === 'NO_APROBADA').length;
  const materiasNoCursadas = estudiante.materias.filter(m => m.estado === 'NO_CURSADA').length;

  const htmlContent = `
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Reporte Detallado - ${estudiante.nombre}</title>
      <style>
        @media print {
          @page { margin: 1cm; size: A4; }
          body { margin: 0; }
        }
        
        body {
          font-family: Arial, sans-serif;
          line-height: 1.4;
          color: #333;
          max-width: 210mm;
          margin: 0 auto;
          padding: 20px;
        }
        
        .header {
          background: #1e3a8a;
          color: white;
          text-align: center;
          padding: 20px;
          margin: -20px -20px 10px -20px;
        }
        
        .sub-header {
          background: #60a5fa;
          color: white;
          text-align: center;
          padding: 15px;
          margin: 0 -20px 20px -20px;
        }
        
        .header h1 {
          margin: 0 0 5px 0;
          font-size: 18px;
        }
        
        .sub-header h2 {
          margin: 0 0 5px 0;
          font-size: 16px;
        }
        
        .sub-header h3 {
          margin: 0;
          font-size: 14px;
          font-weight: normal;
        }
        
        .student-info {
          background: #f3f4f6;
          padding: 15px;
          border-radius: 8px;
          margin-bottom: 20px;
        }
        
        .legend {
          background: white;
          border: 1px solid #e5e7eb;
          padding: 15px;
          border-radius: 8px;
          margin-bottom: 20px;
          text-align: center;
        }
        
        .legend-item {
          display: inline-flex;
          align-items: center;
          margin: 0 15px;
          font-size: 14px;
        }
        
        .legend-dot {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          margin-right: 8px;
        }
        
        .dot-green { background: #16a34a; }
        .dot-red { background: #dc2626; }
        .dot-gray { background: #6b7280; }
        
        .materias-section {
          background: white;
          border: 1px solid #e5e7eb;
          padding: 20px;
          border-radius: 8px;
          margin-bottom: 20px;
        }
        
        .materias-section h3 {
          color: #1e3a8a;
          margin-top: 0;
          margin-bottom: 15px;
        }
        
        .materia-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px;
          margin-bottom: 8px;
          border-radius: 6px;
          border: 1px solid #e5e7eb;
        }
        
        .materia-aprobada {
          background: #f0fdf4;
          border-color: #bbf7d0;
        }
        
        .materia-no-aprobada {
          background: #fef2f2;
          border-color: #fecaca;
        }
        
        .materia-no-cursada {
          background: #f9fafb;
          border-color: #e5e7eb;
        }
        
        .materia-left {
          display: flex;
          align-items: center;
        }
        
        .materia-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          margin-right: 12px;
        }
        
        .materia-right {
          font-weight: bold;
          font-size: 14px;
        }
        
        .nota-aprobada { color: #16a34a; }
        .nota-no-aprobada { color: #dc2626; }
        .nota-no-cursada { color: #6b7280; }
        
        .resumen {
          background: #f3f4f6;
          padding: 15px;
          border-radius: 8px;
          margin-bottom: 20px;
        }
        
        .resumen h3 {
          color: #1e3a8a;
          margin-top: 0;
          margin-bottom: 10px;
        }
        
        .resumen-item {
          margin-bottom: 5px;
          font-size: 14px;
        }
        
        .resultado {
          text-align: center;
          padding: 20px;
          border-radius: 8px;
          margin-bottom: 20px;
          color: white;
          font-weight: bold;
        }
        
        .resultado-apto {
          background: #16a34a;
        }
        
        .resultado-no-apto {
          background: #dc2626;
        }
        
        .footer {
          margin-top: 30px;
          padding-top: 15px;
          border-top: 2px solid #1e3a8a;
          font-size: 11px;
          color: #6b7280;
          text-align: center;
        }
        
        .no-print {
          display: block;
        }
        
        @media print {
          .no-print {
            display: none !important;
          }
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Sistema AGORA - Universidad del Cauca</h1>
      </div>
      
      <div class="sub-header">
        <h2>Comparación Pensum</h2>
        <h3>${estudiante.nombre}</h3>
      </div>
      
      <div class="student-info">
        <div><strong>Estudiante:</strong> ${estudiante.nombre} - <strong>ID:</strong> ${estudiante.id}</div>
        <div><strong>Programa:</strong> ${estudiante.programa}</div>
      </div>
      
      <div class="legend">
        <div class="legend-item">
          <div class="legend-dot dot-green"></div>
          Aprobada
        </div>
        <div class="legend-item">
          <div class="legend-dot dot-red"></div>
          No aprobada
        </div>
        <div class="legend-item">
          <div class="legend-dot dot-gray"></div>
          No cursada
        </div>
      </div>
      
      <div class="materias-section">
        <h3>Materias Obligatorias:</h3>
        ${estudiante.materias.map(materia => `
          <div class="materia-item ${
            materia.estado === 'APROBADA' ? 'materia-aprobada' :
            materia.estado === 'NO_APROBADA' ? 'materia-no-aprobada' : 'materia-no-cursada'
          }">
            <div class="materia-left">
              <div class="materia-dot ${
                materia.estado === 'APROBADA' ? 'dot-green' :
                materia.estado === 'NO_APROBADA' ? 'dot-red' : 'dot-gray'
              }"></div>
              <span>${materia.nombre}</span>
            </div>
            <div class="materia-right ${
              materia.estado === 'APROBADA' ? 'nota-aprobada' :
              materia.estado === 'NO_APROBADA' ? 'nota-no-aprobada' : 'nota-no-cursada'
            }">
              ${materia.estado === 'NO_CURSADA' ? 'No cursada' :
                materia.estado === 'APROBADA' ? `✓ ${materia.nota}` : `✗ ${materia.nota}`}
            </div>
          </div>
        `).join('')}
      </div>
      
      <div class="resumen">
        <h3>Resumen:</h3>
        <div class="resumen-item" style="color: #16a34a;">
          ✓ Aprobadas: ${materiasAprobadas} materias
        </div>
        <div class="resumen-item" style="color: #dc2626;">
          ✗ No aprobadas: ${materiasNoAprobadas} materias
        </div>
        <div class="resumen-item" style="color: #6b7280;">
          ○ No cursadas: ${materiasNoCursadas} materia${materiasNoCursadas !== 1 ? 's' : ''}
        </div>
      </div>
      
      <div class="resultado ${estudiante.estado === 'APTO' ? 'resultado-apto' : 'resultado-no-apto'}">
        <div style="font-size: 14px; margin-bottom: 5px;">RESULTADO:</div>
        <div style="font-size: 18px;">
          El estudiante ${estudiante.estado === 'APTO' ? 'SÍ es apto' : 'NO es apto'}
        </div>
      </div>
      
      <div class="footer">
        <p>Generado el ${new Date().toLocaleDateString('es-CO', { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })}</p>
      </div>
      
      <div class="no-print" style="position: fixed; top: 10px; right: 10px; z-index: 1000;">
        <button onclick="window.print()" style="
          background: #1e3a8a; 
          color: white; 
          border: none; 
          padding: 10px 20px; 
          border-radius: 5px; 
          cursor: pointer;
          font-size: 14px;
        ">
          Guardar como PDF
        </button>
        <button onclick="window.close()" style="
          background: #6b7280; 
          color: white; 
          border: none; 
          padding: 10px 20px; 
          border-radius: 5px; 
          cursor: pointer;
          font-size: 14px;
          margin-left: 10px;
        ">
          Cerrar
        </button>
      </div>
      
      <script>
        window.addEventListener('load', function() {
          setTimeout(() => {
            window.print();
          }, 500);
        });
      </script>
    </body>
    </html>
  `;

  const printWindow = window.open('', '_blank');
  if (printWindow) {
    printWindow.document.write(htmlContent);
    printWindow.document.close();
  }
};

// Exportar resumen a Excel
export const exportResumenToExcel = (estudiantes: EstudianteResumen[]): void => {
  const totalEstudiantes = estudiantes.length;
  const aptos = estudiantes.filter(e => e.estado === 'APTO').length;
  const noAptos = estudiantes.filter(e => e.estado === 'NO_APTO').length;
  const porcentajeAptos = totalEstudiantes > 0 ? ((aptos / totalEstudiantes) * 100).toFixed(1) : '0';

  // Crear workbook
  const wb = XLSX.utils.book_new();

  // Hoja de resumen estadístico
  const resumenData = [
    ['REPORTE GENERAL DE COMPARACIÓN DE PENSUM'],
    ['Sistema AGORA - Universidad del Cauca'],
    [''],
    ['RESUMEN ESTADÍSTICO'],
    ['Total de estudiantes', totalEstudiantes],
    ['Estudiantes aptos', `${aptos} (${porcentajeAptos}%)`],
    ['Estudiantes no aptos', `${noAptos} (${(100 - parseFloat(porcentajeAptos)).toFixed(1)}%)`],
    [''],
    ['Fecha de generación', new Date().toLocaleDateString('es-CO')],
  ];

  const wsResumen = XLSX.utils.aoa_to_sheet(resumenData);
  
  // Aplicar estilos básicos (anchos de columna)
  wsResumen['!cols'] = [
    { width: 25 },
    { width: 20 }
  ];

  XLSX.utils.book_append_sheet(wb, wsResumen, 'Resumen');

  // Hoja de detalle de estudiantes
  const estudiantesData = [
    ['DETALLE DE ESTUDIANTES'],
    [''],
    ['ID', 'Nombre Completo', 'Programa', 'Estado', '% Completado'],
    ...estudiantes.map(est => [
      est.id,
      est.nombre,
      est.programa,
      est.estado,
      est.porcentaje ? `${est.porcentaje}%` : 'N/A'
    ])
  ];

  const wsEstudiantes = XLSX.utils.aoa_to_sheet(estudiantesData);
  
  wsEstudiantes['!cols'] = [
    { width: 12 },
    { width: 25 },
    { width: 25 },
    { width: 12 },
    { width: 12 }
  ];

  XLSX.utils.book_append_sheet(wb, wsEstudiantes, 'Estudiantes');

  // Guardar archivo
  const filename = `reporte_general_${new Date().toISOString().split('T')[0]}.xlsx`;
  XLSX.writeFile(wb, filename);
};

// Exportar detalle de estudiante a Excel
export const exportDetalleToExcel = (estudiante: EstudianteDetalle): void => {
  const materiasAprobadas = estudiante.materias.filter(m => m.estado === 'APROBADA').length;
  const materiasNoAprobadas = estudiante.materias.filter(m => m.estado === 'NO_APROBADA').length;
  const materiasNoCursadas = estudiante.materias.filter(m => m.estado === 'NO_CURSADA').length;

  const wb = XLSX.utils.book_new();

  // Información del estudiante y resumen
  const infoData = [
    ['REPORTE DETALLADO DE ESTUDIANTE'],
    ['Sistema AGORA - Universidad del Cauca'],
    [''],
    ['INFORMACIÓN DEL ESTUDIANTE'],
    ['Nombre', estudiante.nombre],
    ['ID', estudiante.id],
    ['Programa', estudiante.programa],
    ['Estado Final', estudiante.estado],
    [''],
    ['RESUMEN DE MATERIAS'],
    ['Materias aprobadas', materiasAprobadas],
    ['Materias no aprobadas', materiasNoAprobadas],
    ['Materias no cursadas', materiasNoCursadas],
    ['Total de materias', estudiante.materias.length],
    [''],
    ['Fecha de generación', new Date().toLocaleDateString('es-CO')],
  ];

  const wsInfo = XLSX.utils.aoa_to_sheet(infoData);
  wsInfo['!cols'] = [{ width: 25 }, { width: 30 }];
  XLSX.utils.book_append_sheet(wb, wsInfo, 'Información');

  // Hoja de materias detalladas
  const materiasData = [
    ['DETALLE DE MATERIAS'],
    [''],
    ['Materia', 'Estado', 'Nota', 'Observaciones'],
    ...estudiante.materias.map(materia => [
      materia.nombre,
      materia.estado === 'APROBADA' ? 'Aprobada' :
      materia.estado === 'NO_APROBADA' ? 'No Aprobada' : 'No Cursada',
      materia.nota || 'N/A',
      materia.estado === 'NO_CURSADA' ? 'Materia pendiente por cursar' :
      materia.estado === 'NO_APROBADA' ? 'Requiere repetir la materia' : 'Materia completada exitosamente'
    ])
  ];

  const wsMaterias = XLSX.utils.aoa_to_sheet(materiasData);
  wsMaterias['!cols'] = [
    { width: 30 },
    { width: 15 },
    { width: 8 },
    { width: 35 }
  ];

  XLSX.utils.book_append_sheet(wb, wsMaterias, 'Materias');

  // Guardar archivo
  const filename = `reporte_${estudiante.nombre.replace(/\s+/g, '_')}_${estudiante.id}.xlsx`;
  XLSX.writeFile(wb, filename);
};