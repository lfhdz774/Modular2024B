import http from './http';

export const login = async (username, password) => {
    try {
        // Convert password to byte string
        const passwordBytes = new TextEncoder().encode('password');
        console.log('bytes', passwordBytes);
        const response = await http.post('/api/login', { username, password }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        localStorage.setItem('token', response.data.access_token);
        return response;
    } catch (error) {
        console.log(error);
        // Handle different types of errors here
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
