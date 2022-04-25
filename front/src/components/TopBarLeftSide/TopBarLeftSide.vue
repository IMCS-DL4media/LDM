<template id="TopBarLeftSide">

    <ul class="navbar-nav">
      <li class="nav-item dropdown no-arrow ">
        <a class="nav-link dropdown-toggle" href="#" id="projects-dropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <!-- <i class="fas fa-bell fa-fw"></i> -->
          <span>Projects</span>
          <!-- <i class="fas fa-caret-down"></i>  -->

          <!-- Counter - Alerts -->
          <!-- <span class="badge badge-danger badge-counter">3+</span> -->
        </a>

        <!-- Dropdown - Alerts -->
        <div class="dropdown-list dropdown-menu animated--grow-in" aria-labelledby="projects-dropdown">
            <h6 class="dropdown-header">
                Projects
            </h6>

            <router-link class="dropdown-item d-flex align-items-center" :to="{ name: 'Project', params: {project_id: project.id,}}" v-for="project in projects" :key="project.id">
                <!-- <a class="dropdown-item d-flex align-items-center" :href="'/project/' + project.id" v-for="project in projects"> -->
                      <div class="mr-3">
                          <div class="icon-circle bg-primary">
                              <i class="fas fa-file-alt text-white"></i>
                          </div>
                      </div>
                      <div>
                          <div class="small text-gray-500">{{project._created_at}}</div>
                          <span class="font-weight-bold">{{project.name}} {{project.type}}</span>
                      </div>
                <!-- </a> -->
            </router-link>

          <router-link class="dropdown-item text-center small text-gray-500" :to="{name: 'Projects'}">Show All Projects</router-link>
        
        </div>
      </li>
    </ul>
</template>

<script src="./TopBarLeftSide.js"></script>