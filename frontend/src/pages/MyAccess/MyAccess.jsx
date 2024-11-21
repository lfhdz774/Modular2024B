import React, { useEffect, useState, useCallback} from 'react';
import { Container, Paper, Typography, TextField, Button, Grid, FormControl, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { AccessesMyUser, DeactivateAccess} from 'src/Services/credential.service'; // Reemplaza con la ruta actual al servicio
import DeleteIcon from '@mui/icons-material/Delete';
import { GetUserByCode, GetUsersByRole } from 'src/Services/user.service';
import IconButton from '@mui/material/IconButton';
import RequestModal from 'src/components/RequestModal';
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


export const MyAccess = () => {
    const [Access, setAccess] = useState([]);
    const [status, setStatus] = useState('');

  
  
    useEffect(() => {
        const fetchData = async () => {
        await GetAccessFromUser();

        };
      
        fetchData();
      }, []);

    const GetAccessFromUser = async () => {
        try {
          const response = await AccessesMyUser();
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

    const handleDeleteAccess  = async(access_id, server_id) => {
      setStatus("loading");
      let result = await DeactivateAccess(access_id, server_id); 
      if(result.status === 200){
        setStatus("success");
        
      }else{
        setStatus("error");
      }
      await GetAccessFromUser();
      console.log(result);
    }
  
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            Mis accesos
          </Typography>
            <Grid container spacing={2}>
             
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
                                <TableCell > {access.status ? <IconButton aria-label="delete"  onClick={() => handleDeleteAccess(access.access_name, access.server_id)}><DeleteIcon /> </IconButton> : <></> }</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
                </Grid>

            </Grid>
        </Paper>

        <RequestModal status={status} handleClose={() => console.log("closing")} ></RequestModal>
  
      </Container>
    );
};
