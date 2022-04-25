import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore';
import utils from '../../utils/utils'

export default {
    name: "TopBarLeftSide",
    mixins: [mymixin, utils],

    mounted: function() {
        let self = this;

        self.runId = self.$route.params['run_id'];
        self.projectId = self.$route.params['project_id'];

        self.getProjects();
    },

    data: function() {
        return {runId: "",
                projectId: "",
                projects: [],
            };
    },

    methods: {
        getProjects() {
            let self = this;

            axios.get(self.SERVER_URL() + 'projects')
                    .then(function(response) {

                        if (response.status != 200) {
                            throw Error(response.statusText);
                        }

                        console.log("response.data ", response.data)

                        self.projects = _.map(response.data.projects, function(project) {
                                            _.extend(project, {_created_at: self.covnertTimeFromDateObject(project.created_at),});
                                            return project;
                                        });


                        self.projects = _.first(self.projects, 5);
                    })
                    .catch(error => {
                        self.processErrorInPromise(error)
                    }); 
        },
    }
}