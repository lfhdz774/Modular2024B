import React, { useState, useEffect } from 'react';
import { TextField, Button, Box } from '@mui/material';
import { GetUser } from 'src/Services/user.service'; // Replace with the actual path to the service


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

    const handleSubmit = (e) => {
        e.preventDefault();
        // Add your logic to update the user data here
        console.log(user); // Just for demonstration, you can remove this line
    };

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const user = await GetUser(); // Replace with the actual function to get the user data
                setUser(user);
                console.log(user);
            } catch (error) {
                console.log(error);
            }
        };

        fetchUser();
    }, []);

    return (
        <Box sx={{display: 'flex', flexDirection: 'column', gap: '20px', padding: "20px", maxWidth: "40rem"}}>
      <TextField
        name="username"
        label="Username"
        value={user.username}
        onChange={() => handleChange}
        fullWidth
      />
      <TextField
        name="password"
        label="Password"
        value={user.password}
        onChange={() => handleChange}
        fullWidth
        type="password"
      />
      <TextField
        name="email"
        label="Email"
        value={user.email}
        onChange={handleChange}
        fullWidth
      />
      <TextField
        name="firstName"
        label="First Name"
        value={user.first_name}
        onChange={handleChange}
        fullWidth
      />
      <TextField
        name="lastName"
        label="Last Name"
        value={user.last_name}
        onChange={handleChange}
        fullWidth
      />
      <TextField
        name="employeeCode"
        label="Employee Code"
        value={user.employee_code}
        onChange={handleChange}
        fullWidth
      />
      <TextField
        name="roleId"
        label="Role ID"
        value={user.role_id}
        onChange={handleChange}
        fullWidth
      />
      <Button variant="contained" color="primary" onClick={(e) => handleSubmit(e)} >
        Save
      </Button>
    </Box>
    );
};

export default UserAdministration;