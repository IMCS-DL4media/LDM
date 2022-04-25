<template>
	<div>

		<div class="row">
			<div class="offset-lg-1 col-lg-10">
				<div class="d-sm-flex align-items-center justify-content-between mb-4">
					<h1 class="h3 mb-0 text-gray-800">Members</h1>
					<button type="button" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm" data-toggle="modal" data-target="#add-member-modal"><i class="fas fa-plus fa-sm text-white-50"></i> Add Member</button>
				</div>
			</div>
		</div>
		
		<div class="row">
			<div class="offset-lg-1 col-lg-10">
				<div class="row">
					<div class="table-responsive">
						<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">

							<thead>
								<tr>
									<th>#</th>
									<th>User</th>
									<th>Role</th>
									<th></th>
								</tr>
							</thead>

							<tbody>
								<tr class="project" v-for="member in members" :key="member.id">
									<th>{{member.index}}</th>
									<th>{{member.email}}</th>
									<th>{{member.role}}</th>
									<th class="text-center">
										<a v-if="member.role_code != 0" href="#" data-toggle="modal" data-target="#remove-user-modal" @click="setActiveMember(member._id)">
											<i class="fas fa-trash"></i>
										</a>
									</th>
								</tr>
							</tbody>

						</table>
					</div>
				</div>
			</div>
		</div>


		<div class="modal" id="add-member-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title">Add member</h5>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<div class="modal-body">
						<div class="form-group">
							<label for="user-name">Name</label>
							<vue-bootstrap-typeahead 
										id="user-name"
										placeholder="Search users"
										v-model="query"
										:data="users"
										:serializer="s => s.email"
										:minMatchingChars="1"
										@hit="select"
									>
							</vue-bootstrap-typeahead>

						</div>

						<div class="form-group">
							<label for="exampleInputEmail1">Role</label>
							<select class="form-control" id="member-role">
								<option :value="role.role_code" v-for="role in roles" :key="role.role_code">{{role.role}}</option>
							</select>		
						</div>
					</div>

					<div class="modal-footer">
						<button type="button" class="btn btn-success" data-dismiss="modal" @click="addMember">OK</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>

		<div class="modal" id="remove-user-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title">Are you sure?</h5>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<div class="modal-footer">
						<button type="button" class="btn btn-danger" data-dismiss="modal" @click="deleteMember">OK</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>
	</div>

</template>

<script src="./Members.js"></script>
