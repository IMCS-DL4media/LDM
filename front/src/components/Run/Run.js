import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default{	 
    mixins: [mymixin, utils],

    mounted: function() {
        let self = this;

        self.runId = self.$route.params['run_id'];
        self.projectId = self.$route.params['project_id'];

        axios.get(self.SERVER_URL() + 'run/' + self.projectId + "/" + self.runId)
                .then(function(response) {

                    console.log("response ", response)

                    if (response.status != 200) {
                        throw Error(response.statusText);
                    }
                    
                    let run = response.data.run;
                    _.extend(run, {_id: self.getId(run),
                    				_start_time: self.covnertTimeFromDateObject(run.start_time),
                    			});

                    self.run = run;
                    self.logs = _.map(response.data.logs, function(log) {
                    				_.extend(log, {_id: self.getId(log),
		                    						_msg: JSON.stringify(log.body),
		                    						_time: self.covnertTimeFromDateObject(log.logged_on),
                    							});

                    				return log;
                   				});


                    console.log("self.logs ", self.logs)


                    self.project = response.data.project;
                    let link_names = {train: "Training data",
                    					validation: "Validation data",
                    					test: "Test data",
                					};


                    console.log("self.project ", self.project)


                    console.log("self.trainComponents ", self.trainComponents)
                    console.log("self.trainComponentsadsfa ", self.trainComponents[self.project.type])

                    self.project.settings.datasets = _.map(self.project.settings.datasets, function(dataset) {
                        								_.extend(dataset, {title: link_names[dataset.key],
                                                                            run: self.run,
                                                                            name: self.trainComponents[self.project.type][dataset.key],
                                                                        });

                        								return dataset;
                        							});

                    console.log("self.project.settings.datasets ", self.project.settings.datasets)

                    if (_.size(self.project.settings.datasets) > 0) {
                    	self.projectType = self.project.settings.datasets[0].name;
                    }

                })
                .catch(error => {
                    self.processErrorInPromise(error)
                });
    },

	data: function() {
		return {
			runId: "",
			projectId: "",
			project: {settings: {datasets: []}},
			loading: false,		
			run: {},
			logs: [],
			error: null,
			projectType: "",
		}
	},
	
	methods: {

		downloadFile(file_name) {
			console.log("in downloadFile")

			// console.log("ev ", ev)
			console.log("file ", file_name)


            let self = this;

            let header = self.getHeader(self);
            _.extend(header, {responseType: 'blob'});

            axios.get(self.SERVER_URL() + 'logged-file/' + self.projectId + '/' + self.runId + '?path=' + file_name, header)
                    .then(function(response) {

                        console.log("in response", response)

                        let fileURL = window.URL.createObjectURL(new Blob([response.data]));
                        let fileLink = document.createElement('a');

                        fileLink.href = fileURL;
                        fileLink.setAttribute('download', file_name);
                        document.body.appendChild(fileLink);

                        fileLink.click();
                    })
                   .catch(error => {
                        self.processErrorInPromise(error);
                    });
		}

	}		
};