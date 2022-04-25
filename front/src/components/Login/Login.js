import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],
    mounted(){
        $("#email").focus();
    },

    methods: {

        login(ev) {
            var self = this;

            var backend = this.SERVER_URL();
            var email = $("#email").val();
            var password = $("#password").val();

            // if (!this.$session.exists()) {
            axios.post(backend + "login", {"email": email, "password": password})
                .then(response => {

                    // TODO: error message should appear on the front page!
                    if (self.noErrorsInResponse(response)) {

                        var token = response.data.response.token;
 
                        localStorage.setItem("token", token);
                        localStorage.setItem("user", email);
                        localStorage.setItem("activeProject", "{}");

                        // self.$router.push('/projects');
                        self.$router.push({name: 'Projects'});
                    }
                })
                .catch(error => {
                    // TODO: show error on the front page
                    self.processErrorInPromise(error)
                });


            this.$mixpanel.track('Login event', {
                user: email,
                // property_1: 'value 1',
                // property_2: 'value 2',/
                // property_3: 'value 3'
            }); 


        },
    }
};
