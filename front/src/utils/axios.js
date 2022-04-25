import axios from 'axios';
import utils from "./utils"
import app from '../main';
import { _ } from 'vue-underscore'

const instance = axios.create();

instance.interceptors.request.use(config => {
	let header = utils.methods.getHeader();
	_.extend(config, header);

    app.$Progress.start(); // for every request start the progress

	return config;
});

instance.interceptors.response.use(response => {
    app.$Progress.finish(); // finish when a response is received
    return response;
});

export default instance;