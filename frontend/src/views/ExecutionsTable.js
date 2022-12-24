import MaterialTable from "material-table";
import React, { useState, useEffect } from 'react'
import { Link } from "react-router-dom";

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

export const ExecutionsTable = ({api , schedule_id }) => {


  const columns = [
    {
      title: "Execution Time",
      field: "execution_time",
    },
    {
      title: "Execution Id",
      field: "execution_id",
    },
    {
      title: "Status",
      field: "status",
    },
    {
      title: "Logs",
      field: "log_link",
    },
    {
      title: "Executor",
      field: "executor",
    },
    {
      title: "Payload",
      field: "payload",
    }
  ]

  const [rows, setRows] = useState([{}])

  useEffect(() => {
    const getData = async () => {
      const new_data = await api.getExecutions(schedule_id)
      setRows(cleanData(new_data.data))
    }
    getData()
  }, []
  )



  
return (
  <MaterialTable 
    title="Executions" 
    data={JSON.parse(JSON.stringify(rows))} 
    columns={columns} 
    />
);
};