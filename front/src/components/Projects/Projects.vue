<template>	
	<div>

		<div class="row">
			<div class="offset-lg-1 col-lg-10">
				<div class="d-sm-flex align-items-center justify-content-between mb-4">
					<h1 class="h3 mb-0 text-gray-800">Projects</h1>
					<button type="button" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm" data-toggle="modal" data-target="#new-project-modal"><i class="fas fa-plus fa-sm text-white-50"></i> New project</button>
				</div>
			</div>
		</div>

		<div class="row">
			<div class="offset-lg-1 col-lg-10">

				<div class="row">

					<div class="col-lg-12">
						<div id="alerts_fail"  class="alert alert-danger collapse" role="alert">
							Project creation failed.
							<button type="button" class="close" data-dismiss="alert" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
						</div>
							
						<div id="alerts_success" class="alert alert-success collapse" role="alert">
							Project created successfully.
							<button type="button" class="close" data-dismiss="alert" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
						</div>
					</div>
				</div>


				<div class="row">

					<div class="table-responsive">
						<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">

							<thead>
								<tr>
									<th>Name</th>
									<th>Type</th>
									<th>Created</th>
									<th>ID</th>
								</tr>
							</thead>

							<tbody>
								<tr class="project" v-for="project in projects" :key="project.id">
									<th>
										<router-link :to="{name: 'Project', params: {project_id: project.id}}">
											{{ project.name }}
										</router-link>
									</th>
									<th>{{project.type}}</th>
									<th>{{project._created_at}}</th>
									<th>{{project.id}}</th>
								</tr>
							</tbody>

						</table>
					</div>
				</div>
			</div>
		</div>


		<!-- The Modal -->
		<div class="modal" id="new-project-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<!-- Modal Header -->
					<div class="modal-header">
						<h4 class="modal-title">New project</h4>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<!-- Modal body -->
					<div class="modal-body">
						<div class="form-group">
							<label for="exampleInputEmail1">Name</label>
							<input type="text" class="form-control" id="project_name_id" placeholder="Enter project name">
						</div>

						<div class="form-group">
							<label for="exampleInputEmail1">Type</label>
							<select class="form-control" id = "project-type">
								<option value="ImageClassification">ImageClassification</option>
								<option value="ImageCaptioning">ImageCaptioning</option>
								<option value="ObjectDetection">ObjectDetection</option>
								<option value="Media2Text">Media2Text</option>
								<!-- <option value="AudioTranscription">Audio Transcription</option> -->
							</select>		
						</div>
										
						<div class="form-group">
							<label for="exampleInputEmail1">Description</label>
							<input type="text" class="form-control" id="project_description_id" placeholder="Enter project description">	
						</div>
						
					</div>

					<!-- Modal footer -->
					<div class="modal-footer">
						<button type="button" class="btn btn-primary" data-dismiss="modal" @click="createNewProjectClicked">Create</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>

	</div>
</template>

<script src = "./Projects.js">