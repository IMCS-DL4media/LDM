<template>	
  <div class="container">

    <div class="row justify-content-center">

      <div class="col-xl-10 col-lg-12 col-md-9">

        <div class="card o-hidden border-0 shadow-lg my-5">
          <div class="card-body p-0">

            <div class="row">
              <div class="col-lg-3"></div>

              <div class="col-lg-6">
                <div class="p-5">
                  <div class="text-center">
                    <h1 class="h4 text-gray-900 mb-4">LDM Framework</h1>
                  </div>
<!--                   <div class="text-center text-danger" v-if="this.error.length>=1">
                    <p>{{error}}</p>
                  </div> -->

                  <form class="user">
                    <div class="form-group">
                      <input class="form-control form-control-user" id="email" placeholder="Enter Email Address...">
                    </div>
                    <div class="form-group">
                      <input type="password" class="form-control form-control-user" id="password" placeholder="Password">
                    </div>

                    <button type="button" class="btn btn-primary btn-user btn-block" @click.prevent="login">Login</button>
                    <hr>
                  </form>

                  <div class="text-center">
                    <router-link :to="{name: 'Register'}">
                      <a class="small">Create an Account!</a>
                    </router-link>
                  </div>

                </div>
              </div>

              <div class = "col-lg-3"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script src = "./Login.js"></script>