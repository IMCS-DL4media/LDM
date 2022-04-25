<template>	
  <div class="container">
    <div class="row justify-content-center my-5">
      <div class="col-xl-10 col-lg-12 col-md-9">
        <div class="row">
          <div class="col-lg-3"></div>

          <div class="col-lg-6">
            <form class="user">
              <div class="text-center">
                <router-link :to="{name: 'Login'}">
                  <button class="btn btn-primary btn-user btn-block">Go To Login Page</button>
                </router-link>
              </div>
            </form>
          </div>

          <div class = "col-lg-3"></div>
        </div>
      </div>
    </div>
  </div>
</template>
