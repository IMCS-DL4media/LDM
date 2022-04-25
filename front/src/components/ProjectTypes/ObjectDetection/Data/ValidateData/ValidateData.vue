<template>
	<ObjectDetection v-bind="{ dataSourcePath: 'gold-validation-data', downloadPath: 'validation-set', uploadPath: 'upload-validation-data', imagePath: 'all-dataset-file', templateName: 'DataObjectDetectionValidateData', datasetType: 'Validation'}"></ObjectDetection>
</template>

<script src="./ValidateData.js"></script>
