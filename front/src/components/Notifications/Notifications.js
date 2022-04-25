import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore';
import utils from '../../utils/utils'

import { EventBus } from '../event-bus.js';

export default {
    mixins:[mymixin, utils],
    mounted: function() {
    	var self = this;
		var types = {
						info: "info",
						error: "danger",
						warning: "warning",
					};

		EventBus.$on('add-notification', function(data_in) {
			var type_in = data_in.type || "info";
			

			self.notifications.push({id: $.now(), msg: data_in.msg, type: "alert-" + types[type_in]});
		});

		EventBus.$on('remove-notification', function(id) {
			self.notifications = _.reject(self.notifications, function(notification) {
									return notification.id == id;
								});
		});

		EventBus.$on('remove-all-notifications', function() {
			self.notifications = [];
		});

    },

    data: function() {
		return {notifications: [],};
    },

}