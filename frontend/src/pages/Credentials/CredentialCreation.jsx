import React, { useEffect, useState, useCallback} from 'react';
import { Container, Paper, Typography, TextField, Button, Grid, MenuItem, Select, FormControl, InputLabel, Checkbox, FormControlLabel, Backdrop, Box, Modal, Fade, FormLabel } from '@mui/material';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import 'dayjs/locale/es-mx'; // Import the Mexican Spanish locale for Day.js
import {PostCredential, AccessRequest} from 'src/Services/credential.service'; // Reemplaza con la ruta actual al servicio
import { GetServers } from 'src/Services/servers.service';
import { GetUserByCode, GetUsersByRole } from 'src/Services/user.service';
import _ from 'lodash';

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
  const [codigo, setCodigo] = useState('');
  const [user, setUser] = useState({
    server_id: -1,
    group_id: -1,
    user_id: 0,
    expireDate: null,
    aprover_id: -1,
    username: '',
  });
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [loading, setLoading] = useState(false); // State for loading modal
  const [servers, setServers] = useState([]); // State for servers
  
  const [usuario, setUsuario] = useState('');
  const [aprover, setAprover] = useState([]);


  useEffect(() => {
    GetServersList();
    GetAprovers();
  }, []);

  const GetServersList = async() => {
    try {
      const ServerResponse = await GetServers();
      setServers(ServerResponse);
    } catch (error) {
      console.error('Error getting servers', error);
    }
  };


  const GetAprovers = async() => {
    try {
      const AproverResponse = await GetUsersByRole(3);
      setAprover(AproverResponse.data);
      console.log(AproverResponse);
    } catch (error) {
      console.error('Error getting aprovers', error);
    }
  };

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

  const handleSecuritySubmit = () => {
      setLoading(true); // Show loading modal

    // const data = {
    //   ...user,
    //   expireDate: user.expireDate ? user.expireDate.toISOString() : null,
    // };

    setTimeout(async () => {
      try {
        const response = await AccessRequest(user);
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
    handleSecuritySubmit();
  };

  
    // Función que realiza la búsqueda del usuario en la API
    const searchUser = async (code) => {
      try {
        const response = await GetUserByCode(code);
        if (response.status === 284) {
          setUsuario('');
          return;
        }
        setUsuario(response.data);
        setUser((prevUser) => ({
          ...prevUser,
          user_id: response.data.user_id,
        }));
        console.log(response);
      } catch (error) {
        setUsuario('');
      }
    };
  
    // Memorizar la función de búsqueda utilizando useCallback
    const debouncedBuscarUsuario = useCallback(
      _.debounce((codigo) => {
        searchUser(codigo);
      }, 500),
      [] // Solo se crea una vez al montar el componente
    );
  
    // Manejar cambios en el código ingresado por el usuario
    useEffect(() => {
      if (codigo === '') {
        setUsuario('');
        return;
      }
      // Llamar a la función debounced cada vez que cambia el código
      debouncedBuscarUsuario(codigo);
      // Limpiar debounce cuando el componente se desmonte o cambie "codigo"
      return () => {
        debouncedBuscarUsuario.cancel(); // Cancela cualquier búsqueda en curso
      };
    }, [codigo, debouncedBuscarUsuario]); // Dependencias

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
                label="Nombre de Acceso"
                variant="outlined"
                required
                name="username"
                value={user.username}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth variant="outlined" required>
                <TextField
                  labelId="userCode-label"
                  name="userCode"
                  value={codigo}
                  onChange={(e) => setCodigo(e.target.value)}
                  label="Código de Usuario"
                />

             
              </FormControl>

            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth variant="outlined" required>
              <TextField
                variant="outlined"
                disabled
                value={usuario ? usuario.first_name + " " + usuario.last_name : 'No encontrado'}
              ></TextField>
              </FormControl>

            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth variant="outlined" required>
                <InputLabel id="server-label">Servidor</InputLabel>
                <Select
                  labelId="server-label"
                  name="server_id"
                  value={user.server_id}
                  onChange={handleChange}
                  label="Servidor"
                >
                  <MenuItem value="-1"><em>None</em></MenuItem>
                  {
                    servers ? servers.map((server) => (
                      <MenuItem key={server.server_id} value={server.server_id}>{server.name}</MenuItem>
                    )) : null
                  }
                </Select>
              </FormControl>
            </Grid>

             
            <Grid item xs={12}>
              <FormControl fullWidth variant="outlined" required>
                <InputLabel id="group-label">Grupo</InputLabel>
                <Select
                  labelId="group-label"
                  name="group_id"
                  value={user.group_id}
                  onChange={handleChange}
                  label="Grupo"
                >
                  <MenuItem value="-1"><em>None</em></MenuItem>
                  <MenuItem value="1">Grupo 1</MenuItem>
                  <MenuItem value="2">Grupo 2</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12}>
              <FormControl fullWidth variant="outlined" required>
                <InputLabel id="server-label">Aprobador</InputLabel>
                <Select
                  labelId="aprover-label"
                  name="aprover_id"
                  value={user.aprover_id}
                  onChange={handleChange}
                  label="Aprobador"
                >
                  <MenuItem value="-1"><em>None</em></MenuItem>
                  {
                    
                    aprover ? aprover.map((aprover) => (
                      <MenuItem key={aprover.user_id} value={aprover.user_id}>{aprover.first_name + " " + aprover.last_name}</MenuItem>
                    )) : null
                  }
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

    </Container>
  );
};

export default CredentialCreation;