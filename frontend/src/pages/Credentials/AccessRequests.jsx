import React, { useEffect, useState, useCallback } from 'react';
import { GetAccessRequests } from 'src/Services/credential.service';
import {
  Container,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
  IconButton,
  Collapse,
  Grid,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import {ApproveRequest} from 'src/Services/credential.service';
// Estilo para la estructura del contenedor principal
const containerStyle = {
  marginTop: 4,
  marginBottom: 4,
};

// Estilo del contenedor expandido
const expandedStyle = {
  margin: 1,
};





const Row = ({ row, onUpdate }) => {
  const [open, setOpen] = useState(false);
  const [openModal, setOpenModal] = useState(false);
  const [modalMessage, setModalMessage] = useState('');

  const handleClickOpen = (message) => {
    if (message["message"]){
      if(message["link"]){
        setModalMessage(message["message"] + " " + message["link"]);
      }
      else{
        setModalMessage(message["message"]);
      }
    }
    
    setOpenModal(true);
  };

  const handleClose = () => {
    setOpenModal(false);
  };

  // Función para manejar el clic en el botón "Aprobar"
  const handleApprove = async () => {
    const result = await approveRequest(row.request_id);
    handleClickOpen(result);
    if (result) {
      onUpdate(); // Llamar a la función de actualización si la aprobación fue exitosa
    }
  };

  // Función para manejar el clic en el botón "Rechazar"
  const handleReject = async () => {
    const result = await rejectRequest(row.request_id);
    if (result) {
      onUpdate(); // Llamar a la función de actualización si el rechazo fue exitoso
    }
  };


  const approveRequest = async (requestId) => {
    try {
      const response = await ApproveRequest(requestId);
      console.log('Request approved:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error approving request:', error);
    }
  };
  
  // Función para manejar el rechazo del request
  const rejectRequest = async (requestId) => {
    // try {
    //   const response = await axios.post(`/api/requests/${requestId}/reject`);
    //   console.log('Request rejected:', response.data);
    //   return response.data;
    // } catch (error) {
    //   console.error('Error rejecting request:', error);
    // }
  };

  return (
    <React.Fragment>
      <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
        {/* Icono para expandir y contraer la fila */}
        <TableCell>
          <IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        <TableCell>{row.server_name}</TableCell>
        <TableCell align="right">{row.group_name}</TableCell>
        <TableCell align="right">{row.user_id}</TableCell>
        <TableCell align="right">{row.position}</TableCell>
      </TableRow>
      {/* Información adicional que se muestra al expandir */}
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={expandedStyle}>
              <Typography variant="h6" gutterBottom component="div">
                Detalles del Request
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle1">
                    Fecha de Creación: {row.created_at}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle1">
                    Creado por: {row.requester_name}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle1">
                    Fecha de Expiración: {row.expires_at || 'Sin Expiración'}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle1">
                    Estatus: {row.status}
                  </Typography>
                </Grid>
                {/* Botones de Aprobar y Rechazar */}
                <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'space-between', marginTop: 2 }}>
                  <Button
                    variant="contained"
                    color="success"
                    onClick={handleApprove}
                    disabled={row.status !== 'Pending'} // Desactivar si no está pendiente
                  >
                    Aprobar
                  </Button>
                  <Button
                    variant="contained"
                    color="error"
                    onClick={handleReject}
                    disabled={row.status !== 'Pending'} // Desactivar si no está pendiente
                  >
                    Rechazar
                  </Button>
                </Grid>
              </Grid>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>



      <Dialog open={openModal} onClose={handleClose}>
        <DialogTitle>Result</DialogTitle>
        <DialogContent>
          <DialogContentText>{modalMessage}</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
};

// Componente principal para mostrar la tabla de requests pendientes
const PendingRequests = () => {
  const [requests, setRequests] = useState([]);
  

  // Función para obtener los requests pendientes desde el backend
  const fetchRequests = async () => {
    try {
      const response = await GetAccessRequests();
      setRequests(response.data);
      console.log('Requests pendientes:', response.data);
    } catch (error) {
      console.error('Error al obtener los requests pendientes:', error);
    }
  };

  useEffect(() => {
    fetchRequests(); // Obtener los requests cuando se monta el componente
  }, []);

  const updateRequests = () => {
    fetchRequests(); // Llama a la función para traer de nuevo las solicitudes
  };

  return (
    <Container maxWidth="md" sx={containerStyle}>
      <Paper sx={{ padding: 3 }}>
        <Typography variant="h5" gutterBottom>
          Requests Pendientes
        </Typography>
        <TableContainer component={Paper}>
          <Table aria-label="collapsible table">
            <TableHead>
              <TableRow>
                <TableCell />
                <TableCell>Servidor</TableCell>
                <TableCell align="right">Grupo</TableCell>
                <TableCell align="right">Código de Usuario</TableCell>
                <TableCell align="right">Puesto</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {requests ? requests.map((request) => (
                 <Row key={request.request_id} row={request} onUpdate={updateRequests} />
              )) : null}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Container>
  );
};

export default PendingRequests;
