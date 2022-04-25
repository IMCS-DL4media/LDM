import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore';
import utils from '../../utils/utils'

export default {
    name: "TopBarRightSide",
    mixins: [mymixin, utils],

    mounted: function() {
        let self = this;

        self.runId = self.$route.params['run_id'];
        self.projectId = self.$route.params['project_id'];
    },

    data: function() {
        return {runId: "",
                projectId: "",
                user: this.getUsername(),
            };
    },

    methods: {

        logout(ev) {
            let self = this;

            axios.get(this.SERVER_URL() + "logout", self.getHeader())
                    .then(response => {

                        if (self.noErrorsInResponse(response)) {

                            self.$session.destroy();
                            localStorage.clear();

                            self.$router.push('/');
                        }
                    });
        },

    }
}