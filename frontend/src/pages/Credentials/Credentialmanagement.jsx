import React, { useState, useEffect } from 'react';
import { Select, MenuItem, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const CredentialManagement = () => {
    const [selectedServer, setSelectedServer] = useState('');
    const [credentials, setCredentials] = useState([]);

    useEffect(() => {
        const fetchCredentials = async () => {
            try {
                const response = await fetch(`API_ENDPOINT/${selectedServer}`);
                const data = await response.json();
                setCredentials(data);
            } catch (error) {
                console.error('Error fetching credentials:', error);
            }
        };

        fetchCredentials();
    }, [selectedServer]);

    const handleServerChange = (event) => {
        setSelectedServer(event.target.value);
    };

    return (
        <div>
            <Select value={selectedServer} onChange={handleServerChange} label="Servidor">
                <MenuItem value="server1">Server 1</MenuItem>
                <MenuItem value="server2">Server 2</MenuItem>
                <MenuItem value="server3">Server 3</MenuItem>
            </Select>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Username</TableCell>
                            <TableCell>Password</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {credentials.map((credential) => (
                            <TableRow key={credential.id}>
                                <TableCell>{credential.username}</TableCell>
                                <TableCell>{credential.password}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
};

export default CredentialManagement;