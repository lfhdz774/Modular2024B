// Importa las dependencias necesarias
import React, { useState, useEffect } from 'react';
import { Modal, Box, CircularProgress, Typography } from '@mui/material';
import { CheckCircle, Error } from '@mui/icons-material';

const RequestModal = ({ open, status, handleClose }) => {
  // Estilos para el modal
  const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 300,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  };

  // Efecto para cerrar automáticamente el modal después de un retraso
  useEffect(() => {
    if (status === 'success' || status === 'error') {
      const timer = setTimeout(() => {
        handleClose();
      }, 1500); // Cierra el modal después de 1.5 segundos

      return () => clearTimeout(timer); // Limpia el temporizador cuando el componente se desmonte o se actualice
    }
  }, [status, handleClose]);

  // Componente que se muestra dependiendo del estado de la request
  const renderContent = () => {
    switch (status) {
      case 'loading':
        return <CircularProgress />;
      case 'success':
        return <CheckCircle color="success" sx={{ fontSize: 60 }} />;
      case 'error':
        return <Error color="error" sx={{ fontSize: 60 }} />;
      default:
        return null;
    }
  };

  return (
    <Modal open={open} aria-labelledby="modal-title" aria-describedby="modal-description">
      <Box sx={style}>
        <Typography id="modal-title" variant="h6" component="h2">
          {status === 'loading' ? 'Procesando...' : status === 'success' ? '¡Éxito!' : 'Error'}
        </Typography>
        <Box sx={{ mt: 2 }}>
          {renderContent()}
        </Box>
      </Box>
    </Modal>
  );
};

export default RequestModal;
