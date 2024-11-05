import React from 'react';
import * as XLSX from 'xlsx';
import { Button } from '@mui/material';

const ExportToExcel = ({ reportData, fileName }) => {
    const handleExport = () => {
        // Convertir los datos a una hoja de trabajo (worksheet)
        const worksheet = XLSX.utils.json_to_sheet(reportData);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Reporte');

        // Generar el archivo Excel
        XLSX.writeFile(workbook, `${fileName}.xlsx`);
    };

    return (
        <Button variant="contained" color="primary" onClick={handleExport}>
            Exportar a Excel
        </Button>
    );
};

export default ExportToExcel;
