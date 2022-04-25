<template>
	<ImageClassification v-bind="{ dataSourcePath: 'gold-validation-data', downloadPath: 'validation-set', uploadPath: 'upload-validation-data', imagePath: 'all-dataset-file', templateName: 'DataImageClassificationValidateData', datasetType: 'Validation'}"></ImageClassification>
</template>

<script src="./ValidateData.js"></script>
