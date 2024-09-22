import http from './http';

export const PostCommands = async (CommandModel) => {
    try {
        const response = await http.post('/api/commands', JSON.stringify(CommandModel), {
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
