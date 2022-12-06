import MaterialTable from "material-table";
import React, { useState, useEffect } from 'react'

const getKeys = (a_dict) => {
  var retval = []
  for (const [key, value] of Object.entries(a_dict)) {
    retval.push({title: key, field: key})
  }
  return retval
};

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

export const ScheduleTable = (api) => {

  const init_columns = [
    {
      title: "name",
      field: "name",
    },
    {
      title: "enabled",
      field: "enabled",
    },
    {
      title: "cron",
      field: "cron",
    },
    {
      title: "next_run",
      field: "next_run",
    },
  ]

  const [rows, setRows] = useState([])
  const [columns, setColumns] = useState(init_columns)

  useEffect(() => {
    const getData = async () => {
      const new_data = await api.api.getSchedules()
      setColumns(getKeys(new_data.data[0]))
      setRows(cleanData(new_data.data))
    }
    getData()
  }, []
  )



  
return (
  <MaterialTable title="Schedules" data={JSON.parse(JSON.stringify(rows))} columns={columns} />
);
};