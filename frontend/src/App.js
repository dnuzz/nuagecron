import logo from './logo.svg';
import './App.css';
import { ScheduleTable } from './schedules/ScheduleTable'
import { ThemeProvider, createTheme } from '@mui/material';
import NuagecronApi from './Api';

const api = new NuagecronApi('http://localhost:5000')

function App() {
  const defaultMaterialTheme = createTheme();
  return (
    <div className="App" style={{ maxWidth: "100%" }}>
      <ThemeProvider theme={defaultMaterialTheme}>
    <ScheduleTable api={new NuagecronApi('http://localhost:5000')}/>
    </ThemeProvider>
  </div>
  );
}

export default App;
