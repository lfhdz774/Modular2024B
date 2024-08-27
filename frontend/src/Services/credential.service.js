import http from './http';


export const PostCredential = async (credentialModel) => {
    try {
        const response = await http.post('/api/admin/CreateServerId', JSON.stringify(credentialModel), {
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