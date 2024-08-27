import React, { useState } from 'react';
import { Container, Paper, Typography, TextField, Button, Grid, MenuItem, Select, FormControl, InputLabel, Checkbox, FormControlLabel, Backdrop, Box, Modal, Fade } from '@mui/material';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import 'dayjs/locale/es-mx'; // Import the Mexican Spanish locale for Day.js
import {PostCredential} from 'src/Services/credential.service'; // Reemplaza con la ruta actual al servicio

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const CredentialCreation = () => {
  const [user, setUser] = useState({
    username: '',
    password: '',
    email: '',
    first_name: '',
    last_name: '',
    employee_code: '',
    role_id: '',
    server: '',
    group: '',
    expireDate: null,
  });
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [loading, setLoading] = useState(false); // State for loading modal
  const [securityCheck, setSecurityCheck] = useState(false); // State for security check modal
  const [randomNumbers, setRandomNumbers] = useState({ num1: 0, num2: 0 }); // State for random numbers
  const [securityInput, setSecurityInput] = useState(''); // State for security input

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUser((prevUser) => ({
      ...prevUser,
      [name]: value,
    }));
  };

  const handleCheckboxChange = (event) => {
    setShowDatePicker(event.target.checked);
  };

  const generateRandomNumbers = () => {
    const num1 = Math.floor(Math.random() * 100);
    const num2 = Math.floor(Math.random() * 100);
    setRandomNumbers({ num1, num2 });
  };

  const handleSecuritySubmit = () => {
    setSecurityCheck(false);
    setLoading(true); // Show loading modal

    // const data = {
    //   ...user,
    //   expireDate: user.expireDate ? user.expireDate.toISOString() : null,
    // };

    const data ={
        username: user.username,
        password: user.password
    }

    setTimeout(async () => {
      try {
        const response = await PostCredential(data);
        setLoading(false); // Hide loading modal
        // Handle successful response
        console.log('Credential created successfully', response);
      } catch (error) {
        setLoading(false); // Hide loading modal
        // Handle error response
        console.error('Error creating credential', error);
      }
    }, 2000);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    generateRandomNumbers();
    setSecurityCheck(true); // Show security check modal
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Crear Credencial
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Nombre de Usuario"
                variant="outlined"
                required
                name="username"
                value={user.username}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Contraseña"
                type="password"
                variant="outlined"
                required
                name="password"
                value={user.password}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth variant="outlined" required>
                <InputLabel id="server-label">Servidor</InputLabel>
                <Select
                  labelId="server-label"
                  name="server"
                  value={user.server}
                  onChange={handleChange}
                  label="Servidor"
                >
                  <MenuItem value=""><em>None</em></MenuItem>
                  <MenuItem value="server1">Servidor 1</MenuItem>
                  <MenuItem value="server2">Servidor 2</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth variant="outlined" required>
                <InputLabel id="group-label">Grupo</InputLabel>
                <Select
                  labelId="group-label"
                  name="group"
                  value={user.group}
                  onChange={handleChange}
                  label="Grupo"
                >
                  <MenuItem value=""><em>None</em></MenuItem>
                  <MenuItem value="group1">Grupo 1</MenuItem>
                  <MenuItem value="group2">Grupo 2</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={showDatePicker}
                    onChange={handleCheckboxChange}
                    color="primary"
                  />
                }
                label="Mostrar Fecha de Expiración"
              />
            </Grid>
            {showDatePicker && (
              <Grid item xs={12}>
                <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="es-mx">
                  <DatePicker
                    label="Fecha de Expiración"
                    value={user.expireDate}
                    onChange={(newValue) => setUser((prevUser) => ({
                      ...prevUser,
                      expireDate: newValue,
                    }))}
                    renderInput={(params) => <TextField {...params} fullWidth variant="outlined" required />}
                  />
                </LocalizationProvider>
              </Grid>
            )}
            <Grid item xs={12}>
              <Button variant="contained" color="primary" type="submit">
                Crear
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>

      <Modal
        aria-labelledby="transition-modal-title"
        aria-describedby="transition-modal-description"
        open={loading}
        onClose={() => setLoading(false)}
        closeAfterTransition
        slots={{ backdrop: Backdrop }}
        slotProps={{
          backdrop: {
            timeout: 500,
          },
        }}
      >
        <Fade in={loading}>
          <Box sx={style}>
            <Typography id="transition-modal-title" variant="h6" component="h2">
              Creando Credencial
            </Typography>
            <Typography id="transition-modal-description" sx={{ mt: 2 }}>
              Por favor, espere mientras se crea la credencial.
            </Typography>
          </Box>
        </Fade>
      </Modal>

      <Modal
        aria-labelledby="security-modal-title"
        aria-describedby="security-modal-description"
        open={securityCheck}
        onClose={() => setSecurityCheck(false)}
        closeAfterTransition
        slots={{ backdrop: Backdrop }}
        slotProps={{
          backdrop: {
            timeout: 500,
          },
        }}
      >
        <Fade in={securityCheck}>
          <Box sx={style}>
            <Typography id="security-modal-title" variant="h6" component="h2">
              Verificación de Seguridad
            </Typography>
            <Typography id="security-modal-description" sx={{ mt: 2 }}>
              Ingrese el resultado de su algoritmo con los siguientes números:
            </Typography>
            <Typography sx={{ mt: 2 }}>
              Número 1: {randomNumbers.num1}
            </Typography>
            <Typography sx={{ mt: 2 }}>
              Número 2: {randomNumbers.num2}
            </Typography>
            <TextField
              fullWidth
              label="Resultado del Algoritmo"
              variant="outlined"
              value={securityInput}
              onChange={(e) => setSecurityInput(e.target.value)}
              sx={{ mt: 2 }}
            />
            <Button variant="contained" color="primary" onClick={handleSecuritySubmit} sx={{ mt: 2 }}>
              Verificar
            </Button>
          </Box>
        </Fade>
      </Modal>
    </Container>
  );
};

export default CredentialCreation;