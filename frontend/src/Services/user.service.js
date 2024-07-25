import http from './http';

export const GetUser = async () => {
    try {
        const response = await http.get('/api/user');
        return response.data;
    } catch (error) {
        return error;
    }
};

export const PostUser = async (userModel) => {
    try {
        const response = await http.post('/api/admin/signup', JSON.stringify(userModel), {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.log(error);
        return error;
    }
};


export const GetUserRoles = async () => {
    try {
        const response = await http.get('/api/user/roles');
        return response.data;
    } catch (error) {
        return error;
    }
};