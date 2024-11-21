import http from './http';


export const GetChartReport = async () => {
    try {
        const response = await http.get('/api/admin/report/AccessesCount');
        return response.data;
    } catch (error) {
        return error;
    }
}

export const postReportGenerator = async (reportData) => {
    try {
        const response = await http.post('/api/admin/report/Generate', reportData, {
            headers: {
                'Content-Type': 'application/json',
            }}
        );
        return response;
    } catch (error) {
        return error;
    }
}
export const recentAccessReport = async () => {
    try {
        const response = await http.get('/api/admin/report/RecentAccesses');
        return response;
    } catch (error) {
        return error;
    }
}