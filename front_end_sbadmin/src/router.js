import Vue from "vue";
import Router from "vue-router";
import ListOfProjects from "./mycomponents/ListOfProjects/ListOfProjects.vue";

import Project from "./mycomponents/Project/Project.vue";
import Run from "./mycomponents/Run/Run.vue";

// import AddProject from "./views/AddProject.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Projects",
      component: ListOfProjects
    },
    {
      path: "/project/:project_id",      
      component: Project, 		
      props: true
    },
    { 
      path: '/run/:run_id', 		
      component: Run,		 		
      props: true 
    },
    // { 
    //   path: '/addproject/:user_id', 
    //   component: AddProject, 	
    //   props: true
    // },    
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/About.vue")
    }
  ]
});
