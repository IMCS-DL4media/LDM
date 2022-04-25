<template>
	<div>
		<!-- Outer Row -->
		<div class="row justify-content-center">

			<div class="col-xl-10 col-lg-12 col-md-9">

				<div class="card o-hidden border-0 shadow-lg my-5">
					<div class="card-body p-0">
						<!-- Nested Row within Card Body -->
						<div class="row">
						<!-- <div class="col-lg-6 d-none d-lg-block bg-login-image"></div> -->

							<div class="col-lg-12">
								<div class="p-5">


									<div class="input-group mb-3">
										<input type="text" class="form-control" aria-describedby="reload-token" :value="token">
										<button class="btn btn-outline-secondary" type="button" id="reload-token" @click="reloadToken">Reload</button>
									</div>


									<form class="user">




<!-- 										<div class="form-group">
											<input type="text" class="form-control form-control-user" id="username" placeholder="Username">
										</div>


										<div class="form-group">
											<input type="email" class="form-control form-control-user" id="email" aria-describedby="emailHelp" placeholder="Enter Email Address...">
										</div>
 -->
										<div class="form-group">
											<input type="password" class="form-control form-control-user" id="password" placeholder="Old password">
										</div>

										<div class="form-group">
											<input type="password" class="form-control form-control-user" id="password2" placeholder="New password">
										</div>

										<div class="form-group">
											<input type="password" class="form-control form-control-user" id="password3" placeholder="Repeat password">
										</div>


										<div class="btn btn-primary btn-user btn-block" v-on:click="changePassword">
											<span>Change password</span>
										</div>

									</form>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script src="./Profile.js"></script>