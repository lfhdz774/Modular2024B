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
        console.log(userModel)
        const response = await http.post('/api/admin/signup', JSON.stringify(userModel), {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.log(userModel);
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

export const GetUserPositions = async () => {
    try {
        const response = await http.get('/api/user/positions');
        return response.data;
    } catch (error) {
        return error;
    }
};

export const GetUserByCode = async (code) => {
    try {
        const response = await http.get(`/api/user/${code}`);
        return response;
    } catch (error) {
        return error;
    }
}

export const GetUsersByRole = async (role) => {
    try {
        const response = await http.get(`/api/user/role/${role}`);
        return response;
    } catch (error) {
        return error;
    }
}

