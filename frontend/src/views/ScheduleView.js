import React, { useState, useEffect } from 'react'
import { Form } from 'react-router-dom'
import { useLoaderData } from 'react-router-dom'

export const ScheduleView = () => {

    const schedule = useLoaderData().data

    return (
    <div id="schedule">

    <div>
      <h1>
        Schedule: {schedule.name}<br/>
        Project Stack: {schedule.project_stack}
      </h1>
      <div>
        {Object.keys(schedule).map(key => <div>{key}: {JSON.stringify(schedule[key])}</div>)}
      </div>

      <div>
        <Form action="Invoke">
          <button type="submit">Invoke</button>
        </Form>
        <Form
          method="post"
          action="Reset"
        >
          <button type="submit">Reset</button>
        </Form>
      </div>
    </div>
  </div>)
}