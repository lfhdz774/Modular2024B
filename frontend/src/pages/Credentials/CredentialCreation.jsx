import React, { useState } from 'react';
import { TextField, Button, MenuItem, Select, InputLabel, FormControl, Grid, Switch, FormControlLabel } from '@mui/material';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import axios from 'axios';

const CredentialCreation = () => {
    const [server, setServer] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [expireDate, setExpireDate] = useState(null);
    const [appUserId, setAppUserId] = useState('');
    const [group, setGroup] = useState('');
    const [hasExpireDate, setHasExpireDate] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const credentialData = {
            server,
            username,
            password,
            expireDate: hasExpireDate ? expireDate : null,
            appUserId,
            group,
        };

        try {
            const response = await axios.post('/api/credentials', credentialData);
            console.log('Credential created:', response.data);
        } catch (error) {
            console.error('Error creating credential:', error);
        }
    };

    return (
        <div>

            <form onSubmit={handleSubmit} autoComplete='false' style={{ marginTop: "10px", width: "50%" }} >
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel id="server-label">Server</InputLabel>
                            <Select
                                labelId="server-label"
                                value={server}
                                onChange={(e) => setServer(e.target.value)}
                                required
                            >
                                <MenuItem value="server1">Server 1</MenuItem>
                                <MenuItem value="server2">Server 2</MenuItem>
                                <MenuItem value="server3">Server 3</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            label="Nombre de usuario"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            fullWidth
                            required
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            label="Contraseña"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            fullWidth
                            required
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={hasExpireDate}
                                    onChange={(e) => setHasExpireDate(e.target.checked)}
                                    color="primary"
                                />
                            }
                            label="Set Expire Date"
                        />
                    </Grid>
                    {hasExpireDate && (
                        <Grid item xs={12}>
                            <DatePicker
                                selected={expireDate}
                                onChange={(date) => setExpireDate(date)}
                                customInput={<TextField label="Expire Date" fullWidth required />}
                                dateFormat="Pp"
                                zindex={9999}
                            />
                        </Grid>
                    )}
                    <Grid item xs={12}>
                        <TextField
                            label="App User ID"
                            value={appUserId}
                            onChange={(e) => setAppUserId(e.target.value)}
                            fullWidth
                            required
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel id="group-label">Group</InputLabel>
                            <Select
                                labelId="group-label"
                                value={group}
                                onChange={(e) => setGroup(e.target.value)}
                                required
                            >
                                <MenuItem value="group1">Group 1</MenuItem>
                                <MenuItem value="group2">Group 2</MenuItem>
                                <MenuItem value="group3">Group 3</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <Button type="submit" variant="contained" color="primary" fullWidth>
                            Create Credential
                        </Button>
                    </Grid>
                </Grid>
            </form>
        </div>

    );
};

export default CredentialCreation;