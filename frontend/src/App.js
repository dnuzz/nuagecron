import logo from './logo.svg';
import './App.css';
import { ScheduleTable } from './schedules/ScheduleTable'
import { ThemeProvider, createTheme } from '@mui/material';
import NuagecronApi from './Api';

const api = new NuagecronApi('http://localhost:5000')
const defaultMaterialTheme = createTheme();

function App() {
  
  return (
    <div className="App" style={{ maxWidth: "100%" }}>
      <ThemeProvider theme={defaultMaterialTheme}>
    <ScheduleTable api={api}/>
    </ThemeProvider>
  </div>
  );
}

export default App;
