import axios from 'axios';

const http = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 10000,
});

// Add a request interceptor
http.interceptors.request.use(function (config) {
  // Do something before request is sent
  const token = localStorage.getItem('token'); // Fetch the token from local storage
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, function (error) {
  // Do something with request error
  return Promise.reject(error);
});

// Add a response interceptor
http.interceptors.response.use(function (response) {
  // Any status code that lie within the range of 2xx cause this function to trigger
  // Do something with response data
  return response;
}, function (error) {
  // Any status codes that falls outside the range of 2xx cause this function to trigger
  // Do something with response error
  if (error.response && error.response.status === 769) {
    // Handle invalid session
    localStorage.removeItem('token'); // Remove the invalid token
    window.location.href = '/login'; // Redirect to login page
  }
  return Promise.reject(error);
});

export default http;