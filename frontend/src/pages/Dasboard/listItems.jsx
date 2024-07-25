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
export const mainListItems = (
    <React.Fragment>



        <Link to="/home">
            <ListItemButton>
                <ListItemIcon>
                    <DashboardIcon />
                </ListItemIcon>
                <ListItemText primary="Home" />
            </ListItemButton>
        </Link>

        <Link to="/reports">
            <ListItemButton>
                <ListItemIcon>
                    <ShoppingCartIcon />
                </ListItemIcon>
                <ListItemText primary="Reports" />
            </ListItemButton>
        </Link>

        <ProtectedMenu allowedRoles={[7]}>
            <Link to="/user-creation">
                <ListItemButton>
                    <ListItemIcon>
                        <SupervisorAccountIcon />
                    </ListItemIcon>
                    <ListItemText primary="User creation" />
                </ListItemButton>
            </Link>
        </ProtectedMenu>
       


    </React.Fragment>
);

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
