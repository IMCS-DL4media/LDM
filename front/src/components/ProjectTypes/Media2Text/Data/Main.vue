<template id="Media2Text">
	<div>
	
		<div class="container_tabs_pills">			

			<div class="tab-content">
				<div class="tab-pane fade show active" id="tab-data">

					<ul class="nav nav-tabs" id="myTab" role="tablist">

						<li class="nav-item">
							<router-link id="all-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.DataMedia2TextAllData" :to="{ name: 'DataMedia2TextAllData', params: {project_id: projectId }}" role="tab" aria-controls="training-data" aria-selected="false">
							All data
							</router-link>
						</li>

<!-- 						<li class="nav-item">
							<router-link id="training-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.DataMedia2TextTrainingData" :to="{ name: 'DataMedia2TextTrainingData', params: {project_id: projectId }}" role="tab" aria-controls="training-data" aria-selected="false">
							Training data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="validate-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.DataMedia2TextValidateData" :to="{ name: 'DataMedia2TextValidateData', params: {project_id: projectId }}" role="tab" aria-controls="test-data" aria-selected="true">
							Validation data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="test-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.DataMedia2TextTestData" :to="{ name: 'DataMedia2TextTestData', params: {project_id: projectId }}" role="tab" aria-controls="test-data" aria-selected="true">
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
											<div class="btn-group" role="group" aria-label="Basic example">
												<button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#upload-modal"><i class="fas fa-upload"></i></button>
												<!-- <button type="button" class="btn btn-primary btn-sm" @click="download"><i class="fas fa-download"></i></button> -->
											</div>

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
															<router-link :to="{name: 'Media2Text', params: {id: m._id, filePath: filePath, projectId: projectId}}">
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
							        </div>
								</div>
							</div>
						</div>
					</div>
				</div>	
			</div>
		</div>

		<div class="modal" id="upload-modal">
			<div class="modal-dialog">
				<div class="modal-content">
					
					<div class="modal-header">
						<h4 class="modal-title">Upload</h4>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<div class="modal-body">
						<div class="form-group">
							<!-- <div class="file-loading"> -->
								<input id="upload-file" type="file" ref="input_ref" multiple>
							<!-- </div>	 -->
						</div> 
					</div>
					
					<div class="modal-footer">
						<button type="button" class="btn btn-primary" data-dismiss="modal" @click="uploadFile">Upload</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>

	</div>
</template>

<script src="./Main.js"></script>