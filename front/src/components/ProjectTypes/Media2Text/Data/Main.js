import { mymixin } from '../../../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../../../utils/utils'

export default {
        mixins: [mymixin, utils],
        props: ["dataSourcePath", "downloadPath", "uploadPath", "filePath", "templateName"],

        mounted: function() {
            this.projectId = this.$route.params['project_id'];
            this.runId = this.$route.params['run_id'] || this.runId;
            this.currentPage = this.$route.params['page_nr'] || this.currentPage;

            this.activeTab[this.templateName] = "active";
            this.getData();
        },

        watch: {
            $route (to, from) {
                this.currentPage = to.params.page_nr;

                this.currentPage = Math.min(this.currentPage, Math.ceil(this.totalImages / this.step));
                this.currentPage = Math.max(1, this.currentPage);

                this.getData();
            },
        },

        data: function() {
            return {
                projectId: "",
                runId: "",
                runs: [],
                currentPage: 0,
                totalPages: 0,
                totalImages: 0,
                step: 1,
                total: 0,
                isPrevEnabled: "disabled",
                isNextEnabled: "disabled",

                activeTab: {"DataMedia2TextAllData": "",
                            "DataMedia2TextTrainingData": "",
                            "DataMedia2TextValidateData": "",
                            "DataMedia2TextTestData": "",
                        },
                        
                media: [],
                paginationButtons: [],
            };
        },

        methods: {

            getData: function() {
                let self = this;

                let curr_page = self.currentPage - 1;

                axios.get(self.SERVER_URL() + self.dataSourcePath + '/' + self.projectId + "/" + curr_page)
                        .then(function(response) {

                            let data = self.processData(response);
                            _.extend(self, data);

                            self.checkPaginationButtons();
                        })
                        .catch(error => {
                            self.processErrorInPromise(error);
                        });
            },

            processData: function(response) {
                let self = this;

                if (response.status != 200) {
                    self.processErrorInPromise(response);
                    return;
                }

                let data = response.data;

                let media = _.map(data.media, function(item) {
                                let extension = _.last(item.src.split("."));
                                _.extend(item, {_id: self.getId(item),
                                                _path: self.SERVER_URL() + 'all-dataset-file/' + item.src + "?token=" + self.getToken(),
                                                type: item.type,
                                            });
                                return item;
                            });

                let runs = _.map(data.runs, function(run) {
                                _.extend(run, {_id: self.getId(run),});
                                return run;
                            });

                let predefined_datasets = _.map(data.predefined_datasets, function(dataset) {
                                            _.extend(dataset, {_id: self.getId(dataset),});
                                            return dataset;
                                        });

                return {
                        total: data.total,
                        totalImages: data.total,
                        step: data.step,
                        runs: runs,
                        media: media,
                    };
            },

            uploadFile: function() {
                let self = this;

                let form_data = new FormData();
                _.each(this.$refs.input_ref.files, function(file, i) {
                    form_data.append("files[]", file);
                });



                axios.post(this.SERVER_URL() + self.uploadPath  + '/' + this.projectId, form_data)
                        .then(function(response) {
                            var added_data = self.processData(response);
                            _.extend(self, {total: self.total + _.size(added_data.media),
                                            media: _.union(added_data.media, self.media),
                                        });

                            self.checkPaginationButtons();
                        })
                        .catch(error => {
                            self.processErrorInPromise(error)
                        });  
            },

            download: function() {
                let self = this;

                let header = self.getHeader(self);
                _.extend(header, {responseType: 'blob'});

                // axios.get(self.SERVER_URL() + self.downloadPath + '/' + self.projectId, header)
                //         .then(function(response) {
                //             let fileURL = window.URL.createObjectURL(new Blob([response.data]));
                //             let fileLink = document.createElement('a');

                //             fileLink.href = fileURL;
                //             fileLink.setAttribute('download', "train_" + self.projectId + '.zip');
                //             document.body.appendChild(fileLink);

                //             fileLink.click();
                //         })
                //        .catch(error => {
                //             self.processErrorInPromise(error);
                //         });
            },

            clearAllCheckboxes: function() {
                $(".label-checkbox").removeAttr("checked");
            },

            selectAllCheckboxes: function() {
                $(".label-checkbox").attr("checked", "checked");
            },

            filterModeChanged: function($ev) {
                let active = $ev.target.value;
                _.extend(this.filter, {active: active});

                // this.getData();
            },
    }
}
