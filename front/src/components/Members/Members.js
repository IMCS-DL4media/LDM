import { mymixin } from '../../mixins/mixins.js'

import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],

    mounted: function() {
        let self = this;

        self.projectId = self.$route.params['project_id'] || self.projectId;
        axios.get(self.SERVER_URL() + 'project-members/' + self.projectId)
                .then(function(response) {

                    console.log("response ", response)

                    if (response.status != 200) {
                        throw Error(response.statusText);
                    }
                    
                    self.members = _.map(response.data.members, function(member, i) {
                                        _.extend(member, {_id: self.getId(member), index: i + 1,});
                                        return member;
                                    });

                    self.roles = response.data.roles;
                })
                .catch(error => {
                    self.processErrorInPromise(error)
                });

    },

	data: function() {
		return {
            projectId: "",
            error: null,
            members: [],
            roles: [],
            query: '',
            users: [],
		};
	},

    watch: {
        query: _.debounce(function(newQuery) {
                    this.searchUsers(newQuery)
                }, 250)
    },

    methods: {
        addMember: function() {
            let self = this;

            if (_.isEmpty(self.query)) {
                return;
            }

            let list = {email: self.query,
                        roleCode: $("#member-role option:selected").attr("value"),
                    };

            axios.post(this.SERVER_URL() + "project-member/" + self.projectId, list)
                    .then(response => { 
                        console.log("response ", response)
                        if (response.status != 200) {
                            throw Error(response.statusText);
                        }

                        let member = response.data.member;
                        _.extend(member, {_id: self.getId(member), index: _.size(self.members) + 1,});

                        self.members = _.union(self.members, [member]);
                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

        setActiveMember: function(member_id) {
            $("#remove-user-modal").attr({"data-id": member_id});
        },

        deleteMember: function() {
            let self = this;

            let member_id = $("#remove-user-modal").attr("data-id");
            axios.delete(self.SERVER_URL() + 'project-member/' + self.projectId + '/' + member_id)
                    .then(function(response) {      

                        if (response.status != 200) {
                            throw Error(response.statusText);
                        }

                        self.members = _.reject(self.members, function(member) {
                                            return member._id == member_id;
                                        });
                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

        searchUsers: function() {
            let self = this;

            axios.get(self.SERVER_URL() + 'users/' + self.projectId + "?query=" + this.query)
                    .then(function(response) {    
                        self.users = response.data.users;
                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

        select: function() {
        },

    },
};
