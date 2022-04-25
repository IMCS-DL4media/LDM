import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore';
import utils from '../../utils/utils'
    
export default {
    mixins:[mymixin, utils],
    methods: {            

        register: function(ev) {
            var self = this;

            var password1 = $("#password").val();
            var password2 = $("#password2").val();

            if (password1 != password2) {                
                // error msg needed
                console.error("Password1 and password2 do not mathc");
                return;
            }

            var list = {email: $("#email").val(),
                        password: password1,
                    };

            axios.post(this.SERVER_URL() + "register", list, self.getHeader())
                    .then(response => {

                        console.log("resp ", response)

                        if (self.noErrorsInResponse(response)) {
                            self.$router.push('/');
                        }
                    });
        },

    }
}
