import Vue from 'vue'
import App from './App.vue'
import router from "./router"

import underscore from 'vue-underscore'
import VueMoment from 'vue-moment'
import VueSession from 'vue-session'
import { TooltipPlugin, BootstrapVue } from 'bootstrap-vue'
import VueProgressBar from 'vue-progressbar'

import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'

import utils from './utils/utils.js'

import Default from "./layouts/Default.vue"
import NoBars from "./layouts/NoBars.vue"
import NoSideBar from "./layouts/NoSideBar.vue"

import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'



import VueMixpanel from 'vue-mixpanel'

window.$ = require('jquery');


import 'startbootstrap-sb-admin-2/vendor/bootstrap/js/bootstrap.bundle.min.js'
import 'startbootstrap-sb-admin-2/vendor/jquery-easing/jquery.easing.min.js'
// import 'startbootstrap-sb-admin-2/js/sb-admin-2.min.js'

import 'startbootstrap-sb-admin-2/css/sb-admin-2.min.css'

Vue.config.productionTip = false
Vue.use(underscore);
Vue.use(VueSession);
Vue.use(VueMoment);
Vue.use(Chartkick.use(Chart));

Vue.use(TooltipPlugin);
Vue.use(BootstrapVue);

Vue.component('vue-bootstrap-typeahead', VueBootstrapTypeahead)

const options = {
  // color: '#bffaf3',
  color: "#224abe",
  failedColor: '#874b4b',
  thickness: '5px',
  transition: {
    speed: '0.2s',
    opacity: '0.6s',
    termination: 300
  },
  autoRevert: true,
  // location: 'top',
  inverse: false
}

Vue.use(VueProgressBar, options)
Vue.component("default-layout", Default);
Vue.component("no-bars-layout", NoBars);
Vue.component("no-side-bar-layout", NoSideBar);


Vue.use(VueMixpanel, {
  token: "ac387084f654ee57da8752bdc6d2c0f8"
})


router.beforeEach((to, from, next) => {
	if (to.matched.some(record => record.meta.requiresAuth)) {
		let token = utils.methods.getToken();
	    if (!token) {
	        next({name: "NotLoggedIn"});
		} 
		else {
			next();
		}
	}

	else {
		next();
	}

});


const vue = new Vue({
	router,
	render: h => h(App),
}).$mount('#app')

window.Vue = vue;


export default vue