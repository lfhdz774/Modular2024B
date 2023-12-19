
import { Router } from 'react-router-dom';
import RouterComponent from './components/Router';
import ThemeProvider from 'src/theme';

// ----------------------------------------------------------------------

export default function App() {

  return (
    <ThemeProvider>
        <RouterComponent />
    </ThemeProvider>
  );
}