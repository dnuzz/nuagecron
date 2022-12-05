import MaterialTable from "material-table";
import React, { useState, useEffect } from 'react'

const getKeys = (a_dict) => {
  var retval = []
  for (const [key, value] of Object.entries(a_dict)) {
    retval.push({title: key, field: key})
  }
  return retval
};


export const ScheduleTable = (api) => {

  const initialState = {
    data: [{}],
    loading: true,
    columns: [{}]
  }

  const [state, setState] = useState(initialState)

  useEffect(() => {
    const getData = async () => {
      return api.api.getSchedules()
    }

    getData().then(resp => setState((state) => ({
      ...state,
      data: resp.data
     })))
  }
  )

  const columns = [
    {
      title: "Name",
      field: "name",
    },
    {
      title: "Email",
      field: "email",
    },
    {
      title: "Age",
      field: "age",
    },
    {
      title: "Gender",
      field: "gender",
    },
  ]

  
return (
  <MaterialTable title="Employee Details" data={state.data} columns={state.columns} />
);
};