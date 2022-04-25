<template>
	<div>
		
		<div class="table-responsive">
			<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">

				<thead>
					<tr>
						<th>#</th>
						<th>Name</th>
<!-- 						<th>Comment</th>
						<th>Start datetime</th>
						<th>End datetime</th>
						<th>IP</th>
						<th>User ID</th>
						<th>Commit URL</th>
						<th></th>
						<th></th> -->
					</tr>
				</thead>

				<tbody>
					<tr class="dataset" v-for="(dataset, ind) in datasets" :key="ind">
						<td>{{ind + 1}}</td>
						<td>
							<router-link :to="{name: 'PublicDataset', params: {dataset: dataset.name, type: 'Train', page: 1,}}">{{dataset.name}}</router-link>
						</td>
<!-- 						<td>{{run.short_comment}}</td>
						<td>{{run.start_time}}</td>
						<td>{{run.finish_time}}</td>
						<td>{{run.remote_address}}</td>
						<td>{{run.user_id}}</td>
						<td>
							<a :href="run.git_commit_url">{{run.git_commit_url}}</a>
						</td>
						<td>
							<a href="#" data-toggle="modal" data-target="#edit-modal" @click="setActiveRun(run._id)">
								<i class="fas fa-edit"></i>
							</a>
						</td>
						<td>
							<a href="#" data-toggle="modal" data-target="#delete-modal">
								<i class="fas fa-trash"></i>
							</a>
						</td> -->
					</tr>
				</tbody>

			</table>
		</div>


	</div>
</template>

<script src="./PublicDatasets.js"></script>