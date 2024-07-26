import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { Box } from '@mui/material';
import { useNavigate, Link } from 'react-router-dom';
import { logout } from 'src/Services/login.service';
import ProtectedMenu from './ProtectedMenu';


export const MainListItems = () => {
    
    const navigate = useNavigate();



    return (
        <React.Fragment>

                <ListItemButton  onClick={() => navigate('/home')}>
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

            <ProtectedMenu allowedRoles={[7]}>
                    <ListItemButton onClick={() => navigate('/user-creation')}>
                        <ListItemIcon>
                            <SupervisorAccountIcon />
                        </ListItemIcon>
                        <ListItemText primary="Crear usuario" />
                    </ListItemButton>
            </ProtectedMenu>



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
