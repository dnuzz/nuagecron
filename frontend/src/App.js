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

export const api = new NuagecronApi('http://localhost:5000')
const defaultMaterialTheme = createTheme();

const get_schedules = () => {
  return api.getSchedules()
}

const get_schedule = ({ params }) => {
  console.log(params)
  return api.getSchedule(params.name, params.project_stack)
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <ScheduleTable api={api}/>,
    errorElement: <ErrorPage />,
    loader: get_schedules
  },
  {
    path: "/schedule/:name/:project_stack",
    element: <ScheduleView />,
    errorElement: <ErrorPage />,
    loader: get_schedule
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
