<template>
	<div>
<!-- 
		<div class="d-sm-flex align-items-center justify-content-between mb-4">
			<h1 class="h5 mb-0 text-gray-800">{{projectId}}</h1>
			<button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#delete-project-modal"><i class="fas fa-trash"></i></button>
		</div> -->

		<div class="container_tabs_pills">
<!-- 			<ul class="nav nav-pills">
				<li class="nav-item">
					<router-link :to="{ name: 'Project', params: {project_id: projectId }}" class="nav-link active" role="tab" data-toggle="tab">
						Runs 
					</router-link>
				</li>
				<li class="nav-item">

					<router-link :to="{ name: project.settings.datasets[0].name, params: {project_id: projectId, run_id: 'None', page_nr: 1,}}" class="nav-link" role="tab" data-toggle="tab">
						Data
					</router-link>
				</li>		
			</ul> -->

			<!-- <br/> -->

			<div class="tab-content">
				<div class="tab-pane fade active show" id="tab-project-runs">
					<div class="card shadow mb-4">
						<div class="card-body">

							<div class="row">
								<div class="col-lg-8  mb-2">
									ProjectId: {{projectId}}
								</div>

								<div class="col-lg-4 text-right mb-2">
									<div class="btn-group" role="group">
										<button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#delete-project-modal"><i class="fas fa-trash"></i></button>
									</div>
								</div>
							</div>

							<div class="table-responsive">
								<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">

									<thead>
										<tr>
											<th>#</th>
											<th>Run ID</th>
											<th>Comment</th>
											<th>Start time</th>
											<th>End time</th>
											<!-- <th>IP</th> -->
											<th>User</th>
											<!-- <th>Commit URL</th> -->
											<th></th>
											<th></th>
										</tr>
									</thead>

									<tbody>
										<tr :id="run._id" class="run" v-for="(run, ind) in runs" :key="run._id">
											<td>{{ind + 1}}</td>
											<td>
												<router-link :to="{name: 'Run', params: {run_id: run._id}}">{{run._id}}</router-link>
											</td>
											<td>{{run._short_comment}}</td>
											<td>{{run._start_time}}</td>
											<td>{{run._finish_time}}</td>
											<!-- <td>{{run.remote_address}}</td> -->
											<td>{{run.user_email}}</td>
<!-- 											<td>
												<a :href="run.git_commit_url">{{run.git_commit_url}}</a>
											</td> -->
											<td class="text-center">
												<a href="#" data-toggle="modal" data-target="#edit-run-modal" @click="setActiveRun(run._id)">
													<i class="fas fa-edit"></i>
												</a>
											</td>
											<td class="text-center">
												<a href="#" data-toggle="modal" data-target="#delete-run-modal" @click="setActiveRun(run._id)">
													<i class="fas fa-trash"></i>
												</a>
											</td>
										</tr>
									</tbody>

								</table>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>


		<div class="modal" id="edit-run-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<div class="modal-header">
						<h4 class="modal-title">Edit</h4>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<div class="modal-body">
						<div class="form-group">
							<label for="edit-comment-field">Comment</label>
							<input type="text" class="form-control" id="edit-comment-field" :value="activeRun.comment">
						</div>						
					</div>

					<div class="modal-footer">
						<button type="button" class="btn btn-primary" data-dismiss="modal" @click="editRun">Edit</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>


		<div class="modal" id="delete-project-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title">Delete project. Are you ABSOLUTELY SURE?</h5>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<div class="modal-body">
						<div class="alert alert-danger" role="alert">
							You are about to permanently delete this project. Once a project is permanently deleted it cannot be recovered. Permanently deleting this project will immediately delete its repositories and all related resources including datasets, runs etc.
						</div>

<!-- 						<div class="form-group">
							<label for="confirm-field">Please type the project name to confirm: </label>
							<input type="text" class="form-control" id="confirm-field" placeholder="Enter project name">	
						</div> -->

					</div>

					<div class="modal-footer">
						<button type="button" class="btn btn-danger" data-dismiss="modal" @click="deleteProject">Delete</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>


		<div class="modal" id="delete-run-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title">Delete run. Are you ABSOLUTELY SURE?</h5>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<div class="modal-body">
						<div class="alert alert-danger" role="alert">
							You are about to permanently delete this run. Once a run is permanently deleted it cannot be recovered. Permanently deleting this run will immediately delete its repositories and all related resources.
						</div>

					</div>

					<div class="modal-footer">
						<button type="button" class="btn btn-danger" data-dismiss="modal" @click="deleteRun">Delete</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>



	</div>

</template>

<script src="./Project.js"></script>