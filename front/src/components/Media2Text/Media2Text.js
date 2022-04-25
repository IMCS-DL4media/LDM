 import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default{	 
    mixins: [mymixin, utils],

    mounted: function() {
        let self = this;

        self.id = self.$route.params['id'];
        self.runId = self.$route.params['runId'] || self.runId;
        self.projectId = self.$route.params['projectId'] || self.projectId;
        self.filePath = self.$route.params['filePath'];

        self.getData();
    },

    watch: {
        $route (to, from) {
            this.getData();
        },
    },

	data: function() {
		return {
            id: "",
            runId: "",
            projectId: "",
            runs: [],
            filePath: "",
            media: {gold: "Enter text..."},
            error: null
		};
	},

    methods: {

        getData: function() {
            let self = this;

            console.log("self.filePath ", self.filePath + '/' + self.projectId + "/" + self.id)


            axios.get(self.SERVER_URL() + self.filePath + '/' + self.projectId + "/" + self.id)
                .then(function(response) {

                    console.log("response ", response)

                    if (response.status != 200) {
                        throw Error(response.statusText);
                    }
                    
                    self.media = response.data.media;
                    let path = self.SERVER_URL() + 'all-dataset-file/' + self.media.src + "?token=" + self.getToken();
                    

                    console.log("path ", path)


                    _.extend(self.media, {_id: self.getId(self.media),
                                            path: path,
                            });

                    self.runs = _.map(response.data.runs, function(run) {
                                    _.extend(run, {_id: self.getId(run),});
                                    return run;
                                });

                })
                .catch(error => {
                    self.processErrorInPromise(error)
                });
        },

        updateTranscript: function(ev) {
            var self = this;

            let list = {gold: $("#text").val(),};


            console.log("self.filePath update", self.filePath)


            axios.put(self.SERVER_URL() + self.filePath + '/' + self.projectId + '/' + self.id, list)
                    .then(function(response) {
                        _.extend(self.media, {gold: list.gold,});
                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

        deleteFile: function(ev) {
            let self = this;
            axios.delete(self.SERVER_URL() + self.filePath + '/' + self.projectId + '/' + self.id)
                    .then(function(response) {
                        self.$router.go(-1);
                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

        back: function() {
            this.$router.go(-1);
        },
    }

};