import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { FirstLoginService } from 'src/Services/FirstLogin.service';
import { Container, TextField, Typography, CircularProgress, Box } from '@mui/material';

const FirstLogin = () => {
    const { token } = useParams();
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (token) {
            FirstLoginService(token)
                .then((data) => {
                    setResponse(data);
                    setLoading(false);
                })
                .catch((error) => {
                    console.error('Failed to process first login:', error);
                    setError('Error fetching the password.');
                    setLoading(false);
                });
        }
    }, [token]);

    if (loading) {
        return (
            <Container maxWidth="sm" sx={{ textAlign: 'center', mt: 5 }}>
                <CircularProgress />
                <Typography variant="h6" mt={2}>
                    Procesando solicitud...
                </Typography>
            </Container>
        );
    }

    if (error) {
        return (
            <Container maxWidth="sm" sx={{ textAlign: 'center', mt: 5 }}>
                <Typography variant="h6" color="error">
                    {error}
                </Typography>
            </Container>
        );
    }

    return (
        <Container maxWidth="sm" sx={{ mt: 5 }}>
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: 2,
                    backgroundColor: '#f9f9f9',
                    padding: 4,
                    borderRadius: 2,
                    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
                }}
            >
                <Typography variant="h5" gutterBottom>
                    Primera vez iniciando sesión
                </Typography>
                <TextField
                    label="Contraseña generada"
                    value={response.password || ''}
                    InputProps={{
                        readOnly: true,
                    }}
                    fullWidth
                />
            </Box>
        </Container>
    );
};

export default FirstLogin;
