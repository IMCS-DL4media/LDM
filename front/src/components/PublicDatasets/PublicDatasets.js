import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],
    mounted: function() {
        let self = this;

        axios.get(this.SERVER_URL() + "public-datasets")
                .then(function(response) {
                    let data = response.data;
                    if (response.status == 200) {
                        _.extend(self, {datasets: _.values(data.predefined_datasets),});
                    }

                })
                .catch(error => {
                    self.processErrorInPromise(error);
                });
    },

    data: function() {
        return {
            datasets: [],
        }
    },

    methods: {},
}