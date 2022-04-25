<script
  export default {
    name: 'no-bars-app',
    components: {
    }
  }
</script>

<template id="no-bars">
      <div id="content-wrapper" class="d-flex flex-column">
        <div id="content">
          <div class="container-fluid">
            <router-view></router-view>
          </div>
        </div>
      </div>
</template>
