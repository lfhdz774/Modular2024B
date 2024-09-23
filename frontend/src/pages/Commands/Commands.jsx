import React, { useState } from 'react';
import { PostCommands } from 'src/Services/command.service';
import { Container, TextField, Button, Typography, Box, Link } from '@mui/material';

function Command() {
  const [comando, setComando] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [link, setLink] = useState('');

  const enviarComando = async () => {
    try {
      // El nombre del campo debe ser exactamente 'comando' para que el backend lo reciba correctamente
      let Comando = {
        comando: comando  // Esto envía el valor del comando directamente
      };
      
      const response = await PostCommands(Comando);  // Envía el objeto correctamente
      console.log(response);
      setRespuesta(response.respuesta.message);
      setLink(response.respuesta.link);

    } catch (error) {
      console.error("Error al enviar el comando:", error);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 5 }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 3,
          alignItems: 'center',
          backgroundColor: '#f9f9f9',
          padding: 4,
          borderRadius: 2,
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Procesador de Comandos
        </Typography>

        <TextField
          label="Escribe un comando"
          variant="outlined"
          value={comando}
          onChange={(e) => setComando(e.target.value)}
          fullWidth
        />

        <Button 
          variant="contained" 
          color="primary" 
          onClick={enviarComando} 
          sx={{ width: '100%' }}
        >
          Enviar Comando
        </Button>

        {respuesta && (
          <Typography variant="body1" color="textPrimary">
            Respuesta: {respuesta}
          </Typography>
        )}

        {link && (
          <Link href={link} target="_blank" rel="noopener"  sx={{ wordBreak: 'break-all' }}>
            {link}
          </Link>
        )}
      </Box>
    </Container>
  );
}

export default Command;
