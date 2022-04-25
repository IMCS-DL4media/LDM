import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],
    props: ["dataSourcePath", "downloadPath", "uploadPath", "imagePath", "templateName"],

    mounted: function() {
        let self = this;

        console.log("in public dataset")

        self.activeTab["ImageClassificationTrainingData"] = "active";

        // self.dataSourcePath = "public-dataset";

        this.dataset = this.$route.params['dataset'];
        this.datasetType = this.$route.params['type'];

        this.currentPage = this.$route.params['page'] - 1;

        axios.get(this.SERVER_URL() + "public-dataset" + '/' + this.dataset + "/" + this.datasetType + "/" + this.currentPage)
                .then(function(response) {
                    console.log("response ", response)

                    let data = self.processData(response);
                    _.extend(self, data);
                })
                .catch(error => {
                    self.processErrorInPromise(error);
                });
    },

    data: function() {
        return {
            totalImages: 0,
            images: [],
            labels: [],
            currentPage: 0,

            dataset: "",
            datasetType: "",

            activeTab: {"ImageClassificationTrainingData": "",
                        "ImageClassificationValidateData": "",
                        "ImageClassificationTestData": "",
                    },

            filter: {},

            isPrevEnabled: "disabled",
            isNextEnabled: "disabled",

            isDebugMode: false,
        }
    },

    methods: {            

        processData: function(response) {
            let self = this;

            if (response.status != 200) {
                self.processErrorInPromise(response);
                return;
            }

            let data = response.data;

            let labels_map = {};
            _.each(data.labelsCount, function(label) {
                labels_map[self.getId(label)] = label.count;
            });

            let labels = _.map(data.labels, function(label) {
                                                return {_id: self.getId(label),
                                                        category: label.category,
                                                        goldCount: labels_map[label.category],
                                                    };
                                            });

            let images = _.map(data.images, function(img) {
                                let path = self.SERVER_URL() + "public-image/" + self.dataset + "/" + self.datasetType + '/' + img.src;

                                return {_id: self.getId(img),
                                        name: img.src,
                                        class: img.class,
                                        path: path,
                                    };
                            });

            return {labels: labels,
                    images: images,
                    totalImages: data.totalImages,
                    step: data.step,
                };
        },


        prev: function(e) {
            e.preventDefault();
            this.currentPage = Math.max(0, this.currentPage - 1);
            this.getData();
            this.checkPaginationButtons();
        },

        next: function(e) {
            e.preventDefault();
            this.currentPage = Math.min(this.currentPage + 1, Math.ceil(this.totalImages / this.step));
            this.getData();
            this.checkPaginationButtons();
        },


        checkPaginationButtons: function() {

            if (this.currentPage > 0) {
                this.isPrevEnabled = "";
            }
            else {
                this.isPrevEnabled = "disabled";
            }


            if (this.currentPage < Math.ceil(this.totalImages / this.step)) {
                this.isNextEnabled = "";
            }
            else {
                this.isNextEnabled = "disabled";
            }
        },




        // prev: function() {
        //     console.log("prev")

        // },

        // next: function() {
        //     console.log("next")

        //     // this.$router.push({name: "PublicDataset", params: {dataset: this.dataset,
        //     //                                                     dataset_type: this.datasetType,
        //     //                                                     page: this.currentPage + 2,
        //     //                                                 }});
        // },

        isRunNone: function() {

            console.log("is run none")

        },

    },
}