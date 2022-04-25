<template>
	<ImageCaptioning v-bind="{ dataSourcePath: 'silver-validation-data', downloadPath: 'validation-set', uploadPath: 'upload-validation-data', imagePath: 'all-dataset-file', templateName: 'Validate', datasetType: 'Validation'  }"></ImageCaptioning>
</template>

<script src="./ValidateData.js"></script>
