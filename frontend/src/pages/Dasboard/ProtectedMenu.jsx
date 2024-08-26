import React, { useEffect, useState } from 'react';
import { GetUserRoles } from 'src/Services/user.service';

const ProtectedMenu = ({ allowedRoles, children }) => {
    const [hasAccess, setHasAccess] = useState(false);
    const [userRoles, setUserRoles] = useState([0]);

    useEffect(() => {
        const fetchUserRoles = async () => {
            const roles = await GetUserRoles();
            console.log("roles", roles);
            setUserRoles(roles);
        };

        fetchUserRoles();
    }, []);

    useEffect(() => {
        const checkAccess = async () => {
            try {
                if (userRoles === undefined) {
                    return;
                }
                const roles = userRoles
                console.log(roles, allowedRoles);
                console.log(allowedRoles)
                const hasAllowedRole = roles.some(role => allowedRoles.includes(role));
                console.log(hasAllowedRole)
                setHasAccess(hasAllowedRole);
            } catch (error) {
                console.error("Failed to fetch user roles:", error);
            } 
        };

        checkAccess();
    }, [allowedRoles]);


    return hasAccess ? children : null;
};

export default ProtectedMenu;
