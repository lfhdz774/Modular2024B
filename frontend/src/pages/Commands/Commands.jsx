// import React, { useState } from 'react';
// import { PostCommands } from 'src/Services/command.service';
// import { Container, TextField, Button, Typography, Box, Link } from '@mui/material';

// function Command() {
//   const [comando, setComando] = useState('');
//   const [respuesta, setRespuesta] = useState('');
//   const [link, setLink] = useState('');

//   const enviarComando = async () => {
//     try {
//       // El nombre del campo debe ser exactamente 'comando' para que el backend lo reciba correctamente
//       let Comando = {
//         comando: comando  // Esto envía el valor del comando directamente
//       };
      
//       const response = await PostCommands(Comando);  // Envía el objeto correctamente
//       console.log(response);
//       setRespuesta(response.respuesta.message);
//       setLink(response.respuesta.link);

//     } catch (error) {
//       console.error("Error al enviar el comando:", error);
//     }
//   };

//   return (
//     <Container maxWidth="sm" sx={{ mt: 5 }}>
//       <Box
//         sx={{
//           display: 'flex',
//           flexDirection: 'column',
//           gap: 3,
//           alignItems: 'center',
//           backgroundColor: '#f9f9f9',
//           padding: 4,
//           borderRadius: 2,
//           boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
//         }}
//       >
//         <Typography variant="h4" component="h1" gutterBottom>
//           Procesador de Comandos
//         </Typography>

//         <TextField
//           label="Escribe un comando"
//           variant="outlined"
//           value={comando}
//           onChange={(e) => setComando(e.target.value)}
//           fullWidth
//         />

//         <Button 
//           variant="contained" 
//           color="primary" 
//           onClick={enviarComando} 
//           sx={{ width: '100%' }}
//         >
//           Enviar Comando
//         </Button>

//         {respuesta && (
//           <Typography variant="body1" color="textPrimary">
//             Respuesta: {respuesta}
//           </Typography>
//         )}

//         {link && (
//           <Link href={link} target="_blank" rel="noopener"  sx={{ wordBreak: 'break-all' }}>
//             {link}
//           </Link>
//         )}
//       </Box>
//     </Container>
//   );
// }

// export default Command;


import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  List,
  ListItem,
  ListItemAvatar,
  Avatar,
  ListItemText,
  TextField,
  IconButton,
  Paper,
} from '@mui/material';
import { PostCommands } from 'src/Services/command.service';
import SendIcon from '@mui/icons-material/Send';

function Command() {
  const [messages, setMessages] = useState([
    { text: 'Bienvenido al chat.', sender: 'sistema' },
  ]);
  const [newMessage, setNewMessage] = useState('');

  // Referencia al contenedor de mensajes
  const messagesContainerRef = useRef(null);

  // Función para hacer scroll al final (parte inferior)
  const scrollToBottom = () => {
    messagesContainerRef.current?.scrollTo({
      top: messagesContainerRef.current.scrollHeight,
      behavior: 'smooth',
    });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (newMessage.trim() !== '') {
      // Añadir el mensaje del usuario
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: newMessage, sender: 'yo' },
      ]);

      const userMessage = newMessage;
      setNewMessage('');

      try {
        // Petición al backend
        const Comando = {
          comando: userMessage,
        };
        const response = await PostCommands(Comando);
        console.log(response);
        if (response.status === 200) {
          console.log(response.status, response.data.respuesta.message);

          setMessages((prevMessages) => [
            ...prevMessages,
            { text: response.data.respuesta.message, sender: 'sistema' },
          ]);
        } else {
          console.log(response.status);
          let errorMessage = '';
          switch (response.status) {
            case 404:
              errorMessage = 'Error 404: Recurso no encontrado.';
              break;
            case 500:
              errorMessage = 'Error 500: Error interno del servidor.';
              break;
            default:
              errorMessage = `Error ${response.status}: Ocurrió un error al procesar tu solicitud.`;
          }
          setMessages((prevMessages) => [
            ...prevMessages,
            { text: errorMessage, sender: 'sistema' },
          ]);
        }
      } catch (error) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: 'Error: No se pudo conectar con el servidor.', sender: 'sistema' },
        ]);
      }
    }
  };

  return (
    <Paper
      elevation={3}
      style={{
        width: '100%',
        height: '100%',
        padding: 16,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Box
        style={{
          flexGrow: 1,
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column-reverse',
        }}
        ref={messagesContainerRef}
      >
        <List
          style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start'       }}
        >
          {messages.map((message, index) => (
            <ListItem
              key={index}
              style={{
                justifyContent:
                  message.sender === 'yo'
                    ? 'flex-end'
                    : message.sender === 'sistema'
                    ? 'flex-start'
                    : 'center',
              }}
            >
              {message.sender === 'otro' && (
                <ListItemAvatar>
                  <Avatar>{message.sender.charAt(0).toUpperCase()}</Avatar>
                </ListItemAvatar>
              )}
              <ListItemText
                primary={message.text}
                style={{
                  backgroundColor:
                    message.sender === 'yo'
                      ? '#e1f5fe'
                      : message.sender === 'sistema'
                      ? '#fff9c4'
                      : '#f1f1f1',
                  borderRadius: 8,
                  padding: '8px 16px',
                  maxWidth: '60%',
                  textAlign:
                    message.sender === 'yo'
                      ? 'right'
                      : message.sender === 'sistema'
                      ? 'center'
                      : 'left',
                  wordBreak: 'break-word',
                }}
              />
              {message.sender === 'yo' && (
                <ListItemAvatar>
                  <Avatar>{message.sender.charAt(0).toUpperCase()}</Avatar>
                </ListItemAvatar>
              )}
            </ListItem>
          ))}
        </List>
      </Box>
      <Box display="flex" mt={2}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Escribe un mensaje..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') handleSend();
          }}
        />
        <IconButton color="primary" onClick={handleSend}>
          <SendIcon />
        </IconButton>
      </Box>
    </Paper>
  );
}

export default Command;
