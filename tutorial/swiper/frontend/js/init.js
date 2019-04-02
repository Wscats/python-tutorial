axios.defaults.withCredentials = true;

const request = axios.create({
    baseURL: 'http://127.0.0.1:9000/',
    headers:{
        "Access-Control-Allow-Headers":"Origin, X-Requested-With, Content-Type, Accept",
        'Content-Type':'application/x-www-form-urlencoded',
        "Access-Control-Allow-Credentials": true,
        "Access-Control-Allow-Origin": "http://127.0.0.1:8000",
        "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE,OPTIONS",
    },
    transformRequest: [function (data) {
        data = Qs.stringify(data);
        return data;
    }]
});
