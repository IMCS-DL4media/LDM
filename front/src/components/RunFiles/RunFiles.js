import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default{
    mixins: [mymixin, utils],

    mounted: function() {
        let self = this;

        self.runId = self.$route.params['run_id'];
        self.projectId = self.$route.params['project_id'];
        self.pathMatch = self.$route.params['pathMatch'] || self.pathMatch;

        self.getData();
    },

    watch: {
        $route (to, from) {
            this.pathMatch = to.params['pathMatch'] || "";
            this.getData();
        },
    },

	data: function() {
		return {
			runId: "",
            projectId: "",
            pathMatch: "",				
			files: [],
            project: JSON.parse(localStorage.getItem("activeProject")),
            projectType: "",
		}
	},
	
	methods: {

        getData: function() {
            let self = this;

            let items = [];
            if (self.pathMatch) {
                items = self.pathMatch.split("/"); 
            }

            axios.get(self.SERVER_URL() + 'run-files/' + self.projectId + "/" + self.runId)
                    .then(function(response) {

                        console.log("response ", response.data)

                        if (response.status != 200) {
                            throw Error(response.statusText);
                        }

                        if (response.data.files) {
                            let source_tree_in = response.data.files.source_tree;
                            let source_tree = [];
                            if (source_tree_in) {
                                source_tree = self.find(JSON.parse(source_tree_in).children, items);
                            }

                            self.files = _.map(source_tree, function(file) {
                                             _.extend(file, {url: self.butildFileUrl(file)});
                                            return file;
                                        });
                        }

                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },


        butildFileUrl: function(file) {
            let self = this;

            let path = self.buildPath(file.name);
            if (file.type == "file") {
                return "/run-file/" + self.projectId + "/" + self.runId + "?path=" + path;
            }
            else {
                return self.buildInitialUrl() + "/" + path;
            }
        },

        buildPath: function(file_name) {
            let self = this;
            let path = file_name;
            if (self.pathMatch) {
                path = self.pathMatch + "/" + path; 
            }

            return path;
        },


        buildInitialUrl: function() {
            let self = this;
            return "/run-files/" + self.projectId + "/" + self.runId;
        },

        buildRootUrl: function() {
            let self = this;

            let path = self.buildInitialUrl();
            if (self.pathMatch) {
                path = path + "/" + self.pathMatch;
            }

            let url_splitted = path.split("/");
            return _.first(url_splitted, _.size(url_splitted) - 1).join("/");
        },


        find: function(source_tree, path_items) {
            if (_.size(source_tree) == 0 || _.size(path_items) == 0) {
                return _.sortBy(source_tree, "type");
            }
            else {
                let child = _.find(source_tree, function(child) {
                                return child.name == _.first(path_items);
                            });

                if (!child) {
                    console.error("Error: ", source_tree, _.first(path_items));
                    return [];
                }

                if (child.type == "file") {
                    return [child];  
                }

                return this.find(child.children, _.rest(path_items));
            }
        },

        downloadSourceCode: function() {

            console.log("download sourece code")

            let self = this;

            let header = self.getHeader(self);
            _.extend(header, {responseType: 'blob'});

            axios.get(self.SERVER_URL() + 'source-code/' + self.projectId + '/' + self.runId, header)
                    .then(function(response) {

                        console.log("in response", response)

                        let fileURL = window.URL.createObjectURL(new Blob([response.data]));
                        let fileLink = document.createElement('a');

                        fileLink.href = fileURL;
                        fileLink.setAttribute('download', "source_" + self.runId + '.zip');
                        document.body.appendChild(fileLink);

                        fileLink.click();
                    })
                   .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

	}		
};