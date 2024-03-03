import http from './http';
import bcrypt from "bcryptjs";

export const login = async (username, unhashedpassword) => {
    
    try {
        const password = await bcrypt.hash(unhashedpassword, process.env.REACT_APP_PASSWORD_SALT);
        console.log(password);
        const response = await http.post('/api/login', { username, password }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        localStorage.setItem('token', response.data.access_token);
        return response;
    } catch (error) {
        console.log(error);
        // Manejar diferentes tipos de errores aquí
        throw new Error('Login failed', error);
    }
};
// Function to logout
export const logout = async () => {
    localStorage.removeItem('token');
};

export const checkLoggedIn = async () => {
    try {
        const response = await http.get('/checkLoggedIn');
        return response.data.isLoggedIn;
    } catch (error) {
        throw new Error('Failed to check login status');
    }
};
