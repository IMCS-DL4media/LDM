<template id="sidebar">
  <div>
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion toggled" id="accordionSidebar">

      <router-link class="sidebar-brand d-flex align-items-center justify-content-center" to="/projects">
          <div class="sidebar-brand-icon rotate-n-15">
              <i class="fas fa-laugh-wink"></i>
          </div>
          <div class="sidebar-brand-text mx-3">DL Framework<sup>2</sup></div>
      </router-link>


      <!-- Divider -->
      <hr class="sidebar-divider my-0">
      <hr class="sidebar-divider">


      <li class="nav-item" :class=item.active v-for="item in sidebarItems">
        <router-link class="nav-link" :to=item.to>
          <i :class=item.icon></i>
          <span>{{item.title}}</span>
        </router-link>
      </li>


    </ul>
  </div>
</template>

<script src="./SideBar.js"></script>