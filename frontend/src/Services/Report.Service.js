import http from './http';


export const GetChartReport = async () => {
    try {
        const response = await http.get('/api/admin/report/AccessesCount');
        return response.data;
    } catch (error) {
        return error;
    }
}