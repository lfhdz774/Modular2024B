// Import your HTTP service
import http from './http';

// Function to send login request
export const login = async (username, password) => {
    try {
        // Send a POST request with the appropriate headers
        const response = await http.post('/login', { username, password }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        localStorage.setItem('token', response.data.token);
        return response;
    } catch (error) {
        console.log(error);
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
