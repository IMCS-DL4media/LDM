<template>
	<ObjectDetection v-bind="{ dataSourcePath: 'silver-validation-data', downloadPath: 'validation-set', uploadPath: 'upload-validation-data', imagePath: 'validation-dataset-file', templateName: 'Validate', datasetType: 'Validation'}"></ObjectDetection>
</template>

<script src="./ValidateData.js"></script>
