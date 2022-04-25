<template id="main">
  <div>
    <div id = "wrapper">
      <SideBar></SideBar> 
      <div id="content-wrapper" class="d-flex flex-column">
        <div id="content">
          <TopBar></TopBar>
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

<script src="./Default.js"></script>