import { mymixin } from '../../../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../../../utils/utils'

export default {
        mixins: [mymixin, utils],
        props: ["dataSourcePath", "downloadPath", "uploadPath", "imagePath", "templateName", "datasetType"],

        mounted: function() {
            this.projectId = this.$route.params['project_id'];
            this.currentPage = this.$route.params['page_nr'] || this.currentPage;
            this.activeTab[this.templateName] = "active";

            this.getData();
        },

        watch: {
            $route (to, from) {
                this.currentPage = to.params.page_nr;

                this.currentPage = Math.min(this.currentPage, Math.ceil(this.total / this.step));
                this.currentPage = Math.max(1, this.currentPage);

                this.getData();
            },
        },

        data: function() {
            return {
                projectId: "",
                currentPage: 1,
                totalPages: 1,
                step: 1,
                total: 0,
                images: [],
                isLoading: false,
                isPrevEnabled: "disabled",
                isNextEnabled: "disabled",
                isDebugMode: false,
                filter: {active: "all",},
                dataset_spec_kind: "ZIP",
                predefined_datasets: [],
                activeTab: {"DataImageCaptioningAllData": "",
                            "DataImageCaptioningTrainingData": "",
                            "DataImageCaptioningValidateData": "",
                            "DataImageCaptioningTestData": "",
                        },

                queryString: "",
                paginationButtons: [],
            }
        },

        methods: {

            getData: function() {
                let self = this;

                let curr_page = self.currentPage - 1;
                axios.get(self.SERVER_URL() + self.dataSourcePath + '/' + self.projectId  + "/" + curr_page)
                        .then(function(response) {

                            console.log("response ", response)

                            let data = self.processData(response);
                            _.extend(self, data);

                            console.log("data ", data) 

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
                let images = _.map(data.media, function(item) {
                                let path = self.SERVER_URL() + self.imagePath + '/' + item.src + "?token=" + self.getToken();

                                let text_style_class = "text-warning";

                                return {_id: self.getId(item),
                                        name: item.src,
                                        gold: item.gold,
                                        path: path,
                                        silver: item.silver,
                                        textStyle: text_style_class,
                                    };
                            });


                let predefined_datasets = _.map(data.predefined_datasets, function(dataset) {
                                            _.extend(dataset, {_id: self.getId(dataset),});
                                            return dataset;
                                        });

                predefined_datasets = _.filter(predefined_datasets, function(dataset) {
                                            return dataset.dataset_type == self.datasetType;
                                        });

                return {
                        images: images,
                        total: data.total,
                        step: data.step,
                        predefined_datasets: predefined_datasets,
                    };
            },

            uploadDataSetClicked: function() {
                let self = this;

                let form_data = new FormData();
                form_data.append('zip_file', this.$refs.data_fileInputRef.files[0]);
                form_data.append('dataset_spec_kind', this.dataset_spec_kind);
                form_data.append('predefined_dataset_id', document.getElementById("predefined_dataset_id").value);
                
                axios.post(this.SERVER_URL() + self.uploadPath  + '/' + this.projectId, form_data)
                       .then(function(response) {
                            var data = self.processData(response);
                            _.extend(self, {total: self.total + data.total,
                                            images: data.images,
                                            labels: data.labels,
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

                axios.get(self.SERVER_URL() + self.downloadPath + '/' + self.projectId, header)
                        .then(function(response) {
                            let fileURL = window.URL.createObjectURL(new Blob([response.data]));
                            let fileLink = document.createElement('a');

                            fileLink.href = fileURL;
                            fileLink.setAttribute('download', "train_" + self.projectId + '.zip');
                            document.body.appendChild(fileLink);

                            fileLink.click();
                        })
                        .catch(error => {
                            self.processErrorInPromise(error);
                        });
            },

    }
}
