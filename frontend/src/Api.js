import axios from 'axios';

class NuagecronApi {
    constructor(baseUrl) {
        this.api = axios.create({
            baseURL: baseUrl,
            timeout: 1000,
            headers: {"Access-Control-Allow-Origin": "*"}
          });
    }

    async getSchedules(start_key = null) {
        console.log('Call to schedules was made')
        return this.api.get('/schedules', start_key ? { params: {start_key: start_key}} : null)
    }
}

export default NuagecronApi