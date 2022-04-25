<template>
	<div>
		<div class="container_tabs_pills">	

			<div class="tab-content">
				<div class="tab-pane fade show active" id="tab-data">

					<ul class="nav nav-tabs" id="myTab" role="tablist">
						<li class="nav-item">
							<router-link id="logs" data-toggle="tab" class="nav-link" :to="{ name: 'Run', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="logs" aria-selected="false">
							Logs
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="analysis" data-toggle="tab" class="nav-link" :to="{ name: 'Analysis', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="logs" aria-selected="false">
							Analysis
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="training-data-tab" data-toggle="tab" class="nav-link" :to="{ name: project.settings.datasets[0].training, params: {project_id: projectId, page_nr: 1}}" role="tab" aria-controls="training-data" aria-selected="true">
							Training data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="validate-data-tab" data-toggle="tab" class="nav-link" :to="{ name: project.settings.datasets[1].training, params: {project_id: projectId, page_nr: 1}}" role="tab" aria-controls="validate-data" aria-selected="true">
							Validation data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="test-data-tab" data-toggle="tab" class="nav-link" :to="{ name: project.settings.datasets[2].training, params: {project_id: projectId, page_nr: 1, }}" role="tab" aria-controls="test-data" aria-selected="true">
							Test data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link data-toggle="tab" class="nav-link active" :to="{ name: 'RunFiles', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-selected="true">
							Files
							</router-link>
						</li>
					</ul>

					<div class="tab-content">
						<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
							<div class="card shadow mb-4 col mr-2"> 
								<div class="card-body">

									<div class="row">
										<div class="col-lg-2"></div>

										<div class="col-lg-10 text-right">
											<div role="group" aria-label="Basic example" class="btn-group">
												<button type="button" class="btn btn-success btn-sm" @click="downloadSourceCode"><i class="fas fa-download"></i> Download code</button>
											</div>
										</div>
									</div>

									<br/>


									<div class="table-responsive">
										<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
											<!-- <caption>Uploaded files : </caption> -->
											<thead>
												<tr>
													<!-- <th>#</th> -->
													<!-- <th>Role</th> -->
													<!-- <th>File</th> -->
													<!-- <th>Uploaded</th> -->
													<!-- <th>Comment</th> -->
												</tr>
											</thead>
											<tbody>

												<tr v-if="pathMatch!=''">
													<td>
														<router-link :to="buildRootUrl()">
															<span> ..</span>
														</router-link>
													</td>
												</tr>

												<tr v-for="(file, i) in files" :key="file._id">
													<!-- <td>{{i + 1}}</td> -->
													<!-- <td>{{file.role_name}}</td> -->
													<td>
														<router-link :to="file.url">
															<span v-if="file.type == 'directory'"><i class="fas fa-folder"></i></span>
															<span v-else><i class="far fa-file"></i></span>
															<span> {{file.name}}</span>
														</router-link>
													</td>
													<!-- <td>{{file.upload_time}}</td> -->
													<!-- <td>{{file.comment}}</td> -->
												</tr>
											</tbody>
										</table>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

		</div>
	</div>

</template>

<script src="./RunFiles.js"></script>