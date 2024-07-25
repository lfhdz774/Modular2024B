import React, { useEffect, useState } from 'react';
import { GetUserRoles } from 'src/Services/user.service';

const ProtectedMenu = ({ allowedRoles, children }) => {
    const [hasAccess, setHasAccess] = useState(false);

    useEffect(() => {
        const checkAccess = async () => {
            try {
                const roles = await GetUserRoles();
                console.log(roles, allowedRoles);
                const hasAllowedRole = roles.some(role => allowedRoles.includes(role));
                console.log(hasAllowedRole);
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
