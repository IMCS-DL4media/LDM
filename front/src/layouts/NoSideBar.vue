<template id="no-side-bar">
  <div>
    <div id = "wrapper">
      <div id="content-wrapper" class="d-flex flex-column">
        <div id="content">

          <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">

            <TopBarRightSide></TopBarRightSide>

          </nav>
          <div class="container-fluid">
            <Notifications></Notifications>
            
            <router-view></router-view>
          </div>
        </div>
      </div>
    </div>
    <!-- End of Page Wrapper -->

    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
      <i class="fas fa-angle-up"></i>
    </a>
  </div>
</template>

<script src="./NoSideBar.js"></script>
