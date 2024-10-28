import React, { useState, useEffect } from 'react';
import { Container, Paper, Typography, TextField, Button, Grid, InputLabel, Select, MenuItem } from '@mui/material';
import { PostServer, GetServers, GetServerById, UpdateServer } from 'src/Services/servers.service';
import RequestModal from 'src/components/RequestModal'

const RegisterServer = ({ isEditing }) => {
  const [formData, setFormData] = useState({
    name: '',
    hostname: '',
    ip_address: '',
    username: '',
    pkey: '',
    operating_system: '',
  });
  const [servers, setServers] = useState([]);
  const [selectedServerId, setSelectedServerId] = useState('');
  const [open, setOpen] = useState(false)
  const [status, setStatus] = useState('loading');

  // Fetch servers when in edit mode
  useEffect(() => {
    if (isEditing) {
      fetchServers();
    }
  }, [isEditing]);

  const fetchServers = async () => {
    try {
      const response = await GetServers();
      setServers(response);
      console.log('Servers:', response);
    } catch (error) {
      console.error('Error fetching servers:', error);
    }
  };

  const handleServerChange = async (e) => {
    console.log('Selected Server:', e.target.value);
    const serverId = e.target.value;  // Capture selected server ID
    console.log('Selected Server ID:', serverId);
    setSelectedServerId(serverId);  // Update selected server ID

    try {
      const server = await GetServerById(serverId);  // Fetch the server details
      console.log('Server Details:', server);
      setFormData({
        name: server.data.name || '',
        hostname: server.data.hostname || '',
        ip_address: server.data.ip_address || '',
        username: server.data.username || '',
        pkey: server.data.pkey || '',
        operating_system: server.data.operating_system || '',
      });
    } catch (error) {
      console.error('Error fetching server details:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditing && selectedServerId) {
        const updates = { ...formData };
        setOpen(true)
        const response = await UpdateServer({ server_id: selectedServerId, updates });
        if(response.status === 200){
          setStatus('success')
        }
        else{
          setStatus('error')
        }
          
        setOpen(false)
        console.log('Server Updated:', response);
      } else {
        const response = await PostServer(formData);
        console.log('Server Registered:', response);
        console.log(response.status)
      }
    } catch (error) {
      console.error('Error registering/updating server:', error);
    }
  };

  // Función para cerrar el modal
  const handleClose = () => {
    setOpen(false);
    setStatus('loading'); // Reinicia el estado de la request al cerrar el modal
  };



  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          {isEditing ? 'Editar Servidor' : 'Registrar Servidor'}
        </Typography>
        <form onSubmit={handleSubmit}>
          {isEditing && (
            <Grid item xs={12} sx={{ mb: 2 }}>
              <InputLabel id="server-select-label">Selecciona un servidor</InputLabel>
              <Select
                labelId="server-select-label"
                value={selectedServerId}  // Ensure this is bound to selectedServerId
                onChange={handleServerChange}  // Call the handleServerChange correctly
                fullWidth
              >
                <MenuItem key={0} value="">
                  <em>None</em>
                </MenuItem>
                {servers.map((server) => (
                  
                  <MenuItem key={server.server_id} value={server.server_id}>
                    {server.name}
                  </MenuItem>
                ))}
              </Select>
            </Grid>
          )}
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Name"
                variant="outlined"
                required
                name="name"
                value={formData.name}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Hostname"
                variant="outlined"
                required
                name="hostname"
                value={formData.hostname}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="IP Address"
                variant="outlined"
                required
                name="ip_address"
                value={formData.ip_address}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Username"
                variant="outlined"
                required
                name="username"
                value={formData.username}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Private Key"
                variant="outlined"
                required
                name="pkey"
                value={formData.pkey}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Operating System"
                variant="outlined"
                required
                name="operating_system"
                value={formData.operating_system}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Button variant="contained" color="primary" type="submit">
                {isEditing ? 'Update Server' : 'Register Server'}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
      <RequestModal open={open} status={status} handleClose={handleClose} ></RequestModal>
    </Container>
  );
};

export default RegisterServer;
