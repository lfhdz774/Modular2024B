import http from './http';

export const FirstLoginService = async (token) => {
    try {
        const response = await http.get(`/api/first-login/password/${token}`,{
            Headers: {
                'Content-Type': 'application/json',
                'allow-origin': '*',
                'allow-credentials': true,
            },
        });
        return response.data;
    } catch (error) {
        console.error(error);
        throw error; 
    }
};