import axios from 'axios';

class NuagecronApi {
    constructor(baseUrl) {
        this.api = axios.create({
            baseURL: baseUrl,
            timeout: 1000,
            headers: {"Access-Control-Allow-Origin": "*"}
          });

        this.schedule_map = new Map()
        this.executions_map_map = new Map()
    }

    async getSchedules(start_key = null) {
        console.log('Call to schedules was made')
        const retrieved_schedules = await this.api.get('/schedules', start_key ? { params: {start_key: start_key}} : null)
        for (const schedule of retrieved_schedules.data) {
            this.schedule_map.set(schedule.schedule_id, schedule)
        }
        return retrieved_schedules.data
    }

    async getSchedule(schedule_id) {
        
        if (!this.schedule_map.has(schedule_id)){
            console.log('Call to schedule was made')
            const schedule = await this.api.get(`/schedule/${schedule_id}`)
            this.schedule_map.set(schedule_id, schedule.data)
        }
        return this.schedule_map.get(schedule_id)
    }

    async getExecutions(schedule_id) {
        if (!this.executions_map_map.has(schedule_id)){
            console.log('Call to executions was made')
            const executions_for_schedule = await this.api.get(`/executions/${schedule_id}`)
            this.executions_map_map.set(schedule_id, executions_for_schedule.data)
        }
        return this.executions_map_map.get(schedule_id)
    }
}

export default NuagecronApi