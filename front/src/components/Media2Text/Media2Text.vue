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
								
								<div class="col-lg-11 text-right">
									<div class="btn-group" role="group">

										<button type="button" class="btn btn-info btn-sm" data-toggle="modal" data-target="#edit-modal"><i class="far fa-edit"></i></button>

										<button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#delete-file-modal"><i class="fas fa-trash"></i></button>
									</div>
								</div>
							</div>

							<br/>

							<div class="row">
								<div class="col-lg-12">
									<p>File id: {{media.uploaded_file_name}}</p>
								</div>
							</div>

							<div class="row">
								<div class="col col-lg-2"></div>

								<div v-if="media.path" class="col col-lg-9">

									<div v-if="media.type == 'audio'">
										<audio controls>
											<source :src="media.path" type="audio/mpeg">
										</audio>
									</div>

									<div v-else>
										<video style="max-width:100%; height:auto" controls>
											<source :src="media.path" type="video/mp4">
											Your browser does not support the video tag.
										</video>
									</div>

								</div>

								<div class="col col-lg-1"></div>
							</div>

							<br/>

							<div class="row">
								<div class="col-lg-12">
									<div class="row">
										<div class="col col-lg-2"></div>
										<div class="col-lg-8">
											<div id="gold">{{media.gold}}</div>
										</div>
										<div class="col col-lg-2"></div>
									</div>

								</div>
							</div>

						</div>
					</div>
				</div>
			</div>
		</div>


		<!-- The Modal -->
		<div class="modal" id="edit-modal">
			<div class="modal-dialog modal-lg">
				<div class="modal-content">

					<!-- Modal Header -->
					<div class="modal-header">
						<h4 class="modal-title">Edit text</h4>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<!-- Modal body -->
					<div class="modal-body">										
						<div class="form-group">
							<textarea type="text" rows="10" class="form-control" id="text" placeholder="Enter text..." :value="media.gold"></textarea>
						</div>
					</div>

					<!-- Modal footer -->
					<div class="modal-footer">
						<button type="button" class="btn btn-primary" data-dismiss="modal" @click="updateTranscript">OK</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
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

<script src="./Media2Text.js"></script>