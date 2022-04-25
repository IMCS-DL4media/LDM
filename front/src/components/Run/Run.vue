<template>
	<div>
				
		<div class="container_tabs_pills">
			<div class="tab-content">
				<div class="tab-pane fade show active" id="tab-data">

					<ul class="nav nav-tabs" id="myTab" role="tablist">
						<li class="nav-item">
							<router-link id="logs-tab" data-toggle="tab" class="nav-link active" :to="{ name: 'RunFiles', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="training-data" aria-selected="false">
							Logs
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="anlaysis" data-toggle="tab" class="nav-link" :to="{ name: 'Analysis', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="logs" aria-selected="false">
							Analysis
							</router-link>
						</li>

						<li class="nav-item" v-for="dataset in project.settings.datasets">
							<router-link data-toggle="tab" class="nav-link" :to="{name: dataset.name, params: {project_id: dataset.run.project_id, run_id: dataset.run._id, page_nr: 1,}}" role="tab" aria-selected="true">
								{{dataset.title}}
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="files-tab" data-toggle="tab" class="nav-link" :to="{ name: 'RunFiles', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-selected="true">
							Files
							</router-link>
						</li>

					</ul>

					<div class="tab-content">
						<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
							<div class="card shadow mb-4 col mr-2"> 
								<div class="card-body">

									<div class="row1">
										<!-- <p>RunId: {{run._id}}</p> -->
										<!-- <p>Comment: {{run.comment}}</p> -->
										<p>RunId: {{runId}} Started at: {{run._start_time}}</p>

<!-- 										<div class="btn-group" role="group">
											<router-link v-for="dataset in project.settings.datasets" :to="{name: dataset.name, params: {project_id: dataset.run.project_id, run_id: dataset.run._id, page_nr: 1,}}">

												<button type="button" class="btn btn-success">
													{{dataset.title}}
												</button>
											</router-link>
										</div> -->
									</div>

									<br/>

									<div class="table-responsive">
										<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
									
											<thead>
												<tr>
													<th>#</th>
													<th>Log</th>
													<th>Time</th>
												</tr>
											</thead>

											<tbody>
												<tr v-if="log.type=='file'" v-for="(log, i) in logs" :key="log._id">
													<td>{{ i + 1 }}</td>
													<td > 
														<a href="#" @click="downloadFile(log.body.file_name)">
															{{log.body.comment || log.body.file_name}} 
														</a>

														<router-link v-if="log.body.file_opened" :to="{name: 'LoggedFile', params: {project_id: projectId, run_id: runId,}, query: {path: log.body.file_name,}}" class="small" >
															<i class="fas fa-eye "></i>
														</router-link>
													</td>

													<td>{{ log._time }}</td>
												</tr>

												<tr v-else :key="log._id">
													<td>{{ i + 1 }}</td>
													<td>{{ log._msg }}</td>
													<td>{{ log._time }}</td>
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

<script src="./Run.js"></script>