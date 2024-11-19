import axios from 'axios';

const http = axios.create({
  baseURL: process.env.REACT_APP_ENV === 'DEVELOPMENT' ?   process.env.REACT_APP_BACKEND_URL_LOCAL : process.env.REACT_APP_BACKEND_URL_PROD , //'http://ec2-18-223-101-59.us-east-2.compute.amazonaws.com:5000',
  timeout: 10000,
});

console.log('process.env.REACT_APP_ENV', process.env.REACT_APP_ENV);

// Add a request interceptor
http.interceptors.request.use(function (config) {
  // Do something before request is sent
  const token = localStorage.getItem('token'); // Fetch the token from local storage
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.withCredentials = true; // Send cookies when cross-domain requests
  config.headers['access-control-allow-origin'] = '*'; // Allow cross-origin requests
  return config;
}, function (error) {
  // Do something with request error
  console.error(error);
  return Promise.reject(error);
});

// Add a response interceptor
http.interceptors.response.use(function (response) {

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