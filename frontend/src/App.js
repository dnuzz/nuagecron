import './App.css';
import { ScheduleTable } from './views/ScheduleTable'
import { ScheduleView } from './views/ScheduleView'
import { ThemeProvider, createTheme } from '@mui/material';
import NuagecronApi from './Api';
import {
  createBrowserRouter,
  RouterProvider,
  Route,
  Outlet,
  createRoutesFromElements,
} from "react-router-dom";
import ErrorPage from './views/ErrorPage'
import LoginButton from './components/LoginButton';
import LogoutButton from './components/LogoutButton';
import Profile from './components/Profile';
import { useAuth0 } from '@auth0/auth0-react';
import { Auth0ProviderWithNavigate } from './auth0-with-navigate';

export const api = new NuagecronApi('/api')
const defaultMaterialTheme = createTheme({palette: {
  mode: 'light',
}});


export const router = createBrowserRouter(
  createRoutesFromElements(
    <Route element={<Auth0ProviderWithNavigate />} errorElement={<ErrorPage/>}>
        <Route element={<Layout />}>
          <Route path="/" element={<ScheduleTable api={api}/>} />
          <Route path="/schedule/:schedule_id" element={<ScheduleView api={api}/>} />
        </Route>
    </Route>
));

function Layout() {

  const { isAuthenticated } = useAuth0()

  let button;
  if (isAuthenticated) {
    button = <LogoutButton/>;
  } else {
    button = <LoginButton/>
  }

  return <div>
    <Profile/>
    {button}
    <Outlet />
  </div>
}

export default function App() {
  
  return (
  <div className="App" style={{ maxWidth: "100%" }}>
    <ThemeProvider theme={defaultMaterialTheme}>
      <RouterProvider router={router} />
    </ThemeProvider>
  </div>
  );
}
