<template>
	<ImageCaptioning v-bind="{ dataSourcePath: 'silver-training-data', downloadPath: 'training-set', uploadPath: 'upload-training-data', imagePath: 'all-dataset-file', templateName: 'Train', datasetType: 'Train'  }"></ImageCaptioning>
</template>

<script src="./TrainingData.js"></script>