<template>
	<ObjectDetection v-bind="{ dataSourcePath: 'silver-training-data', downloadPath: 'training-set', uploadPath: 'upload-training-data', imagePath: 'all-dataset-file', templateName: 'Train', datasetType: 'Train' }"></ObjectDetection>
</template>

<script src="./TrainingData.js"></script>