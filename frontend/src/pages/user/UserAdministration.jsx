import React, { useState, useEffect } from 'react';
import { TextField, Button, Box } from '@mui/material';
import { GetUser, PostUser } from 'src/Services/user.service'; // Replace with the actual path to the service
import { UserModel } from 'src/Models/UserModel';

const UserAdministration = () => {
    const [user, setUser] = useState({
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        employee_code: '',
        role_id: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUser((prevUser) => ({
            ...prevUser,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      const newUser = new UserModel(user.username, user.password, user.email, user.first_name, user.last_name, user.employee_code, user.role_id);
  
      try {
          const response = await PostUser(newUser);
      } catch (error) {
          console.log(error);
      }
  };

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const user = await GetUser();
                setUser(user);
                console.log(user);
            } catch (error) {
                console.log(error);
            }
        };

        fetchUser();
    }, []);

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: '20px', padding: '20px', maxWidth: '40rem' }}>
            <TextField
                name="username"
                label="Username"
                value={user.username}
                onChange={handleChange}
                fullWidth
                variant="filled"
                autoComplete="new-username"
            />
            <TextField
                name="password"
                label="Password"
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
                label="First Name"
                value={user.first_name}
                onChange={handleChange}
                fullWidth
                variant="filled"
            />
            <TextField
                name="last_name"
                label="Last Name"
                value={user.last_name}
                onChange={handleChange}
                fullWidth
                variant="filled"
            />
            <TextField
                name="employee_code"
                label="Employee Code"
                value={user.employee_code}
                onChange={handleChange}
                fullWidth
                variant="filled"
            />
            <TextField
                name="role_id"
                label="Role ID"
                value={user.role_id}
                onChange={handleChange}
                fullWidth
                variant="filled"
            />
            <Button variant="contained" color="primary" onClick={handleSubmit}>
                Guardar
            </Button>
        </Box>
    );
};

export default UserAdministration;

