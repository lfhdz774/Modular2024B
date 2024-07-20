import http from './http';
import {UserModel} from 'src/Models/UserModel'; // Import the UserModel class
export const GetUser = async() => {
    try {
        const response = await http.get('/api/user');
        return response.data;
    } catch (error) {
        return new UserModel();
    }
}