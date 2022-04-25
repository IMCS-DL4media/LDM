<template id="ObjectDetection">
	<div>
	
		<div class="container_tabs_pills">
			<div class="tab-content">
				<div class="tab-pane fade show active" id="tab-data">

					<div class="tab-content" id="myTabContent2">
						<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
							<div class="card shadow mb-4 col mr-2"> 
								<div class="card-body">

									<div class="row">
										<div class="col-lg-12 text-right">
											<div>
												<form class="form-horizontal">
													<p>Total {{total}}</p>
												</form>
											</div>
										</div>
									</div>

						            <div v-if="!isLoading" class="row">
						                <div class="col-sm-12">        
						                    <div class="row">
						                        <div class="col-sm-2" v-for="p in images">
						                            <div style="position:relative;">
						                            	<img :src="p.path" :style="p.height">

					                            		<div v-for="pos in p.positions" class="bbox" :style="pos.style">
					                            			<div :style="pos.labelStyle">
					                            				{{ pos.label }}
					                            			</div>
					                            		</div>
						                            </div>
						                        </div>
						                    </div>

											<nav aria-label="Page navigation example" style="margin-top:10px;">
						                        <ul class="pagination justify-content-center">

													<li class="page-item " v-bind:class="{ disabled: isPrevEnabled }">
														<span class="page-link" >
															<router-link :to="{ name: 'ProductionDataImageClassification', params: {project_id: projectId, model_id: modelId, page_nr: currentPage-1}}">
																Previous
															</router-link>
														</span>
													</li>

													<li v-for="button in paginationButtons" class="page-item " v-bind:class="{active: button.active,}">
														<span v-if="button.active == 'active'" class="page-link active">
															{{button.index}}
															<span class="sr-only">(current)</span>
														</span >

														<a v-else class="page-link active" >
															<router-link :to="{ name: 'ProductionDataImageClassification', params: {project_id: projectId, model_id: modelId, page_nr: button.index}}">
																{{button.index}}
															</router-link>
														</a >
													</li>

													<li class="page-item " v-bind:class="{ disabled: isNextEnabled }">
														<span class="page-link" >
															<router-link :to="{ name: 'ProductionDataImageClassification', params: {project_id: projectId, model_id: modelId, page_nr: currentPage+1}}">
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
						                            <input type="checkbox" class="label-checkbox label" :id="cl._id" checked @change="filterModeChanged()"> {{cl.category}}
						                            ({{cl.silverCount}})
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