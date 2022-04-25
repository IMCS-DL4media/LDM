<template>
	<div id="app">
		<vue-progress-bar></vue-progress-bar>
		<component :is="layout">
			<router-view/>
		</component>
	</div>
</template>

<script src="./App.js"></script>