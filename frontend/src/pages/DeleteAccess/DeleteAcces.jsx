import React, { useEffect, useState, useCallback} from 'react';
import { Container, Paper, Typography, TextField, Button, Grid, MenuItem, Select, FormControl, InputLabel, Checkbox, FormControlLabel, Backdrop, Box, Modal, Fade, FormLabel } from '@mui/material';
import 'dayjs/locale/es-mx'; // Import the Mexican Spanish locale for Day.js
import { AccessRequestForMe} from 'src/Services/credential.service'; // Reemplaza con la ruta actual al servicio
import { GetServers } from 'src/Services/servers.service';
import {  GetUsersByRole } from 'src/Services/user.service';
import RequestModal from 'src/components/RequestModal';
import _, { set } from 'lodash';

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


export const DeleteAccess = () => {

const [data, setData] = useState([]);
const [servers, setServers] = useState([]);
const [loading, setLoading] = useState(false);
const [status, setStatus] = useState('');
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
    } catch (error) {
      console.error('Error getting aprovers', error);
    }
  };



  const handleChange = (e) => {
    const { name, value } = e.target;
    setData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleRequestChange = (e) => {

  };


  const handleSubmit = (event) => {
    event.preventDefault();
    handleSecuritySubmit();
  };

  const handleSecuritySubmit = () => {
    setStatus("loading");
    setLoading(true); // Show loading modal


  setTimeout(async () => {
    try {
      const response = await AccessRequestForMe(data);
      if(response.status === 201)
        setStatus("success");
      else
        setStatus("error");

      setLoading(false); // Hide loading modal
      // Handle successful response
      console.log('Credential created successfully', response);
      
    } catch (error) {
      setStatus("error");
      setLoading(false); // Hide loading modal
      // Handle error response
      console.error('Error creating credential', error);
    }
  }, 2000);
};

  
  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Solicitar Acceso
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <FormControl fullWidth variant="outlined" required>
                <InputLabel id="server-label">Servidor</InputLabel>
                <Select
                  labelId="server-label"
                  name="server_id"
                  value={data.server_id}
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
                  value={data.group_id}
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
                  name="approver_id"
                  value={data.approver_id}
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
              <Button variant="contained" color="primary" type="submit">
                Crear
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>

      <RequestModal status={status} handleClose={handleRequestChange} ></RequestModal>
    </Container>
  );
};
