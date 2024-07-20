import React from 'react';
import { Navigate } from 'react-router-dom';
import { getUserRoles } from 'src/Services/Helper.service';

const ProtectedRoute = ({ allowedRoles, children }) => {
  const userRoles = getUserRoles(); 
    console.log(userRoles)
  const hasRequiredRole = allowedRoles.some((role) => userRoles === role);

  if (!hasRequiredRole) {
    return <Navigate to="/unauthorized" replace />; 
  }

  return children;
};

export default ProtectedRoute;