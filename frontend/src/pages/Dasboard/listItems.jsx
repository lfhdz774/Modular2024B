import React, { useState, useEffect } from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import PersonSearchIcon from '@mui/icons-material/PersonSearch';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import AutoModeIcon from '@mui/icons-material/AutoMode';
import { Box } from '@mui/material';
import { useNavigate, Link } from 'react-router-dom';
import { logout } from 'src/Services/login.service';
import ProtectedMenu from './ProtectedMenu';
import { GetUserRoles } from 'src/Services/user.service';
import Divider from '@mui/material/Divider';
import DnsIcon from '@mui/icons-material/Dns';
import LockPersonIcon from '@mui/icons-material/LockPerson';


export const MainListItems = () => {


    const [userRoles, setUserRoles] = useState([0]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchUserRoles = async () => {
            const roles = await GetUserRoles();
            console.log("roles", roles);
            setUserRoles(roles);
            setIsLoading(false);
        };

        fetchUserRoles();
    }, []);

    const navigate = useNavigate();



    return (
        <React.Fragment>

            <ListItemButton onClick={() => navigate('/home')}>
                <ListItemIcon>
                    <DashboardIcon />
                </ListItemIcon>
                <ListItemText primary="Inicio" />
            </ListItemButton>

            <ListItemButton onClick={() => navigate('/reports')}>
                <ListItemIcon >
                    <ShoppingCartIcon />
                </ListItemIcon>
                <ListItemText primary="Reportes" />
            </ListItemButton>

            <ProtectedMenu allowedRoles={[7]} userRole={userRoles}>
                <ListItemButton onClick={() => navigate('/user-creation')}>
                    <ListItemIcon>
                        <SupervisorAccountIcon />
                    </ListItemIcon>
                    <ListItemText primary="Crear usuario" />
                </ListItemButton>
            </ProtectedMenu>

            <Divider sx={{ my: 1 }} />

            <ProtectedMenu allowedRoles={[7]} userRole={userRoles}>
                <ListItemButton onClick={() => navigate('/user-credential-creation')}>
                    <ListItemIcon>
                        <PersonAddIcon />
                    </ListItemIcon>
                    <ListItemText primary="Crear credencial" />
                </ListItemButton>
            </ProtectedMenu>

            <ProtectedMenu allowedRoles={[7]} userRole={userRoles}>
                <ListItemButton onClick={() => navigate('/user-credential-management')}>
                    <ListItemIcon>
                        <PersonSearchIcon />
                    </ListItemIcon>
                    <ListItemText primary="Administrar credenciales" />
                </ListItemButton>
            </ProtectedMenu>

            <ProtectedMenu allowedRoles={[7]} userRole={userRoles}>
                <ListItemButton onClick={() => navigate('/server-creation')}>
                    <ListItemIcon>
                        <DnsIcon />
                    </ListItemIcon>
                    <ListItemText primary="Registrar servidores" />
                </ListItemButton>
            </ProtectedMenu>

            <ProtectedMenu allowedRoles={[7]} userRole={userRoles}>
            <ListItemButton onClick={() => navigate('/server-management')}>
                    <ListItemIcon>
                        <LockPersonIcon />
                    </ListItemIcon>
                    <ListItemText primary="Administrar servidores" />
                </ListItemButton>
            </ProtectedMenu>

            <Divider sx={{ my: 1 }} />

            <ListItemButton onClick={() => navigate('/commands')}>
                <ListItemIcon >
                    <AutoModeIcon />
                </ListItemIcon>
                <ListItemText primary="Comandos IA" />
            </ListItemButton>

        </React.Fragment>
    );
}

export const UserManagement = () => {

    const navigate = useNavigate();
    const handleLogout = () => {
        logout();
        navigate('/login');
    };
    return (
        <>
            <Box sx={{ display: "flex", flexDirection: "column", height: "100%", alignItems: "flex-end" }}>
                <Box sx={{ width: "100%", maxHeight: "50px", flexGrow: 1, alignSelf: "flex-end", marginTop: "auto" }}>
                    <ListItemButton onClick={() => navigate('/user')}>
                        <ListItemIcon>
                            <AccountCircleIcon />
                        </ListItemIcon>
                        <ListItemText primary="Administrar Usuario" />
                    </ListItemButton>
                </Box>
                <Box sx={{ width: "100%", maxHeight: "50px", flexGrow: 1, alignSelf: "flex-end" }}>
                    <ListItemButton onClick={handleLogout}>
                        <ListItemIcon>
                            <ExitToAppIcon />
                        </ListItemIcon>
                        <ListItemText primary="Cerrar sesión" />
                    </ListItemButton>
                </Box>
            </Box>
        </>
    );
};
