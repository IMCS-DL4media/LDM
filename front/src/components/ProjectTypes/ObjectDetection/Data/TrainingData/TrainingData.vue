<template>
	<ObjectDetection v-bind="{ dataSourcePath: 'gold-training-data', downloadPath: 'training-set', uploadPath: 'upload-training-data', imagePath: 'all-dataset-file', templateName: 'DataObjectDetectionTrainingData', datasetType: 'Train' }"></ObjectDetection>
</template>

<script src="./TrainingData.js"></script>