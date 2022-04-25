<template>
	<ImageCaptioning v-bind="{ dataSourcePath: 'gold-validation-data', downloadPath: 'validation-set', uploadPath: 'upload-validation-data', imagePath: 'all-dataset-file', templateName: 'DataImageCaptioningValidateData', datasetType: 'Validation'  }"></ImageCaptioning>
</template>

<script src="./ValidateData.js"></script>
