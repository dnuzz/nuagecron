import './App.css';
import { ScheduleTable } from './views/ScheduleTable'
import { ScheduleView } from './views/ScheduleView'
import { ThemeProvider, createTheme } from '@mui/material';
import { Button } from "@mui/material";
import NuagecronApi from './Api';
import {
  createBrowserRouter,
  RouterProvider,
  Route,
  Outlet,
  createRoutesFromElements,
} from "react-router-dom";
import ErrorPage from './views/ErrorPage'
import Profile from './components/Profile';
import { OAuthProviderWithNavigate } from './Authentication';
import { AuthContext } from 'react-oauth2-code-pkce'
import { useContext } from 'react';

export const api = new NuagecronApi('/api')
const defaultMaterialTheme = createTheme({
  palette: {
    mode: 'light',
  }
});


export const router = createBrowserRouter(
  createRoutesFromElements(
    <Route element={<OAuthProviderWithNavigate />} errorElement={<ErrorPage />}>
      <Route element={<Layout />}>
        <Route path="/" element={<ScheduleTable api={api} />} />
        <Route path="/schedule/:schedule_id" element={<ScheduleView api={api} />} />
      </Route>
    </Route>
  ));

function Layout() {

  const { token, login, logOut } = useContext(AuthContext)

  let button;
  let outlet;
  if (token) {
    button = <Button onClick={() => logOut()}>
      Log Out
    </Button>;
    outlet = <Outlet />;
  } else {
    button = <Button onClick={() => login()}>
      Login
    </Button>
    outlet = <div />
  }

  return <div>
    <Profile />
    {button}
    {outlet}
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
