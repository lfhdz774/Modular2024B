import axios from 'axios';

const http = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 10000,
});

// Add a request interceptor
http.interceptors.request.use(function (config) {
    // Do something before request is sent
    const token = localStorage.getItem('token'); // Fetch the token from local storage
    config.headers.Authorization =  `Bearer ${token}`;
    return config;
  }, function (error) {
    // Do something with request error
    return Promise.reject(error);
});

export default http;