<template>
	<ImageCaptioning v-bind="{ dataSourcePath: 'gold-training-data', downloadPath: 'training-set', uploadPath: 'upload-training-data', imagePath: 'all-dataset-file', templateName: 'DataImageCaptioningTrainingData', datasetType: 'Train'  }"></ImageCaptioning>
</template>

<script src="./TrainingData.js"></script>