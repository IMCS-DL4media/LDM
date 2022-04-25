import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default{
    mixins: [mymixin, utils],

    mounted: function() {
        let self = this;

        self.runId = self.$route.params['run_id'];
        self.projectId = self.$route.params['project_id'];

        self.routeName = self.$route.meta.sideBarItem;

        self.getData();
        self.setActiveSidebarItem();
    },

    watch: {
        $route (to, from) {
            this.pathMatch = to.params['pathMatch'] || "";
            this.getData();

            this.routeName = to.meta.sideBarItem;
            this.setActiveSidebarItem();
        },
    },

	data: function() {
		return {
			runId: "",
            projectId: "",
            dataComponent: "",
            productionComponent: "",
            routeName: "",
            sidebarItems: this.buildSidebar(),
		}
	},
	
	methods: {
        getData: function() {
            let self = this;

            let active_project = JSON.parse(localStorage.getItem("activeProject") || "{}");
            if (active_project && self.getId(active_project) == self.projectId) {
                self.setActiveProject(active_project);               
                return;
            }

            axios.get(self.SERVER_URL() + 'active-project/' + self.projectId)
                    .then(function(response) {
                        let project = response.data.project;
                        localStorage.setItem("activeProject", JSON.stringify(project));
                        self.setActiveProject(project);
                        
                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

        setActiveProject(project) {
            let self = this;

            self.dataComponent = self.dataComponents[project.type];
            self.productionComponent = self.productionComponents[project.type];

            self.sidebarItems = self.buildSidebar();
            self.setActiveSidebarItem();
        },

        buildSidebar() {

            return [{title: "Data",
                    to: { name: this.dataComponent, params: {project_id: this.projectId, page_nr: 1,}},
                    icon: "fas fa-fw fa-database",
                    active: ""
                    },

                    {title: "Training",
                    to: { name: 'Project', params: {project_id: this.projectId }},
                    icon: "fas fa-fw fa-wrench",
                    active: "",
                    },

                    {title: "Production",
                    to: { name: this.productionComponent, params: {project_id: this.projectId, page_nr: 1,}},
                    icon: "fas fa-fw fa-industry",
                    active: "",
                    },

                    {title: "Members",
                    to: { name: 'Members', params: {project_id: this.projectId }},
                    icon: "fas fa-fw fa-user-friends",
                    active: "",
                    },
              ];
        },

        setActiveSidebarItem() {
            let name = this.routeName;

            this.sidebarItems = _.map(this.sidebarItems, function(item) {
                                  _.extend(item, {active: "",});
                                  return item;
                              });

            let item = _.find(this.sidebarItems, function(item) {
                        return item.title == name;
                    });

            if (!item) {
                console.error("No item with name", name);
                return;
            }

            _.extend(item, {active: "active",});
        },
    }
}