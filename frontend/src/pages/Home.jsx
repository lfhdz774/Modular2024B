import React, { useEffect, useState } from 'react';
import { Container, Grid, Paper, Typography, Card, CardContent, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Box, useTheme } from '@mui/material';
import { BarChart } from '@mui/x-charts';
import { recentAccessReport } from 'src/Services/Report.Service';
import {GetChartReport} from 'src/Services/Report.Service';
const HomePage = () => {
  const theme = useTheme();
  const [servers, setServers] = React.useState([]);
  const [credentials, setCredentials] = React.useState([]);

  const [chartData, setChartData] = useState([
    { server_name: 'Servidor 1', credentials_count: 12 },
    { server_name: 'Servidor 2', credentials_count: 19 },
    { server_name: 'Servidor 3', credentials_count: 3 },
  ]);


  const getChartData = async() => {
    const chartDataResponse = await GetChartReport();
    setChartData([]);
    setChartData(chartDataResponse);

    const recentAccessReportResponse = await recentAccessReport();
    if (recentAccessReportResponse.status === 200)
      setCredentials(recentAccessReportResponse.data);
    else
      setCredentials([]);
    console.log(recentAccessReportResponse);
  }

  useEffect(() => {
    getChartData();
  }, []);

  


  // const credentials = [
  //   { id: 1, server: 'Servidor 1', username: 'usuario1', expireDate: '2023-12-31' },
  //   { id: 2, server: 'Servidor 2', username: 'usuario2', expireDate: '2024-01-15' },
  //   { id: 3, server: 'Servidor 3', username: 'usuario3', expireDate: '2024-02-20' },
  // ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        ServerPortal-APP CUCEI 2024B
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Maneja tus Servidores y Acceso de forma sencilla.
      </Typography>
      <Grid container spacing={3}>
      
      <Grid item xs={12} md={8} lg={9}>
      <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 260 }}>
        <Typography variant="h6" gutterBottom>
          Credenciales activas por servidor
        </Typography>
        <BarChart
          xAxis={[{ dataKey: 'server_name', label: 'Servidor', scaleType: 'band' }]}
          series={[{ dataKey: 'credentials_count', label: 'Credenciales Activas' }]}
          dataset={chartData}
          height={200}
        />
      </Paper>
    </Grid> 
        
        {/* Create Credential */}
        {/* <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Crear Credencial
              </Typography>
              <Button variant="contained" color="primary">
                Crear
              </Button>
            </CardContent>
          </Card>
        </Grid> */}
        {/* Remove Credential */}
        {/* <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Eliminar Credencial
              </Typography>
              <Button variant="contained" color="secondary">
                Eliminar
              </Button>
            </CardContent>
          </Card>
        </Grid> */}
        {/* Recent Orders */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" gutterBottom>
              Credeciales Recientes
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Servidor</TableCell>
                    <TableCell>Nombre de Usuario</TableCell>
                    <TableCell>Fecha de creación</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  { credentials ? credentials.map((credential) => (
                    <TableRow key={credential.id}>
                      <TableCell>{credential.server}</TableCell>
                      <TableCell>{credential.username}</TableCell>
                      <TableCell>{credential.createdAt}</TableCell>
                    </TableRow>
                  )) : null}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default HomePage;