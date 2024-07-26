import http from './http';

export const login = async (username, password) => {
    try {
        const response = await http.post('/api/login', { username, password }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        localStorage.setItem('token', response.data.access_token)
        return response;
    } catch (error) {
        console.log(error);
        throw new Error('Login failed', error);
    }
};


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
