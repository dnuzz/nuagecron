import MaterialTable from 'material-table'
import React, { useState, useEffect } from 'react'
import { Form, Link } from 'react-router-dom'
import { useParams } from 'react-router-dom'
import { ExecutionsTable } from './ExecutionsTable'
import { Button } from '@mui/material'

const cleanData = (a_dict) => {
    for (const [key, value] of Object.entries(a_dict)){
      if (value instanceof Object && value !== null){
        a_dict[key] = JSON.stringify(value)
      }
    }
  return a_dict
}

export const ScheduleView = ({ api }) => {

    let { schedule_id } = useParams()

    const [scheduleData, setScheduleData] = useState({name: '', project_stack: '', schedule_id: schedule_id})

    useEffect(() => {
      const getData = async () => {
        const new_data = await api.getSchedule(schedule_id)
        setScheduleData(cleanData(new_data))
      }
      getData()
    }, []
    )

    return (
    <div id="schedule">
      <Link to="/"><Button>Back</Button></Link>
    <div>
      <h1>
        Schedule: {scheduleData.name}<br/>
        Project Stack: {scheduleData.project_stack}
      </h1>
      <div>
        {Object.keys(scheduleData).map(key => <div>{key}: {JSON.stringify(scheduleData[key])}</div>)}
      </div>

      <div>
        <Form action="Invoke" method="post">
          <Button type="submit">Invoke</Button>
        </Form>
        <Form
          method="post"
          action="Reset"
        >
          <Button type="submit">Reset</Button>
        </Form>
      </div>
      <ExecutionsTable api={api} schedule_id={scheduleData.schedule_id} />
    </div>
  </div>)
}