import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default{	 
	// props: ['run_id'],
    mixins: [mymixin, utils],

    mounted: function() {
        let self = this;

        self.id = self.$route.params['id'];
        self.filePath = self.$route.params['filePath'];
        self.projectId = self.$route.params['projectId'] || self.projectId;

        self.runId = self.$route.params['runId'] || self.runId;

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
			runId: "None",
            projectId: "",
            runs: [],
			path: "",
			filePath: "",
            media: {},
			error: null
		};
	},

    methods: {
        updateTranscript: function(ev) {
            var self = this;

            let list = {gold: $("#gold").val(),};

            axios.put(self.SERVER_URL() + self.filePath + '/' + self.projectId + '/' + self.id, list, self.getHeader(self))
                    .then(function(response) {
                        _.extend(self.media, {gold: list.gold,});
                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

        getData: function() {
            let self = this;

            axios.get(self.SERVER_URL() + self.filePath + '-transcription/' + self.projectId + '/' + self.runId + "/" + self.id, self.getHeader(self))
                    .then(function(response) {

                        console.log("response ", response)

                        if (response.status != 200) {
                            throw Error(response.statusText);
                        }
                        
                        self.media = response.data.media;
                        _.extend(self.media, {_id: self.getId(self.media),});

                        console.log("self.media ", self.media)


                        
                        self.path = self.SERVER_URL() + self.filePath + '/' + self.media.src + "?token=" + self.getToken();
                        self.runs = _.map(response.data.runs, function(run) {
                                        _.extend(run, {_id: self.getId(run),});
                                        return run;
                                    });

                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },



        runChanged: function(ev) {
            this.runId = event.target.value || this.getNone();
            this.$router.push({name: "VideoTranscription", params: {projectId: this.projectId,
                                                                    runId: this.runId,
                                                                    id: this.id,
                                                                }});
        },

        getNone: function() {
            return "None";
        },

        isRunNone: function() {
            return this.runId == this.getNone();
        },

        deleteFile: function(ev) {
            let self = this;
            axios.delete(self.SERVER_URL() + self.filePath + '/' + self.projectId + '/' + self.id, self.getHeader(self))
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