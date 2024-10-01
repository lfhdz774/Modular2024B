import React, { useState, useEffect } from 'react';
import { TextField, Button, Box, Select, MenuItem, InputLabel, FormControl } from '@mui/material';
import { GetUser, PostUser, GetUserPositions } from 'src/Services/user.service'; // Reemplaza con la ruta actual al servicio
import { UserModel } from 'src/Models/UserModel';

const UserAdministration = () => {
    const [positions, setPositions] = useState([]);
    
    const [user, setUser] = useState({
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        employee_code: '',
        role_id: -1,
        employee_position: -1,
    });



    const handleChange = (e) => {
        const { name, value } = e.target;
        setUser((prevUser) => ({
            ...prevUser,
            [name]: value,
        }));
    };

    const handleRoleChange = (e) => {
        setUser((prevUser) => ({
            ...prevUser,
            role_id: e.target.value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        //const newUser = new UserModel(user.username, user.password, user.email, user.first_name, user.last_name, user.employee_code, user.role_id);

        try {
            const response = await PostUser(user);
            console.log(response);
        } catch (error) {
            console.log(error);
        }
    };

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const fetchedUser = await GetUser();
                setUser(fetchedUser);
            } catch (error) {
                console.log(error);
            }
        };

        //fetchUser();
        fetchPositions();
    }, []);

    const fetchPositions = async () => {
        try {
            const response = await GetUserPositions();
            setPositions(response);
            console.log('Positions:', response);
        } catch (error) {
            console.error('Error fetching positions:', error);
        }
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: '20px', padding: '20px', maxWidth: '40rem' }}>
            <TextField
                name="username"
                label="Usuario"
                value={user.username}
                onChange={handleChange}
                fullWidth
                variant="filled"
                autoComplete="new-username"
            />
            <TextField
                name="password"
                label="Contraseña"
                value={user.password}
                onChange={handleChange}
                fullWidth
                type="password"
                variant="filled"
                autoComplete="new-password"
            />
            <TextField
                name="email"
                label="Email"
                value={user.email}
                onChange={handleChange}
                fullWidth
                variant="filled"
            />
            <TextField
                name="first_name"
                label="Nombres"
                value={user.first_name}
                onChange={handleChange}
                fullWidth
                variant="filled"
            />
            <TextField
                name="last_name"
                label="Apellidos"
                value={user.last_name}
                onChange={handleChange}
                fullWidth
                variant="filled"
            />
            <TextField
                name="employee_code"
                label="Código de empleado"
                value={user.employee_code}
                onChange={handleChange}
                fullWidth
                variant="filled"
            />
            <FormControl fullWidth>
                <InputLabel id="rolLabel">Rol</InputLabel>
                <Select
                    id="role_id"
                    labelId="rolLabel"
                    name="role_id"
                    value={user.role_id}
                    onChange={handleRoleChange}
                    fullWidth
                    variant="filled"
                >
                    <MenuItem value={1}>Administrador</MenuItem>
                    <MenuItem value={2}>Usuario</MenuItem>
                    <MenuItem value={3}>Aprobador</MenuItem>
                    <MenuItem value={4}>Administrador de conexiones</MenuItem>
                    <MenuItem value={5}>Auditor</MenuItem>
                    <MenuItem value={6}>Soporte</MenuItem>
                    <MenuItem value={7}>Super usuario</MenuItem>
                </Select>
            </FormControl>
            <FormControl fullWidth>
                <InputLabel id="positionLabel">Puesto</InputLabel>
                <Select
                    labelId="positionLabel"
                    value={user.employee_position}
                    onChange={handleChange}
                    fullWidth
                    variant='filled'
                    name='employee_position'
                    id='employee_position'
                >
                    <MenuItem key={0} value="">
                        <em>None</em>
                    </MenuItem>
                    {positions.map((position) => (

                        <MenuItem key={position.position_Id} value={position.position_Id}>
                            {position.position_name}
                        </MenuItem>
                    ))}
                </Select>

            </FormControl>
            <Button variant="contained" color="primary" onClick={handleSubmit}>
                Guardar
            </Button>
        </Box>
    );
};

export default UserAdministration;
