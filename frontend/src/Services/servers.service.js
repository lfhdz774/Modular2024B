import http from "./http";

export const PostServer = async (ServerModel) => {
    console.log(ServerModel)
    try {
        const response = await http.post('/api/admin/CreateServer',ServerModel, {
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

export const GetServers = async() => {
    try {
        const response = await http.get('/api/admin/GetServers');
        return response.data;
    } catch (error) {
        console.log(error);
        return error;
    }
}

export const GetServerById = async(serverId) => {
    console.log(serverId)
    try {
        const response = await http.get('/api/admin/GetServer/' + serverId);
        return response.data;
    } catch (error) {
        console.log(error);
        return error;
    }
}

export const UpdateServer = async (ServerModel) => {
    console.log(ServerModel)
    try {
        const response = await http.put('/api/admin/UpdateServer',ServerModel, {
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