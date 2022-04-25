import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],

    mounted: function() {
        var self = this;

        self.projectId = self.$route.params['project_id'];
        self.getProjectRuns();
    },

    watch: {
        $route (to, from) {
            this.projectId = to.params.project_id || "";
            this.getProjectRuns();
        },
    },

    data: function() {
        return {
            projectId: "",
            project: {settings:
                        {datasets: [
                            {name: "ImageClassificationTrainingData"},
                        ],
                    }
                },
            loading: false,
            activeRun: {},
            runs: [],
            error: null,
        }
    },

    methods: {            

        getProjectRuns() {
            let self = this;

            axios.get(self.SERVER_URL() + 'runs/' + self.projectId)
                    .then(function(response) {

                        console.log("response ", response)

                        if (response.status != 200) {
                            throw Error(response.statusText);
                        }

                        let data = response.data;

                        self.runs = _.map(data.runs, function(run) {
                                        _.extend(run, {_id: self.getId(run),
                                                        _short_comment: self.makeShortComment(run.comment),
                                                        _start_time: self.covnertTimeFromDateObject(run.start_time),
                                                    });

                                        if (run.finished) {
                                            _.extend(run, {_finish_time: self.covnertTimeFromDateObject(run.finish_time),});
                                        }

                                        return run;
                                    });

                        self.project = data.project;

                    })
                    .catch(error => {
                        self.processErrorInPromise(error)
                    });
        },


        makeShortComment: function(val) {
            if (_.isEmpty(val)) {
                return "";
            }

            return val.substr(0, 40) + "...";

        },

        editRun: function() {
            let self = this;

            let list = {runId: this.activeRun._id,
                        projectId: this.projectId,
                        comment: $("#edit-comment-field").val(),
                    };

            axios.put(this.SERVER_URL() + 'run/' + this.projectId + '/' + this.runId, list)
                    .then(function(response) {      
                        if (response.status != 200) {
                            console.error("Error", response);
                            return;
                        }

                        _.extend(self.activeRun, {comment: list.comment,
                                                    _short_comment: self.makeShortComment(list.comment),
                                                });
                    })
                    .catch(error => {
                        self.processErrorInPromise(error)
                    });
        },

        deleteRun: function() {
            let self = this;
            console.log("delete run")

            let run_id = this.activeRun._id;

            axios.delete(this.SERVER_URL() + 'run/' + this.projectId + '/' + run_id)
                    .then(function(response) {      

                        if (response.status != 200) {
                            console.error("Error", response);
                            return;
                        }

                        self.runs = _.reject(self.runs, function(run) {
                                        return run._id == run_id;
                                    });
                    })
                    .catch(error => {
                        self.processErrorInPromise(error)
                    }); 

        },

        setActiveRun: function(run_id) {
            this.activeRun = _.find(this.runs, function(run) {
                                return run._id == run_id;
                            });
        },

        deleteProject: function() {
            let self = this;

            axios.delete(self.SERVER_URL() + 'project/' + self.projectId)
                    .then(function(response) { 
                        self.$router.push({name: 'Projects'});
                    })
                    .catch(error => {
                        self.processErrorInPromise(error)
                    });
        },

    },
}