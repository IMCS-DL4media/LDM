<template>
	<div>	
		<div class="container_tabs_pills">						
			<div class="tab-content" id="myTabContent2">
				<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
					<div class="card shadow mb-4 col mr-2"> 
						<div class="card-body">

							<div class="row">
								<div class="col-lg-1">
									<button type="button" class="btn btn-primary btn-sm" @click="back">Back</button>
								</div>

								<div class="col-lg-3">
									<!-- <label for="sel1" class="my-1 mr-2">Run</label> -->
			                    	<select class="form-control form-control-sm" @change="runChanged($event)" id="runs" v-model="runId">
			                        	<option value="None">None</option>
			                            <option v-for="run in runs" :value="run._id">{{run._id}}</option>
			                    	</select>
			                    </div>
								
								<div class="col-lg-8 text-right">
									<div class="btn-group" role="group" aria-label="Basic example">
										<button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#delete-file-modal"><i class="fas fa-trash"></i></button>
									</div>
								</div>
							</div>

							<br/>

							<div class="row">
								<div class="col-lg-12">
									<p>File name: {{media.uploaded_file_name}}</p>
								</div>
							</div>

							<br/>

							<div class="row">
								<div class="col-lg-8">
									<video :src="path" type="video/mp4" style="max-width:100%; height:auto" controls>
									</video>
								</div>
							</div>

							<br/>

							<div v-if="runId=='None'" class="row">
								<div class="col-lg-12">
									<div class="row">
										<div class="col-lg-8">
											<textarea id="gold" rows="10" placeholder="Enter transcript text..." :value="media.gold"></textarea>
										</div>
									</div>
									<div class="row">
										<div class="col-lg-8">
											<button type="button" class="btn btn-success btn-sm" @click="updateTranscript">Update</button>
										</div>
									</div>
								</div>
							</div>

							<div v-else class="row">
								<div class="col-lg-4">
									<p class="card-text">{{media.gold}}</p>
								</div>
								<div class="col-lg-2">
								</div>
								<div class="col-lg-4">
									<p class="card-text">{{media.silver}}</p>
								</div>
							</div>

						</div>
					</div>
				</div>
			</div>
		</div>


		<div class="modal" id="delete-file-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title">Delete file. Are you ABSOLUTELY SURE?</h5>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<!-- <div class="modal-body"> -->
<!-- 						<div class="alert alert-danger" role="alert">
							You are about to permanently delete this project. Once a project is permanently deleted it cannot be recovered. Permanently deleting this project will immediately delete its repositories and all related resources including datasets, runs etc.
						</div> -->

<!-- 						<div class="form-group">
							<label for="confirm-field">Please type the project name to confirm: </label>
							<input type="text" class="form-control" id="confirm-field" placeholder="Enter project name">	
						</div> -->
					<!-- </div> -->

					<div class="modal-footer">
						<button type="button" class="btn btn-danger" data-dismiss="modal" @click="deleteFile">Delete</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>

	</div>

</template>

<script src="./VideoTranscription.js"></script>