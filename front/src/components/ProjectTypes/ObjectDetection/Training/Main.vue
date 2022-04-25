<template id="ImageClassification">
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
							<router-link id="analysis" data-toggle="tab" class="nav-link"  :to="{ name: 'Analysis', params: {run_id: runId, project_id: projectId,}}" role="tab" aria-controls="logs" aria-selected="false">
							Analysis
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="training-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.Train" :to="{ name: 'TrainObjectDetectionTrainingData', params: {project_id: projectId, }}" role="tab" aria-controls="training-data" aria-selected="true">
							Training data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="validate-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.Validate" :to="{ name: 'TrainObjectDetectionValidateData', params: {project_id: projectId, page_nr: 1}}" role="tab" aria-controls="validate-data" aria-selected="true">
							Validation data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="test-data-tab" data-toggle="tab" class="nav-link" :class="activeTab.Test" :to="{ name: 'TrainObjectDetectionTestData', params: {project_id: projectId, page_nr: 1, }}" role="tab" aria-controls="test-data" aria-selected="true">
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
										<div class="col-lg-3">
											<!-- <label for="sel1" class="my-1 mr-2">Run</label> -->
					                    	<select class="form-control form-control-sm" @change="runChanged($event)" id="runs" v-model="runId">
					                            <option v-for="run in runs" :value="run._id">{{run._id}}</option>
					                    	</select>
					                    </div>
										
									</div>

									<br/>

						            <div v-if="!isLoading" class="row">
						                <div class="col-sm-9">        
						                    <div class="row">
						                        <div class="col-sm-2" v-for="p in images">
						                            <!-- <div> -->
						                            	<!-- <img :src="p.path" style="max-height:150px;"> -->
<!-- 					                        			<div class="mb-3" :class="p.textStyle">
					                        				{{p.gold}} / {{p.silver}}
					                        			</div> -->

						                            <div style="position:relative;">
						                            	<img :src="p.path" :style="p.height">

					                            		<div v-for="pos in p.goldPositions" class="gold-bbox" :style="pos.style">
					                            			<div :style="pos.labelStyle">
					                            				{{ pos.label }}
					                            			</div>
					                            		</div>

					                            		<div v-for="pos in p.silverPositions" class="bbox" :style="pos.style">
					                            			<div :style="pos.labelStyle">
					                            				{{ pos.label }}
					                            			</div>
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

<!-- 						                    <div class="form-group">
						                        <fieldset id="filter-options" @change="filterModeChanged()"  >
						                            <div class="form-check-inline">
						                                <label class="form-check-label" >
						                                    <input class="form-check-input" type="radio" name="binding" id="binding_provided" value="all" checked v-model="filter.active"> All
						                                </label>
						                            </div>
						                            
						                            <br/>
						                            
						                            <div class="form-check-inline">
						                                <label class="form-check-label" >
						                                    <input class="form-check-input" type="radio" name="binding" id="binding_weak" value="match" v-model="filter.active"> Matching (Gold == Silver)
						                                </label>
						                            </div>
						                            
						                            <br/>

						                            <div class="form-check-inline">
						                                <label class="form-check-label" >
						                                    <input class="form-check-input" type="radio" name="binding" id="binding_strong" value="mismatch" v-model="filter.active"> Mismatching (Gold != Silver)
						                                </label>
						                            </div>
						                            
						                        </fieldset>

						                        <hr>
						                    </div> -->

						                    <!-- <br/> -->

<!-- 						                    <div>
					                    		<button type="button" class="btn btn-info mr-2" @click="selectAllCheckboxes()">Select all</button>
					                    		<button type="button" class="btn btn-default"  @click="clearAllCheckboxes()">Clear all</button>
					                    	</div>

					                    	<br/> -->

<!-- 						                    <div v-for="cl in labels" :key="cl._id">
						                        <span class="font-weight-bolder h5">
						                            <input type="checkbox" class="label-checkbox label" :id="cl._id" checked @change="filterModeChanged()"> {{cl.category}}
						                            ({{cl.goldCount + "/" + cl.silverCount}})
						                        </span>
						                    </div> -->

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