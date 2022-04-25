<template>
	<ImageClassification v-bind="{ dataSourcePath: 'gold-training-data', downloadPath: 'training-set', uploadPath: 'upload-training-data', imagePath: 'all-dataset-file', templateName: 'DataImageClassificationTrainingData', datasetType: 'Train' }"></ImageClassification>
</template>

<script src="./TrainingData.js"></script>