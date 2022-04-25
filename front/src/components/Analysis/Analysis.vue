<template id="Analysis">
	<div>
	
		<div class="container_tabs_pills">
			<div class="tab-content">
				<div class="tab-pane fade show active" id="tab-data">

					<ul class="nav nav-tabs" role="tablist">

						<li class="nav-item">
							<router-link id="logs-tab" data-toggle="tab" class="nav-link"  :to="{ name: 'Run', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="logs" aria-selected="false">
							Logs
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="analysis" data-toggle="tab" class="nav-link active"  :to="{ name: 'Analysis', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="logs" aria-selected="false">
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
							<router-link id="files-tab" data-toggle="tab" class="nav-link" :to="{ name: 'RunFiles', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="files-tab" aria-selected="true">
							Files
							</router-link>
						</li>

					</ul>

					<div class="tab-content" id="myTabContent2">
						<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
							<div class="card shadow mb-4 col mr-2"> 
								<div class="card-body">

									<div class="row">
										<div class="col-lg-12">
											<div class="d-sm-flex align-items-center justify-content-between">
												<button class="btn btn-sm btn-primary shadow-sm" @click="reloadPage">
													<i class="fas fa-sync"></i>
												</button>

												<button type="button" class="btn btn-sm btn-primary shadow-sm" data-toggle="modal" data-target="#add-chart-modal">
													<i class="fas fa-plus fa-sm"></i> Add Chart
												</button>
											</div>
											<br>
										</div>
									</div>

									<!-- https://github.com/ankane/vue-chartkick -->
									<div class="row">
										<div :class="'col-lg-' + chart.width " v-for="chart in charts" :key="chart._id">
											
											<div class="row">
												<div class="col-lg-12">
													<div class="d-sm-flex align-items-center justify-content-between">
														<span>{{chart.title}} ({{chart._id}})</span>
														<button @click="addData(chart._id)">Add data</button>
														<a href="#" class="btn btn-danger btn-circle btn-sm" data-toggle="modal" data-target="#delete-chart-modal" @click="openDeleteChartForm(chart._id)"><i class="fas fa-trash"></i></a>
													</div>
												</div>
											</div>

											<div v-if="chart.type=='line-chart'">
												<line-chart :data="chart.data" :xtitle="chart.xtitle" :ytitle="chart.ytitle"/>
											</div>

											<div v-if="chart.type=='column-chart'">
												<column-chart :data="chart.data" :xtitle="chart.xtitle" :ytitle="chart.ytitle" />
											</div>
											<br>
										</div>
									</div>

								</div>
							</div>
						</div>
					</div>
				</div>	
			</div>
		</div>

		<div class="modal" id="add-chart-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title">Add chart</h5>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<div class="modal-body">
						<div class="form-group">
							<label for="chart-title">Title</label>
							<input type="text" class="form-control" id="chart-title">
						</div>

						<div class="form-group">
							<label for="chart-type">Type</label>
							<select class="form-control" id="chart-type">
								<option :value="chartType.type" v-for="chartType in chartTypes" :key="chartType.type">{{chartType.type}}</option>
							</select>		
						</div>

						<div class="form-group">
							<label for="chart-xtitle">xTitle</label>
							<input type="text" class="form-control" id="chart-xtitle">
						</div>

						<div class="form-group">
							<label for="chart-ytitle">yTitle</label>
							<input type="text" class="form-control" id="chart-ytitle">
						</div>

						<div class="form-group">
							<label for="chart-width">Width</label>
							<input type="number" min="1" max="12" value="12" class="form-control" id="chart-width">
						</div>

					</div>

					<div class="modal-footer">
						<button type="button" class="btn btn-success" data-dismiss="modal" @click="addChart">OK</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>


		<div class="modal" id="delete-chart-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title">Delete chart. Are you ABSOLUTELY SURE?</h5>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<div class="modal-body">
						<div class="alert alert-danger" role="alert">
							You are about to permanently delete this chart. Once a chart is permanently deleted it cannot be recovered.
						</div>

<!-- 						<div class="form-group">
							<label for="confirm-field">Please type the project name to confirm: </label>
							<input type="text" class="form-control" id="confirm-field" placeholder="Enter project name">	
						</div> -->

					</div>

					<div class="modal-footer">
						<button type="button" class="btn btn-danger" data-dismiss="modal" @click="deleteChart">Delete</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>

	</div>
</template>

<script src="./Analysis.js"></script>