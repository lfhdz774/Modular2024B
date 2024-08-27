import React from 'react';
import { Container, Grid, Paper, Typography, Card, CardContent, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Box, useTheme } from '@mui/material';
import { BarChart } from '@mui/x-charts';

const HomePage = () => {
  const theme = useTheme();

  const chartData = [
    { server: 'Servidor 1', activeCredentials: 12 },
    { server: 'Servidor 2', activeCredentials: 19 },
    { server: 'Servidor 3', activeCredentials: 3 },
  ];

  const credentials = [
    { id: 1, server: 'Servidor 1', username: 'usuario1', expireDate: '2023-12-31' },
    { id: 2, server: 'Servidor 2', username: 'usuario2', expireDate: '2024-01-15' },
    { id: 3, server: 'Servidor 3', username: 'usuario3', expireDate: '2024-02-20' },
  ];

  const today = new Date();
  const expiringSoon = credentials.filter(credential => {
    const expireDate = new Date(credential.expireDate);
    const timeDiff = expireDate - today;
    const daysDiff = timeDiff / (1000 * 3600 * 24);
    return daysDiff <= 30; // Expiring within the next 30 days
  });

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Widgets
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Maneja tus credenciales de forma segura.
      </Typography>
      <Grid container spacing={3}>
        {/* Chart */}
        <Grid item xs={12} md={8} lg={9}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 260 }}>
            <Typography variant="h6" gutterBottom>
              Credenciales activas por servidor
            </Typography>
            <BarChart
              xAxis={[{ dataKey: 'server', label: 'Servidor', scaleType: 'band' }]}
              series={[{ dataKey: 'activeCredentials', label: 'Credenciales Activas' }]}
              dataset={chartData}
              height={200}
            />
          </Paper>
        </Grid>
        {/* Credentials Expiring Soon */}
        <Grid item xs={12} md={4} lg={3}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 260 , backgroundColor: theme.palette.background.paper }}>
            <Typography variant="h6" gutterBottom>
              Credenciales por expirar
            </Typography>
            {expiringSoon.length > 0 ? (
              expiringSoon.map(credential => (
                <Box key={credential.id} sx={{ p: 1, mb: 1, border: `1px solid ${theme.palette.divider}`, borderRadius: '4px', backgroundColor: theme.palette.background.default }}>
                  <Typography variant="body2" color={theme.palette.text.primary}>
                    <strong>{credential.username}</strong> en <strong>{credential.server}</strong>
                  </Typography>
                  <Typography variant="body2" color={theme.palette.text.secondary}>
                    Expira el {credential.expireDate}
                  </Typography>
                </Box>
              ))
            ) : (
              <Typography variant="body2" color={theme.palette.text.secondary}>No hay credenciales por expirar pronto.</Typography>
            )}
          </Paper>
        </Grid>
        {/* Create Credential */}
        <Grid item xs={12} md={4}>
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
        </Grid>
        {/* Remove Credential */}
        <Grid item xs={12} md={4}>
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
        </Grid>
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
                    <TableCell>Fecha de Expiración</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {credentials.map((credential) => (
                    <TableRow key={credential.id}>
                      <TableCell>{credential.server}</TableCell>
                      <TableCell>{credential.username}</TableCell>
                      <TableCell>{credential.expireDate}</TableCell>
                    </TableRow>
                  ))}
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