import MaterialTable from "material-table";
import React, { useState, useEffect } from 'react'
import { Link } from "react-router-dom";
import { useLoaderData } from "react-router-dom";

const cleanData = (dicts) => {
  for (const a_dict of dicts) {
    for (const [key, value] of Object.entries(a_dict)){
      if (value instanceof Object && value !== null){
        a_dict[key] = JSON.stringify(value)
      }
    }
  }
  return dicts
}

export const ScheduleTable = ({ api }) => {

  const columns = [
    {
      title: "Name",
      field: "name",
    },
    {
      title: "Project Stack",
      field: "project_stack",
    },
    {
      title: "Cron",
      field: "cron",
    },
    {
      title: "Next Run",
      field: "next_run",
    },
    {
      title: "Executor",
      field: "executor",
    },
    {
      title: "Concurrency",
      field: "concurrent_runs",
    },
    {
      title: "History",
      field: "execution_history",
    },
    {
      title: "Default Settings",
      field: "original_settings",
    },
    {
      title: "Enabled",
      field: "enabled",
    }
  ]

  const [rows, setRows] = useState([{}])

  useEffect(() => {
    const getData = async () => {
      const new_data = await api.getSchedules()
      setRows(cleanData(new_data))
    }
    getData()
  }, []
  )



  
return (
  <MaterialTable 
    title="Schedules" 
    data={JSON.parse(JSON.stringify(rows))} 
    columns={columns} 
    actions={[
      rowData => ({
        icon: () => <Link to={`/schedule/${rowData.schedule_id}`}>View</Link>,
        tooltip: 'View Details',
        onClick: (rowData)
      })
    ]}/>
);
};