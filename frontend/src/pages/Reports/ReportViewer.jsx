import React, { useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { TextField, Button, MenuItem, Select, InputLabel, FormControl, Grid, Box } from '@mui/material';
import { postReportGenerator } from 'src/Services/Report.Service';
import ExportToExcel from 'src/components/ExportToExcel ';
import { replace } from 'lodash';

// Lista simulada de reportes con sus filtros.
const reportes = [
  {
    id: 1,
    nombre: 'Reporte de Accesos',
    filtros: [
      { nombre: 'Fecha Inicio', tipo: 'date', clave: 'fechaInicio' },
      { nombre: 'Fecha Fin', tipo: 'date', clave: 'fechaFin' }
    ],
  },

];

const ReportViewer = () => {
  const [reporteSeleccionado, setReporteSeleccionado] = useState(null);
  const [filtros, setFiltros] = useState({});
  const [data, setData] = useState([]);
  const [columns, setColumns] = useState([]);

  const handleReporteChange = (event) => {
    const reporte = reportes.find((r) => r.id === parseInt(event.target.value));
    setReporteSeleccionado(reporte);
    setFiltros({});
  };

  const handleFiltroChange = (clave, valor) => {
    setFiltros((prev) => ({ ...prev, [clave]: valor }));
  };

  const getCurrentDate = () => {
    const date = new Date();
    return `${date.toLocaleDateString()}}`;
  };

  const fetchData = async () => {
    try {
      const response = await postReportGenerator({
        idReporte: reporteSeleccionado.id,
        filtros,
      });

      const reportData = response.data;
      console.log('reportData:', reportData);
      if (reportData.length > 0) {
        // Genera columnas dinámicamente a partir de las claves del primer objeto.
        const generatedColumns = Object.keys(reportData[0]).map((key) => ({
          field: key,
          headerName: key.charAt(0).toUpperCase() + key.slice(1),
          width: 150,
        }));
        setColumns(generatedColumns);
      } else {
        setColumns([]);
      }

      setData(reportData);
    } catch (error) {
      console.error('Error al obtener los datos del reporte:', error);
    }
  };

  return (
    <Box padding={3}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Seleccionar Reporte</InputLabel>
            <Select value={reporteSeleccionado?.id || ''} onChange={handleReporteChange}>
              {reportes.map((reporte) => (
                <MenuItem key={reporte.id} value={reporte.id}>
                  {reporte.nombre}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={3}>
          <Box display="flex" flexDirection="column" gap={2}>
            {reporteSeleccionado &&
              reporteSeleccionado.filtros.map((filtro) => (
                <TextField
                  key={filtro.clave}
                  label={filtro.nombre}
                  type={filtro.tipo}
                  InputLabelProps={{ shrink: true }}
                  onChange={(e) => handleFiltroChange(filtro.clave, e.target.value)}
                />
              ))}
            <Button variant="contained" color="primary" onClick={fetchData}>
              Generar Reporte
            </Button>
          </Box>
        </Grid>

        <Grid item xs={9}>
          <div style={{ height: 400 }}>
            <DataGrid rows={data} columns={columns} pageSize={5} />
          </div>
          {/* Agregar el botón para exportar a Excel */}
          {data.length > 0 && (
            <ExportToExcel reportData={data} fileName={replace(reporteSeleccionado.nombre, " ","_") + getCurrentDate()} />
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default ReportViewer;
