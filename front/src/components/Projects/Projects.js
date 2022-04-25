import { mymixin } from '../../mixins/mixins.js'

import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],
    mounted: function() {
    	var self = this;

        axios.get(this.SERVER_URL() + 'projects')
	            .then(function(response) {

		            if (response.status != 200) {
		                throw Error(response.statusText);
		            }

		            console.log("response.data ", response.data)


		            self.projects = _.map(response.data.projects, function(project) {
		            					_.extend(project, {_created_at: self.covnertTimeFromDateObject(project.created_at),});
		            					return project;
		            				});
		        })
	            .catch(error => {
	                self.processErrorInPromise(error)
	            }); 
    },

    data: function() {
        return {
            projects: [],
        };
    },

	methods: {
		createNewProjectClicked: function() {
			var self = this;

			$('#alerts_success').hide();
			$('#alerts_fail').hide();

			var list = {name: $("#project_name_id").val(),
						type: $("#project-type option:selected").attr("value"),
						description: $("#project_description_id").val(),
					};

            axios.post(this.SERVER_URL() + "project", list)
					.then(response => {	

						if (response.status != 200) {
							$('#alerts_fail').show();
							return;
						}

						$('#alerts_success').show();

						let project = response.data.data;
						_.extend(project, {_created_at: self.covnertTimeFromDateObject(project.created_at),});

						self.projects = _.union(self.projects, [project]);
					},
					response => {						
						console.log(response.body)				
						$('#alerts_fail').show();
					});
		},
	}
};
