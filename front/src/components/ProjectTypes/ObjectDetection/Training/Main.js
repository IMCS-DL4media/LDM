import { mymixin } from '../../../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../../../utils/utils'

import './../style.css';

export default {
        mixins: [mymixin, utils],
        props: ["dataSourcePath", "downloadPath", "uploadPath", "imagePath", "templateName", "datasetType"],

        mounted: function() {
            this.projectId = this.$route.params['project_id'];
            this.runId = this.$route.params['run_id'] || this.runId;
            this.currentPage = this.$route.params['page_nr'] || this.currentPage;

            this.activeTab[this.templateName] = "active";
            this.currentTemplate = this.$route.name;

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
                runId: "",
                runs: [],
                currentPage: 1,
                totalPages: 0,
                step: 1,
                total: 0,
                labels: [],
                images: [],
                isLoading: false,
                isPrevEnabled: "disabled",
                isNextEnabled: "disabled",
                // isDebugMode: false,
                filter: {active: "all",},
                dataset_spec_kind: "ZIP",
                predefined_datasets: [],
                // activeTab: {"ImageClassificationTrainingData": "",
                //             "ImageClassificationValidateData": "",
                //             "ImageClassificationTestData": "",
                //         },


                activeTab: {"ObjectDetectionTrainingData": "",
                            "ObjectDetectionValidateData": "",
                            "ObjectDetectionTestData": "",
                        },


                queryString: "",
                paginationButtons: [],
                currentTemplate: "",
            }
        },

        methods: {

            getData: function() {
                let self = this;

                let curr_page = self.currentPage - 1;

                let url = self.SERVER_URL() + self.dataSourcePath + '/' + self.projectId + "/" + self.runId + "/" + curr_page;
                if (self.queryString) {
                    url = url + "?" + self.queryString;
                }

                axios.get(url, self.getHeader(self))
                        .then(function(response) {

                            console.log("response ", response)

                            let data = self.processData(response);
                            _.extend(self, data);

                            console.log("data 22", data) 

                            self.checkPaginationButtons();
                        })
                        .catch(error => {
                            self.processErrorInPromise(error);
                            self.$Progress.fail()
                        });
            },

            processData: function(response) {
                let self = this;

                if (response.status != 200) {
                    self.processErrorInPromise(response);
                    return;
                }

                let data = response.data;

                console.log("data ", data)


                let images = _.map(data.media, function(img) {
                                let path = self.SERVER_URL() + self.imagePath +  '/' + self.projectId + '/' + img.uploaded_file_name + "?token=" + self.getToken();

                                let text_style_class = "text-warning";
                                if (img.result != 1) {
                                    text_style_class = "text-danger";
                                }

                                let max_height = 250;
                                let img_height = img.height || max_height;
                                let height_ratio = max_height / img_height;


                                let silverPositions = _.map(img.silver, function(item) {
                                                let bbox = item.bbox;

                                                let height_number = ((bbox[3] - bbox[1]) * height_ratio);

                                                let left = "left: " + (bbox[0] * height_ratio)  + "px;";
                                                let top = "top: " + (bbox[1] * height_ratio) + "px;";
                                                let width = "width: " + ((bbox[2] - bbox[0]) * height_ratio) + "px;";
                                                let height = "height: " + height_number + "px;";                                             

                                                let text_style = "color:blue;"
                                                let style = left + top + width + height + text_style;

                                                return {style: style,
                                                        labelStyle: "position:absolute;left:2px;top:" + height_number + "px;",
                                                        label: item.value,
                                                    };
                                            });


                                let goldPositions = _.map(img.gold, function(item) {
                                                let bbox = item.bbox;
                                                let height_number = ((bbox[3] - bbox[1]) * height_ratio);

                                                let left = "left: " + (bbox[0] * height_ratio)  + "px;";
                                                let top = "top: " + (bbox[1] * height_ratio) + "px;";
                                                let width = "width: " + ((bbox[2] - bbox[0]) * height_ratio) + "px;";
                                                let height = "height: " + height_number + "px;";                                             

                                                let text_style = "color:red;"
                                                let style = left + top + width + height + text_style;

                                                return {style: style,
                                                        labelStyle: "position:absolute;left:2px;top:" + height_number + "px;",
                                                        label: item.value,
                                                    };
                                            });



                                return {_id: self.getId(img),
                                        path: path,
                                        height: "max-height:" + max_height + "px",
                                        // gold: img.gold,
                                        // positions: positions,
                                        silverPositions: silverPositions,
                                        goldPositions: goldPositions,

                                        textStyle: text_style_class,
                                    };
                            });

                console.log("images ", images)

                let runs = _.map(data.runs, function(run) {
                                _.extend(run, {_id: self.getId(run),});
                                return run;
                            });

                return {
                        // labels: labels,
                        images: images,
                        total: data.total,
                        step: data.step,
                        runs: runs,
                    };





                // let silvers_map = {};
                // _.each(data.silversCount, function(label) {
                //     silvers_map[label._id] = label.count;
                // });


                // console.log("silvers_map", silvers_map)


                // let labels = _.map(data.labels, function(label) {
                //                     return {
                //                             _id: self.getId(label),
                //                             category: label.category,
                //                             goldCount: label.count || 0,
                //                             silverCount: silvers_map[label.category] || 0,
                //                         };
                //                 });


                // labels = _.sortBy(labels, "category");

                // let silvers = {};
                // _.each(data.silversCount, function(silver) {

                //     console.log("sivler", silver)

                //     silvers[silver._id] = silver.count;
                // });


                // let images = _.map(data.media, function(img) {

                //                 console.log("img", img)

                //                 let path = self.SERVER_URL() + self.imagePath +  '/' + img.src + "?token=" + self.getToken();
                //                 let text_style_class = "text-warning";
                //                 if (img.result != 1) {
                //                     text_style_class = "text-danger";
                //                 }

                //                 return {_id: self.getId(img),
                //                         name: img.src,
                //                         gold: img.gold,
                //                         path: path,
                //                         silver: img.silver,
                //                         textStyle: text_style_class,
                //                     };
                //             });


                // let runs = _.map(data.runs, function(run) {
                //                 _.extend(run, {_id: self.getId(run),});
                //                 return run;
                //             });

                // let predefined_datasets = _.map(data.predefined_datasets, function(dataset) {
                //                             _.extend(dataset, {_id: self.getId(dataset),});
                //                             return dataset;
                //                         });


                // predefined_datasets = _.filter(predefined_datasets, function(dataset) {
                //                             return dataset.dataset_type == self.datasetType;
                //                         });

                // console.log("labelsss ", labels)

                // return {labels: labels,
                //         images: images,
                //         total: data.total,
                //         step: data.step,
                //         runs: runs,
                //         predefined_datasets: predefined_datasets,
                //     };
            },

            uploadDataSetClicked: function() {
                let self = this;

                let form_data = new FormData();
                form_data.append('zip_file', this.$refs.data_fileInputRef.files[0]);
                form_data.append('dataset_spec_kind', this.dataset_spec_kind);
                form_data.append('predefined_dataset_id', document.getElementById("predefined_dataset_id").value);
                
                axios.post(this.SERVER_URL() + self.uploadPath  + '/' + this.projectId, form_data, this.getHeader(this))
                        .then(function(response) {
                            var data = self.processData(response);
                            _.extend(self, {total: self.total + data.total,
                                            images: data.images,
                                            labels: data.labels,
                                        });
                            self.checkPaginationButtons();
                        })
                        .catch(error => {
                            self.processErrorInPromise(error);
                        });  
            },

            download: function() {
                let self = this;

                let header = self.getHeader(self);
                _.extend(header, {responseType: 'blob'});

                console.log("download")

                axios.get(self.SERVER_URL() + self.downloadPath + '/' + self.projectId, header)
                        .then(function(response) {

                            console.log("response ", response)

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

            // checkPaginationButtons: function() {

            // },

            runChanged: function(event) {
                this.runId = event.target.value || this.runId;

                this.filter.active = "all";
                this.queryString = "";


                console.log("this.templateName ", this.templateName)


                this.$router.push({name: this.currentTemplate,
                                    params: {project_id: this.projectId,
                                                run_id: this.runId,
                                                page_nr: 1,
                                            }
                                });
            },

            clearAllCheckboxes: function() {
                $(".label-checkbox").removeAttr("checked");
            },

            selectAllCheckboxes: function() {
                $(".label-checkbox").attr("checked", "checked");
            },

            filterModeChanged: function($ev) {
                let filter_val = $("#filter-options").find('input:radio:checked').attr("value");

                let exclude = _.filter($(".label"), function(label) {
                                    return $(label).prop('checked') == false;
                                });

                let exclude_ids = _.map(exclude, function(item) {
                                    return $(item).attr("id");
                                });

                if (_.size(exclude_ids) > 0 && filter_val) {
                    this.queryString = "exclude=" + exclude_ids.join(",") + "&" + "match=" + filter_val;
                }
                else {
                    if (_.size(exclude_ids) == 0) {
                        this.queryString = "match=" + filter_val;
                    }
                    else {
                        this.queryString = "exclude=" + exclude_ids.join(",");
                    }
                }
                
                this.filter.active = filter_val;
                this.currentPage = 1;

                this.getData();
            },
    }
}
