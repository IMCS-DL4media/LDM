<template id="ImageClassification">
	<div>
	
		<div class="modal" id="data-modal">
			<div class="modal-dialog">
				<div class="modal-content">
					
					<div class="modal-header">
						<h4 class="modal-title">Upload dataset</h4>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>
	
					<div class="modal-body">
						<div class="form-group ">
							<!-- <label for="fset1"> Dataset specification kind: </label> -->
							<fieldset id="fset1">
								<div class="form-check-inline">
									<label class="form-check-label">
										<input class="form-check-input" type="radio" name="dataset_spec_kind" id="dataset_spec_kind_predefined" value="PredefinedDataSet" checked v-model="dataset_spec_kind"> Use predefined dataset
									</label>
								</div>
								<div class="form-check-inline">
									<label class="form-check-label">
										<input class="form-check-input" type="radio" name="dataset_spec_kind" id="dataset_spec_kind_ZIP" value="ZIP" v-model="dataset_spec_kind"> Upload zip 
									</label>
								</div>
<!-- 								<div class="form-check-inline" disabled>
									<label class="form-check-label" disabled>
										<input class="form-check-input" type="radio" name="dataset_spec_kind" id="dataset_spec_kind_URL" value="URL" v-model="dataset_spec_kind" disabled> URL
									</label>
								</div> -->
							</fieldset>
						</div>

						<div class="form-group" v-show="dataset_spec_kind == 'ZIP'">
							<div class="file-loading">
								<input id="file_input_id" name="test_file_input" type="file" ref="data_fileInputRef" accept=".zip">
							</div>	
						</div> 

						<div class="form-group" v-show="dataset_spec_kind == 'PredefinedDataSet'">
							<label for="project-type">Predefined Datasets:</label>
							<select class="form-control" id="predefined_dataset_id">
								<option v-for="dataset in predefined_datasets" :value="dataset._id">
									{{dataset.name}} - {{dataset.dataset_type}}
								</option>
							</select>
						</div>
					</div>
					
					<div class="modal-footer">
						<button type="button" class="btn btn-primary" data-dismiss="modal" @click="uploadDataSetClicked">Upload</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>


		<div class="modal" id="shuffle-modal">
			<div class="modal-dialog">
				<div class="modal-content">
					
					<div class="modal-header">
						<h4 class="modal-title">Shuffle modal</h4>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>
	
					<div class="modal-body">
<!-- 						<div class="form-group ">
							<label for="fset1"> Dataset specification kind: </label>
							<fieldset id="fset1">
								<div class="form-check-inline">
									<label class="form-check-label">
										<input class="form-check-input" type="radio" name="dataset_spec_kind" id="dataset_spec_kind_predefined" value="PredefinedDataSet" checked v-model="dataset_spec_kind"> Use predefined dataset
									</label>
								</div>
								<div class="form-check-inline">
									<label class="form-check-label">
										<input class="form-check-input" type="radio" name="dataset_spec_kind" id="dataset_spec_kind_ZIP" value="ZIP" v-model="dataset_spec_kind"> Upload zip 
									</label>
								</div>
								<div class="form-check-inline" disabled>
									<label class="form-check-label" disabled>
										<input class="form-check-input" type="radio" name="dataset_spec_kind" id="dataset_spec_kind_URL" value="URL" v-model="dataset_spec_kind" disabled> URL
									</label>
								</div>
							</fieldset>
						</div> -->

<!-- 						<div class="form-group" v-show="dataset_spec_kind == 'ZIP'">
							<div class="file-loading">
								<input id="file_input_id" name="test_file_input" type="file" ref="data_fileInputRef" accept=".zip">
							</div>	
						</div> 

						<div class="form-group" v-show="dataset_spec_kind == 'PredefinedDataSet'">
							<label for="project-type">Predefined Datasets:</label>
							<select class="form-control" id="predefined_dataset_id">
								<option v-for="dataset in predefined_datasets" :value="dataset._id">
									{{dataset.name}} - {{dataset.dataset_type}}
								</option>
							</select>
						</div> -->
					</div>
					
					<div class="modal-footer">
						<button type="button" class="btn btn-primary" data-dismiss="modal" @click="shuffleClicked">Shuffle</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>



		<div class="container_tabs_pills">			
<!-- 			<ul class="nav nav-pills">
				<li class="nav-item">
					<router-link :to="{ name: 'Project', params: {project_id: projectId}}" class="nav-link" role="tab" data-toggle="tab">
						Runs
					</router-link>
				</li>
				<li class="nav-item">
					<li class="nav-item">
						<router-link :to="{ name: 'ImageClassificationTrainingData', params: {project_id: projectId, page_nr: 1}}" class="nav-link active" role="tab" data-toggle="tab">
							Data 
						</router-link>
					</li>
				</li>		
			</ul> -->

<!-- 			<div class="row">
				<div class="col-lg-12 text-right">
					<div class="btn-group" role="group">
						<button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#data-modal"><i class="fas fa-upload"></i></button>
						<button type="button" class="btn btn-primary btn-sm" @click="download"><i class="fas fa-download"></i></button>
					</div>
				</div>
			</div> -->

			<div class="tab-content">
				<div class="tab-pane fade show active" id="tab-data">

					<ul class="nav nav-tabs" id="myTab" role="tablist">

						<li class="nav-item">
							<router-link id="all-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.DataImageClassificationAllData" :to="{ name: 'DataImageClassificationAllData', params: {project_id: projectId, }}" role="tab" aria-controls="all-data" aria-selected="false">
							All data
							</router-link>
						</li>

<!-- 						<li class="nav-item">
							<router-link id="training-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.DataImageClassificationTrainingData" :to="{ name: 'DataImageClassificationTrainingData', params: {project_id: projectId, }}" role="tab" aria-controls="training-data" aria-selected="true">
							Training data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="validate-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.DataImageClassificationValidateData" :to="{ name: 'DataImageClassificationValidateData', params: {project_id: projectId, page_nr: 1}}" role="tab" aria-controls="test-data" aria-selected="true">
							Validation data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="test-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.DataImageClassificationTestData" :to="{ name: 'DataImageClassificationTestData', params: {project_id: projectId, page_nr: 1, }}" role="tab" aria-controls="test-data" aria-selected="true">
							Test data
							</router-link>
						</li> -->
					</ul>

					<div class="tab-content" id="myTabContent2">
						<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
							<div class="card shadow mb-4 col mr-2"> 
								<div class="card-body">

									<div class="row">
										
										<div class="col-lg-12 text-right">
											<div class="btn-group" role="group" aria-label="buttons">
												<!-- <button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#shuffle-modal"><i class="fab fa-mix"></i></button> -->

												<button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#data-modal"><i class="fas fa-upload"></i></button>
												
												<button type="button" class="btn btn-primary btn-sm" @click="download"><i class="fas fa-download"></i></button>
											</div>

											<div>
												<form class="form-horizontal">
													<p>Total {{total}}</p>
												</form>
											</div>
										</div>
									</div>

						            <div v-if="!isLoading" class="row">
						                <div class="col-sm-9">        
						                    <div class="row">
						                        <div class="col" v-for="p in images">
							                        <!-- <img height="150" width="150" :src="p.path"> -->
							                        <!-- <div>Gold label: {{currClassName}}</div> -->
							                        <!-- <div>Silver label : Sunflower</div> -->
							                        <!-- <div>File name: {{p.name}}</div> -->


						                            <!-- <img height = "150" width = "150" :src=" SERVER_URL() + 'get_testing_file/' + p + `?project_id=` + project_id "  > -->
						                            <!-- <div> <span class = "font-weight-bolder h6" >Gold label : </span>{{currClassName}}</div> -->

						                            <div>
						                            	<img :src="p.path" style="max-height:150px;">
					                        			<div class="mb-3">
				                        					{{p.gold}}
				                        				</div>
						                            </div>
						                        </div>
						                    </div>

											<nav aria-label="Page navigation example" >
						                        <ul class="pagination justify-content-center">

													<li class="page-item " v-bind:class="{ disabled: isPrevEnabled }">
														<span class="page-link" >
															<router-link :to="{ name: templateName, params: {project_id: projectId, run_id: runId, page_nr: currentPage-1}}">
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
															<router-link :to="{ name: templateName, params: {project_id: projectId, run_id: runId, page_nr: button.index}}">
																{{button.index}}
															</router-link>
														</a >
													</li>

													<li class="page-item " v-bind:class="{ disabled: isNextEnabled }">
														<span class="page-link" >
															<router-link :to="{ name: templateName, params: {project_id: projectId, run_id: runId, page_nr: currentPage+1}}">
																Next
															</router-link>
														</span>
													</li>
													
						                        </ul>
											</nav>					    				
						                </div>

					                	<div class="col-sm-3">
						                    <div v-for="cl in labels" :key="cl._id">
						                        <span class="font-weight-bolder h5">
						                            <input type="checkbox" class="label-checkbox label" :id="cl._id" checked @change="filterModeChanged()"> {{cl.category}} ({{cl.goldCount}})
						                        </span>
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
	</div>
</template>

<script src="./Main.js"></script>