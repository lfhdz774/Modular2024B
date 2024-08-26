import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { GetUserRoles } from 'src/Services/user.service';

const ProtectedRoute = ({ allowedRoles, children }) => {
  const [userRoles, setUserRoles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
	const fetchUserRoles = async () => {
	  try {
		const roles = await GetUserRoles();
		setUserRoles(roles);
	  } catch (error) {
		console.error('Failed to fetch user roles:', error);
	  } finally {
		setIsLoading(false);
	  }
	};

	fetchUserRoles();
  }, []);

  if (isLoading) {
	return <div>Loading...</div>; // You can replace this with a proper loading indicator
  }

  const hasRequiredRole = allowedRoles.some((role) => userRoles.includes(role));
  if (!hasRequiredRole) {
	return <Navigate to="/unauthorized" replace />;
  }

  return children;
};

export default ProtectedRoute;