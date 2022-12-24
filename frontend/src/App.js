import './App.css';
import { ScheduleTable } from './views/ScheduleTable'
import { ScheduleView } from './views/ScheduleView'
import { ThemeProvider, createTheme } from '@mui/material';
import NuagecronApi from './Api';
import {
  createBrowserRouter,
  RouterProvider,
  Route,
} from "react-router-dom";
import ErrorPage from './views/ErrorPage'

export const api = new NuagecronApi('api')
const defaultMaterialTheme = createTheme();

const get_schedules = () => {
  return api.getSchedules()
}

const get_schedule = ({ params }) => {
  console.log(params)
  return api.getSchedule(params.schedule_id)
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <ScheduleTable api={api}/>,
    errorElement: <ErrorPage />
  },
  {
    path: "/schedule/:schedule_id",
    element: <ScheduleView api={api}/>,
    errorElement: <ErrorPage />
  }
]);

export default function App() {
  
  return (
  <div className="App" style={{ maxWidth: "100%" }}>
    <ThemeProvider theme={defaultMaterialTheme}>
      <RouterProvider router={router} />
    </ThemeProvider>
  </div>
  );
}
