import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
        mixins: [mymixin, utils],

        mounted: function() {
            let self = this;

            self.projectId = self.$route.params['project_id'] || self.projectId;
            self.runId = self.$route.params['run_id'] || self.runId;

            self.getData();
        },

        data: function() {
            return {
                projectId: "",
                runId: "None",
                project: JSON.parse(localStorage.getItem("activeProject")),
                charts: [],
                chartTypes: [{type: "line-chart",},
                            {type: "column-chart",},
                        ],
                current_chart_id: "",
            }
        },

        methods: {

            getData: function() {
                let self = this;

                axios.get(self.SERVER_URL() + 'project-charts/' + self.projectId + "/" + self.runId)
                        .then(function(response) {

                            console.log("response ", response)

                            if (response.status != 200) {
                                throw Error(response.statusText);
                            }
                            
                            let data = response.data;
                            let charts_data = data.data;

                            self.charts = _.map(data.charts, function(chart) {

                                                let chart_data_obj = _.find(charts_data, function(item) {
                                                                        return item.chart_id == self.getId(chart);
                                                                    });

                                                let chart_data = [];
                                                if (chart_data_obj) {
                                                    chart_data = chart_data_obj.data;
                                                }

                                                _.extend(chart, {_id: self.getId(chart),
                                                                 width: chart.width || 12,
                                                                 data: chart_data,
                                                        });

                                                return chart;
                                            });


                            console.log("self.charts ", self.charts)

                        })
                        .catch(error => {
                            self.processErrorInPromise(error)
                        });
            },


            addData: function(chart_id) {
                let self = this;
                console.log("in add data")

                let list = {charts: [{_id: chart_id,
                                     data: [
                                            [1, 22], [2, 25], [3, 28], [4, 34],
                                        ]
                                    },
                                ]
                            };

                axios.post(self.SERVER_URL() + "logger/log-charts/" + self.projectId + "/" + self.runId, list)
                        .then(response => { 
                            console.log("response ", response)
                            if (response.status != 200) {
                                throw Error(response.statusText);
                            }
                        })
                        .catch(error => {
                            self.processErrorInPromise(error);
                        });
            },


            addChart: function() {
                let self = this;

                let list = {"title": $("#chart-title").val(),
                            "type": $("#chart-type option:selected").attr("value"),
                            "xtitle": $("#chart-xtitle").val(),
                            "ytitle": $("#chart-ytitle").val(),
                            "width": $("#chart-width").val(),
                        };

                axios.post(self.SERVER_URL() + "logger/chart/" + self.projectId, list)
                        .then(response => { 
                            console.log("response ", response)
                            if (response.status != 200) {
                                throw Error(response.statusText);
                            }

                            let chart = response.data.chart;
                            _.extend(chart, {_id: self.getId(chart),
                                            index: _.size(self.charts) + 1,
                                            width: chart.width || 12,
                                        });

                            self.charts = _.union(self.charts, [chart]);
                        })
                        .catch(error => {
                            self.processErrorInPromise(error);
                        });

            },

            openDeleteChartForm: function(chart_id) {
                console.log("openDeleteChartForm ", chart_id)
                this.current_chart_id = chart_id;
            },

            deleteChart: function() {
                let self = this;

                axios.delete(self.SERVER_URL() + "logger/log-chart/" + self.current_chart_id + "/" + self.projectId + "/" + self.runId)
                        .then(response => { 
                            console.log("response ", response)
                            if (response.status != 200) {
                                throw Error(response.statusText);
                            }

                            self.charts = _.reject(self.charts, function(chart) {
                                                return chart._id == self.current_chart_id;
                                            });
                        })
                        .catch(error => {
                            self.processErrorInPromise(error);
                        });
            },

            reloadPage: function() {
                this.getData();
            },

        }
}
