import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { GetUserRoles } from 'src/Services/user.service';

const ProtectedRoute = ({ allowedRoles, children }) => {
  const [userRoles, setUserRoles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchUserRoles = async () => {
      const roles = await GetUserRoles();
      console.log(roles);
      setUserRoles(roles);
      setIsLoading(false);
    };

    fetchUserRoles();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const hasRequiredRole = allowedRoles.some((role) => userRoles.includes(role));

  if (!hasRequiredRole) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
};

export default ProtectedRoute;
