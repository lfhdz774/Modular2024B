import React, { useEffect, useState, useCallback} from 'react';
import { Container, Paper, Typography, TextField, Button, Grid, FormControl, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { AccessRequest,AccessesByUser, DeactivateAccess} from 'src/Services/credential.service'; // Reemplaza con la ruta actual al servicio
import DeleteIcon from '@mui/icons-material/Delete';
import { GetUserByCode, GetUsersByRole } from 'src/Services/user.service';
import IconButton from '@mui/material/IconButton';
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


export const DeleteAccess = () => {

    const [codigo, setCodigo] = useState('');
    const [user, setUser] = useState({
      server_id: -1,
      group_id: -1,
      user_id: 0,
      expireDate: null,
      aprover_id: -1,
      username: '',
    });
    const [Access, setAccess] = useState([]);
    
    const [usuario, setUsuario] = useState('');
  
  
    useEffect(() => {
      GetServersList();
      GetAprovers();
    }, []);
  
    const GetServersList = async() => {
     
    };
  
  
    const GetAprovers = async() => {
      try {
        const AproverResponse = await GetUsersByRole(3);
        console.log(AproverResponse);
      } catch (error) {
        console.error('Error getting aprovers', error);
      }
    };
  
  
    useEffect(() => {
        const fetchData = async () => {
          console.log(usuario);
          console.log("Buscando accesos, del usuario:", usuario.user_id);
          await GetAccessFromUser(usuario.user_id);
        };
      
        fetchData();
      }, [usuario]);

    const GetAccessFromUser = async (code) => {
        console.log("Buscando accesos, del usuario:", code);
        try {
          const response = await AccessesByUser(code);
          //setUsuario(response.data);
          if(response.data){
            console.log("Usuario encontrado");
           // setUsuario(response.data);
            setAccess(response.data);
          }
          console.log(response);
        } catch (error) {
          console.error('Error getting access', error);
         // setUsuario('');
           setAccess([]);
        }
      };
  
    const handleSecuritySubmit = () => {
        //setLoading(true); // Show loading modal
  
      // const data = {
      //   ...user,
      //   expireDate: user.expireDate ? user.expireDate.toISOString() : null,
      // };
  
      setTimeout(async () => {
        try {
          const response = await AccessRequest(user);
          //setLoading(false); // Hide loading modal
          // Handle successful response
          console.log('Credential created successfully', response);
        } catch (error) {
         //setLoading(false); // Hide loading modal
          // Handle error response
          console.error('Error creating credential', error);
        }
      }, 2000);
    };
  
    const handleSubmit = (event) => {
      event.preventDefault();
      handleSecuritySubmit();
    };

    const handleDeleteAccess  = async(access_id, server_id) => {
      let result = await DeactivateAccess(access_id, server_id); 

      console.log(result);
    }
  
    
      // Función que realiza la búsqueda del usuario en la API
      const searchUser = async (code) => {
        try {
          const response = await GetUserByCode(code);
          console.log(response.data);
          if (response.status === 284) {
            setUsuario('');
            return;
          }
          setUsuario(response.data);
          if(response.data){
            console.log("Usuario encontrado");
            setUsuario(response.data);
          }
          console.log(response);
        } catch (error) {
          console.error('Error getting user', error);
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
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            Eliminar accesos
          </Typography>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
             
              <Grid item xs={6}>
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

              <Grid item xs={6}>
                <FormControl fullWidth variant="outlined" required>
                <TextField
                  variant="outlined"
                  disabled
                  value={usuario ? usuario.first_name + " " + usuario.last_name : 'No encontrado'}
                ></TextField>
                </FormControl>
  
              </Grid>

                <Grid item xs={12}>
                <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                                <TableCell>Servidor</TableCell>
                                <TableCell>Access ID</TableCell>
                                <TableCell>Rol</TableCell>
                                <TableCell>Activo Desde</TableCell>
                                <TableCell>Estatus</TableCell>
                                <TableCell></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {Access.map((access) => (
                            <TableRow key={access.id}>
                                <TableCell>{access.server_name}</TableCell>
                                <TableCell>{access.access_name}</TableCell>
                                <TableCell>{access.user_groups}</TableCell>
                                <TableCell>{access.created_at}</TableCell>
                                <TableCell>{access.status ? "Activo" : "Inactivo"}</TableCell>
                                <TableCell><IconButton aria-label="delete" onClick={() => handleDeleteAccess(access.access_name, access.server_id)}><DeleteIcon /></IconButton></TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
                </Grid>

            </Grid>
          </form>
        </Paper>
  
      </Container>
    );
};
