import { mymixin } from '../../mixins/mixins.js'
import utils from '../../utils/utils'
    
export default {
    mixins:[mymixin, utils],

    mounted: function() {
        let self = this;

        axios.get(self.SERVER_URL() + 'user-profile')
                .then(function(response) {
                    self.token = response.data.token;
                })
                .catch(error => {
                    self.processErrorInPromise(error)
                });
    },

    data: function() {
        return {
            token: "",
        }
    },

    methods: {            
        changePassword: function() {
            let self = this;

            let password1 = $("#password").val();
            let password2 = $("#password2").val();
            let password3 = $("#password3").val();

            // need a msg
            if (password2 != password3) {
                self.addNotification("The new password and the repeated password do not match!", "error");
                console.error("Passwords do not match");
                return;
            }

            let list = {userName: self.getUsername() + "adfa",
                        oldPassword: $("#password").val(),
                        newPassword: $("#password2").val(),
                    };

            axios.post(this.SERVER_URL() + "Login/ChangePassword", list)
                    .then(response => {

                        console.log("resp ", response)

                        if (self.noErrorsInResponse(response)) {
                            self.addNotification("The password has been successfully changed!");
                        }

                    });
        },

        reloadToken() {
            let self = this;

            axios.put(self.SERVER_URL() + 'user-token', {})
                    .then(function(response) {
                        self.token = response.data.token;
                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

    }
}