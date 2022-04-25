<template>
	<div>
		<div class="row">
			<div v-if="file.isNotebook" class=" col-lg-8">
        <p>{{filePath}}</p>
        <div v-html="file.code" style="color:black;"></div>
      </div>
		
      <div v-else  class="col-lg-8">
        <p>{{filePath}}</p>
        <prism-editor class="my-editor" v-model="file.code" :highlight="highlighter" line-numbers readonly></prism-editor>
      </div>

    </div>
	</div>

</template>

<script src="./RunFile.js"></script>


<style>
  /* required class */
  .my-editor {
    /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
    background: white;
    color: #ccc;
 
    /* you must provide font-family font-size line-height. Example: */
    font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
    font-size: 14px;
    line-height: 1.5;
    padding: 5px;
  }
 
  /* optional class for removing the outline */
  .prism-editor__textarea:focus {
    outline: none;
  }

</style> 