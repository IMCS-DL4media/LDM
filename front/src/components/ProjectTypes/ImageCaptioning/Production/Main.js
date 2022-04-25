import { mymixin } from '../../../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../../../utils/utils'

export default {
        mixins: [mymixin, utils],
        mounted: function() {
            this.projectId = this.$route.params['project_id'];
            this.currentPage = this.$route.params['page_nr'] || this.currentPage;

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
                totalPages: 0,
                step: 1,
                total: 0,
                labels: [],
                images: [],
                isLoading: false,
                isPrevEnabled: "disabled",
                isNextEnabled: "disabled",
                isDebugMode: false,
                queryString: "",
                paginationButtons: [],

                dataSourcePath: "production-data",
                imagePath: "production-file",
                modelId: "model_id"
            }
        },

        methods: {

            getData: function() {
                let self = this;

                let curr_page = self.currentPage - 1;

                let url = self.SERVER_URL() + self.dataSourcePath + '/' + self.projectId + "/" + self.modelId + "/" + curr_page;
                if (self.queryString) {
                    url = url + "?" + self.queryString;
                }

                axios.get(url)
                        .then(function(response) {

                            console.log("response ", response)

                            let data = self.processData(response);
                            _.extend(self, data);

                            console.log("data ", data) 

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
                let labels = _.map(data.labelsCount, function(label) {
                                    return {
                                            _id: label._id,
                                            category: label._id,
                                            silverCount: label.count,
                                        };
                                });

                labels = _.sortBy(labels, "category");

                let images = _.map(data.media, function(img) {
                                let path = self.SERVER_URL() + self.imagePath +  '/' + self.projectId + '/' + img.file_name + "?token=" + self.getToken();

                                let text_style_class = "text-warning";
                                if (img.result != 1) {
                                    text_style_class = "text-danger";
                                }

                                return {_id: self.getId(img),
                                        name: img.src,
                                        gold: img.gold,
                                        path: path,
                                        silver: img.silver,
                                        textStyle: text_style_class,
                                    };
                            });

                return {labels: labels,
                        images: images,
                        total: data.total,
                        step: data.step,
                    };
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
                
                // this.filter.active = filter_val;
                this.currentPage = 1;

                this.getData();
            },
    }
}
