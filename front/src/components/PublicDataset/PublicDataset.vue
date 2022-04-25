<template>
	<div>
		<div class="container_tabs_pills">			

			<div class="tab-content">
				<div class="tab-pane fade show active" id="tab-data">

					<ul class="nav nav-tabs" id="myTab" role="tablist">
						<li class="nav-item">
							<router-link id="training-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.ImageClassificationTrainingData" :to="{ name: 'ImageClassificationTrainingData', params: {project_id: projectId }}" role="tab" aria-controls="training-data" aria-selected="false">
							Training data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="validate-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.ImageClassificationValidateData" :to="{ name: 'ImageClassificationValidateData', params: {project_id: projectId }}" role="tab" aria-controls="test-data" aria-selected="true">
							Validation data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="test-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.ImageClassificationTestData" :to="{ name: 'ImageClassificationTestData', params: {project_id: projectId }}" role="tab" aria-controls="test-data" aria-selected="true">
							Test data
							</router-link>
						</li>
					</ul>

					<div class="tab-content" id="myTabContent2">
						<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
							<div class="card shadow mb-4 col mr-2"> 
								<div class="card-body">

									<div class="row">
<!-- 										<div class="col-lg-2">
					                    	<select class="form-control form-control-sm" @change="runChanged($event)" id="runs" v-model="runId">
					                        	<option value="None">None</option>
					                            <option v-for="run in runs" :value="run._id">{{run._id}}</option>
					                    	</select>
					                    </div> -->
										
										<div class="col-lg-10 text-right">
		<!-- 									<div class="btn-group" role="group" aria-label="Basic example">
												<button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#data-modal"><i class="fas fa-upload"></i></button>
												<button type="button" class="btn btn-primary btn-sm" @click="download"><i class="fas fa-download"></i></button>
											</div> -->

											<div>
												<form class="form-horizontal">
													<p>Total {{totalImages}}</p>
												</form>
											</div>
										</div>
									</div>

						            <div class="row">
						                <div class="col-sm-9">        
						                    <div class="row">

						                        <div class="col" v-for="p in images">
						                            <div>
						                            	<img height="150" width="150" :src="p.path">
					                        			<div class="mb-3">
				                        					{{p.class}}
				                        				</div>
						                            </div>
						                        </div>
						                    </div>

											<nav aria-label="Page navigation example" >
						                        <ul class="pagination justify-content-center">

						                            <li class="page-item" v-bind:class="{ disabled: isPrevEnabled }">
						                            	<router-link class="page-link" :to="{ name: 'PublicDataset', params: {dataset: this.dataset, dataset_type: this.datasetType, page: this.currentPage + 2,}}">Previous</router-link>
						                            </li>

						                            <!-- <li class="page-item"><a class="page-link" href="#">1</a></li> -->
						                            <!-- <li class="page-item"><a class="page-link" href="#">2</a></li> -->
						                            <!-- <li class="page-item"><a class="page-link" href="#">3</a></li> -->

						                            <li class="page-item" v-bind:class="{ disabled: isNextEnabled }">
						                            	<router-link class="page-link" :to="{ name: 'PublicDataset', params: {dataset: this.dataset, dataset_type: this.datasetType, page: this.currentPage + 2,}}">Next</router-link>
						                            </li>
						    

						                        </ul>
											</nav>					    				
						                </div>


					                	<div class="col-sm-3">

						                    <div v-for="cl in labels" :key="cl._id">
						                        <span v-if="isDebugMode" class="font-weight-bolder h5">
						                            <input type="checkbox" class="label-checkbox" :id="cl._id" checked @click="checkboxClicked( cl, 'id' + cl )"> {{cl.category}}
						                            ({{cl.goldCount + "/" + cl.silverCount}})
						                        </span>

						                        <span v-else class="font-weight-bolder h5">
						                            <input type="checkbox" class="label-checkbox" :id="cl._id" checked @click="checkboxClicked( cl, 'id' + cl )"> {{cl.category}} ({{cl.goldCount}})
						                        </span>
						                    </div>

					                    	<br/>
					                    
					                    	<button type="button" class="btn btn-info mr-2" @click="selectAllCheckboxes()">Select all</button>
					                    	<button type="button" class="btn btn-default"  @click="clearAllCheckboxes()">Clear all</button>
					                  
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

<script src="./PublicDataset.js"></script>