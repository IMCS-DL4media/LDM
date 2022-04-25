
// window.axios = require("axios");
import axios from './utils/axios'
window.axios = axios;

export default {

  computed: {
    layout() {
    	const default_layout = "default";
    	return (this.$route.meta.layout || default_layout) + "-layout";
    }
  },

}

