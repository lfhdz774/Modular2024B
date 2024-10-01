import http from './http';


export const PostCredential = async (credentialModel) => {
    try {
        const response = await http.post('/api/admin/CreateAccess', JSON.stringify(credentialModel), {
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

export const AccessRequest = async (accessRequestModel) => {
    try {
        const response = await http.post('/api/admin/AccessRequest', JSON.stringify(accessRequestModel), {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response;
    } catch (error) {
        console.log(error);
        return error;
    }
}


export const GetAccessRequests = async () => {
    try {
        console.log('GetAccessRequests');
        const response = await http.get('/api/admin/GetAllRequests');
        return response;
    } catch (error) {
        return error;
    }
}

export const ApproveRequest = async (requestId) => {
    try {
        const response = await http.post(`/api/admin/ApproveRequest/${requestId}`);
        return response;
    } catch (error) {
        return error;
    }
}