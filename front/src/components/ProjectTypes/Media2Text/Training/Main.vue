<template id="Media2Text">
	<div>
	
		<div class="container_tabs_pills">
			<div class="tab-content">
				<div class="tab-pane fade show active" id="tab-data">

					<ul class="nav nav-tabs" id="myTab" role="tablist">

						<li class="nav-item">
							<router-link id="logs-tab" data-toggle="tab" class="nav-link" :to="{ name: 'RunFiles', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="training-data" aria-selected="false">
							Logs
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="anlaysis" data-toggle="tab" class="nav-link" :to="{ name: 'Analysis', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="logs" aria-selected="false">
							Analysis
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="training-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.Train" :to="{ name: 'TrainMedia2TextTrainingData', params: {project_id: projectId }}" role="tab" aria-controls="training-data" aria-selected="false">
							Training data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="validate-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.Validate" :to="{ name: 'TrainMedia2TextValidateData', params: {project_id: projectId }}" role="tab" aria-controls="test-data" aria-selected="true">
							Validation data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="test-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.Test" :to="{ name: 'TrainMedia2TextTestData', params: {project_id: projectId }}" role="tab" aria-controls="test-data" aria-selected="true">
							Test data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="files-tab" data-toggle="tab" class="nav-link" :to="{ name: 'RunFiles', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-selected="true">
							Files
							</router-link>
						</li>

					</ul>

					<div class="tab-content" id="myTabContent2">
						<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
							<div class="card shadow mb-4 col mr-2"> 
								<div class="card-body">

									<div class="row">
										<div class="col-lg-3">
											<!-- <label for="sel1" class="my-1 mr-2">Run</label> -->
					                    	<select class="form-control form-control-sm" @change="runChanged($event)" id="runs" v-model="runId">
					                            <option v-for="run in runs" :value="run._id">{{run._id}}</option>
					                    	</select>
					                    </div>
										
										<div class="col-lg-12 text-right">
											<div>
												<form class="form-horizontal">
													<p>Total {{total}}</p>
												</form>
											</div>
										</div>
									</div>


						            <div class="row">
						                <div class="col-sm-12">        
						                    <div class="row">
						                        <div class="col-sm-3" v-for="m in media">
						                            <div>

						                            	<div v-if="m.type == 'audio'">
															<audio controls>
																<source :src="m._path" type="audio/mpeg">
															</audio>
														</div>

														<div v-else>
															<video width="320" controls>
																<source :src="m._path" type="video/mp4">
																Your browser does not support the video tag.
															</video>
														</div>

														<div class="mb-3">
															<router-link :to="{name: 'TrainingMedia2Text', params: {id: m._id, filePath: filePath, runId: runId, projectId: projectId}}">
																<div class="h5 mb-0 font-weight-bold text-gray-800"> 
																	{{ m.uploaded_file_name }}
																</div>
															</router-link>
					                        			</div>

						                            </div>
						                        </div>
						                    </div>

											<nav aria-label="Page navigation example" >
						                        <ul class="pagination justify-content-center">

													<li class="page-item " v-bind:class="{ disabled: isPrevEnabled }">
														<span class="page-link" >
															<router-link :to="{ name: currentTemplate, params: {project_id: projectId, run_id: runId, page_nr: currentPage-1}}">
																Previous
															</router-link>
														</span>
													</li>

													<li v-for="button in paginationButtons" class="page-item " v-bind:class="{active: button.active, }">
														<span v-if="button.active == 'active'" class="page-link active">
															{{button.index}}
															<span class="sr-only">(current)</span>
														</span >

														<a v-else class="page-link active" >
															<router-link :to="{ name: currentTemplate, params: {project_id: projectId, run_id: runId, page_nr: button.index}}">
																{{button.index}}
															</router-link>
														</a >
													</li>

													<li class="page-item " v-bind:class="{ disabled: isNextEnabled }">
														<span class="page-link" >
															<router-link :to="{ name: currentTemplate, params: {project_id: projectId, run_id: runId, page_nr: currentPage+1}}">
																Next
															</router-link>
														</span>
													</li>
													
						                        </ul>
											</nav>
															    				
						                </div>
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

<script src="./Main.js"></script>