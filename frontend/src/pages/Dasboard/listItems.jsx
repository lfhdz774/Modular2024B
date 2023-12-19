import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import PeopleIcon from '@mui/icons-material/People';
import BarChartIcon from '@mui/icons-material/BarChart';
import LayersIcon from '@mui/icons-material/Layers';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { Box } from '@mui/material';
import { useNavigate , Link } from 'react-router-dom';
import { logout } from 'src/Services/login.service';
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

       
    </React.Fragment>
);

export const UserManagement = () => {

    const navigate = useNavigate ();
    const handleLogout = () => {
        logout();
        navigate('/login');
    };
    return (
        <Box sx={{ position: "absolute", bottom: 0, width: "100%" }}>
            <ListItemButton onClick={handleLogout}>
                <ListItemIcon>
                    <ExitToAppIcon />
                </ListItemIcon>
                <ListItemText primary="Cerrar sesión" />
            </ListItemButton>
        </Box>
    );
};
