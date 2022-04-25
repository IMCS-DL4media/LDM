import Vue from "vue";
import Router from "vue-router";
import Projects from "./components/Projects/Projects.vue";
import Project from "./components/Project/Project.vue";

// classification
import DataImageClassificationAllData from "./components/ProjectTypes/ImageClassification/Data/AllData/AllData.vue";
import DataImageClassificationTrainingData from "./components/ProjectTypes/ImageClassification/Data/TrainingData/TrainingData.vue";
import DataImageClassificationTestData from "./components/ProjectTypes/ImageClassification/Data/TestData/TestData.vue";
import DataImageClassificationValidateData from "./components/ProjectTypes/ImageClassification/Data/ValidateData/ValidateData.vue";

import TrainImageClassificationTrainingData from "./components/ProjectTypes/ImageClassification/Training/TrainingData/TrainingData.vue";
import TrainImageClassificationTestData from "./components/ProjectTypes/ImageClassification/Training/TestData/TestData.vue";
import TrainImageClassificationValidateData from "./components/ProjectTypes/ImageClassification/Training/ValidateData/ValidateData.vue";

import ProductionDataImageClassification from "./components/ProjectTypes/ImageClassification/Production/Main.vue";


// captioning
import DataImageCaptioningAllData from "./components/ProjectTypes/ImageCaptioning/Data/AllData/AllData.vue";
import DataImageCaptioningTrainingData from "./components/ProjectTypes/ImageCaptioning/Data/TrainingData/TrainingData.vue";
import DataImageCaptioningTestData from "./components/ProjectTypes/ImageCaptioning/Data/TestData/TestData.vue";
import DataImageCaptioningValidateData from "./components/ProjectTypes/ImageCaptioning/Data/ValidateData/ValidateData.vue";

import TrainImageCaptioningTrainingData from "./components/ProjectTypes/ImageCaptioning/Training/TrainingData/TrainingData.vue";
import TrainImageCaptioningTestData from "./components/ProjectTypes/ImageCaptioning/Training/TestData/TestData.vue";
import TrainImageCaptioningValidateData from "./components/ProjectTypes/ImageCaptioning/Training/ValidateData/ValidateData.vue";

import ProductionDataImageCaptioning from "./components/ProjectTypes/ImageCaptioning/Production/Main.vue";



// object detection
import DataObjectDetectionAllData from "./components/ProjectTypes/ObjectDetection/Data/AllData/AllData.vue";
import DataObjectDetectionTrainingData from "./components/ProjectTypes/ObjectDetection/Data/TrainingData/TrainingData.vue";
import DataObjectDetectionTestData from "./components/ProjectTypes/ObjectDetection/Data/TestData/TestData.vue";
import DataObjectDetectionValidateData from "./components/ProjectTypes/ObjectDetection/Data/ValidateData/ValidateData.vue";

import TrainObjectDetectionTrainingData from "./components/ProjectTypes/ObjectDetection/Training/TrainingData/TrainingData.vue";
import TrainObjectDetectionTestData from "./components/ProjectTypes/ObjectDetection/Training/TestData/TestData.vue";
import TrainObjectDetectionValidateData from "./components/ProjectTypes/ObjectDetection/Training/ValidateData/ValidateData.vue";

import ProductionDataObjectDetection from "./components/ProjectTypes/ObjectDetection/Production/Main.vue";



// Media2Text
import DataMedia2TextAllData from "./components/ProjectTypes/Media2Text/Data/AllData/AllData.vue";
import DataMedia2TextTrainingData from "./components/ProjectTypes/Media2Text/Data/TrainingData/TrainingData.vue";
import DataMedia2TextTestData from "./components/ProjectTypes/Media2Text/Data/TestData/TestData.vue";
import DataMedia2TextValidateData from "./components/ProjectTypes/Media2Text/Data/ValidateData/ValidateData.vue";

import TrainMedia2TextTrainingData from "./components/ProjectTypes/Media2Text/Training/TrainingData/TrainingData.vue";
import TrainMedia2TextTestData from "./components/ProjectTypes/Media2Text/Training/TestData/TestData.vue";
import TrainMedia2TextValidateData from "./components/ProjectTypes/Media2Text/Training/ValidateData/ValidateData.vue";

import ProductionDataMedia2Text from "./components/ProjectTypes/Media2Text/Production/Main.vue";


import PublicDatasets from "./components/PublicDatasets/PublicDatasets.vue";
import PublicDataset from "./components/PublicDataset/PublicDataset.vue";

import Run from "./components/Run/Run.vue";
import RunFiles from "./components/RunFiles/RunFiles.vue";
import RunFile from "./components/RunFile/RunFile.vue";

import Analysis from "./components/Analysis/Analysis.vue";

import LoggedFile from "./components/LoggedFile/LoggedFile.vue";

import Login from "./components/Login/Login.vue";
import Members from "./components/Members/Members.vue";

import Profile from "./components/Profile/Profile.vue";

import NotLoggedIn from "./components/NotLoggedIn/NotLoggedIn.vue"

import Media2Text from "./components/Media2Text/Media2Text.vue";
import TrainingMedia2Text from "./components/TrainingMedia2Text/TrainingMedia2Text.vue";


// import AudioTranscription from "./components/AudioTranscription/AudioTranscription.vue";

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: "/",
      name: "Login",
      meta: {layout: "no-bars"},
      component: require("@/components/Login/Login.vue").default,
    },

    {
      path: "/register",
      name: "Register",
      meta: {layout: "no-bars"},
      component: require("@/components/RegisterUser/RegisterUser.vue").default,
    },

    {
      path: "/not-logged-in",
      name: "NotLoggedIn",
      meta: {layout: "no-bars"},
      component: require("@/components/NotLoggedIn/NotLoggedIn.vue").default,
    },


    {
      path: "/projects",
      name: "Projects",
      component: Projects,
      meta: {requiresAuth: true, layout: "no-side-bar",},
    },

    {
      path: "/project/:project_id",
      name: "Project",
      component: Project,
      meta: {requiresAuth: true, sideBarItem: "Training",},
    },

    // {
    //   path: "/image-classification-training-data/:project_id/:run_id?",
    //   name: "ImageClassificationTrainingData",
    //   component: ImageClassificationTrainingData,     
    //   meta: {requiresAuth: true},
    // },

    // {
    //   path: "/image-classification-test-data/:project_id/:run_id?",
    //   name: "ImageClassificationTestData",
    //   component: ImageClassificationTestData,
    //   meta: {requiresAuth: true},
    // },

    // {
    //   path: "/image-classification-validate-data/:project_id/:run_id?",
    //   name: "ImageClassificationValidateData",
    //   component: ImageClassificationValidateData,
    //   meta: {requiresAuth: true},
    // },

    {
      path: "/public-datasets",
      name: "PublicDatasets",
      component: PublicDatasets,
      // meta: {requiresAuth: true},
    },


    {
      path: "/public-dataset/:dataset/:type/:page",
      name: "PublicDataset",
      component: PublicDataset,
      // meta: {requiresAuth: true},
    },

    { 
      path: '/run-details/:project_id/:run_id',
      name: "Run",         
      component: Run,       
      meta: {requiresAuth: true, sideBarItem: "Training",},
    },

    { 
      path: '/run-files/:project_id/:run_id',
      name: "RunFiles",         
      component: RunFiles,       
      meta: {requiresAuth: true, sideBarItem: "Training"},
      children: [{path: "",
                  name: "RunFiles",
                  component: RunFiles,
                  meta: {sideBarItem: "Training"},
                 },
                 {path: "*",
                  name: "RunFiles",
                  component: RunFiles,
                  meta: {sideBarItem: "Training"},
                 },
              ],
    },

    { 
      path: '/run-file/:project_id/:run_id',
      name: "RunFile",         
      component: RunFile,       
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    { 
      path: '/logged-file/:project_id/:run_id',
      name: "LoggedFile",         
      component: LoggedFile,       
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/members/:project_id",
      name: "Members",
      component: Members,
      meta: {requiresAuth: true, sideBarItem: "Members"},
    },

    { 
      path: '/analysis/:project_id/:run_id',
      name: "Analysis",         
      component: Analysis,       
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },


    {
      path: "/profile",
      name: "Profile",
      component: Profile,
      meta: {requiresAuth: true},
    },


// project types
    
  // classification

    {
      path: "/image-classification-all-data/:project_id/:page_nr",
      name: "DataImageClassificationAllData",
      component: DataImageClassificationAllData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/image-classification-training-data/:project_id/:page_nr",
      name: "DataImageClassificationTrainingData",
      component: DataImageClassificationTrainingData,     
      meta: {requiresAuth: true, sideBarItem: "Data"
              // progress: {
              //   func: [
              //     {call: 'color', modifier: 'temp', argument: '#ffb000'},
              //     {call: 'fail', modifier: 'temp', argument: '#6e0000'},
              //     {call: 'location', modifier: 'temp', argument: 'top'},
              //     {call: 'transition', modifier: 'temp', argument: {speed: '1.5s', opacity: '0.6s', termination: 400}}
              //   ]
              // }
      },
    },

    {
      path: "/image-classification-test-data/:project_id/:page_nr",
      name: "DataImageClassificationTestData",
      component: DataImageClassificationTestData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/image-classification-validate-data/:project_id/:page_nr",
      name: "DataImageClassificationValidateData",
      component: DataImageClassificationValidateData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/train-image-classification-training-data/:project_id/:run_id/:page_nr",
      name: "TrainImageClassificationTrainingData",
      component: TrainImageClassificationTrainingData,     
      meta: {requiresAuth: true, sideBarItem: "Training"
              // progress: {
              //   func: [
              //     {call: 'color', modifier: 'temp', argument: '#ffb000'},
              //     {call: 'fail', modifier: 'temp', argument: '#6e0000'},
              //     {call: 'location', modifier: 'temp', argument: 'top'},
              //     {call: 'transition', modifier: 'temp', argument: {speed: '1.5s', opacity: '0.6s', termination: 400}}
              //   ]
              // }
      },
    },

    {
      path: "/train-image-classification-test-data/:project_id/:run_id/:page_nr",
      name: "TrainImageClassificationTestData",
      component: TrainImageClassificationTestData,
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/train-image-classification-validate-data/:project_id/:run_id/:page_nr",
      name: "TrainImageClassificationValidateData",
      component: TrainImageClassificationValidateData,
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/production-image-classification-data/:project_id/:page_nr",
      name: "ProductionDataImageClassification",
      component: ProductionDataImageClassification,
      meta: {requiresAuth: true, sideBarItem: "Production"},
    },

  // object detection

    {
      path: "/object-detection-all-data/:project_id/:page_nr",
      name: "DataObjectDetectionAllData",
      component: DataObjectDetectionAllData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/object-detection-training-data/:project_id/:page_nr",
      name: "DataObjectDetectionTrainingData",
      component: DataObjectDetectionTrainingData,     
      meta: {requiresAuth: true, sideBarItem: "Data"
              // progress: {
              //   func: [
              //     {call: 'color', modifier: 'temp', argument: '#ffb000'},
              //     {call: 'fail', modifier: 'temp', argument: '#6e0000'},
              //     {call: 'location', modifier: 'temp', argument: 'top'},
              //     {call: 'transition', modifier: 'temp', argument: {speed: '1.5s', opacity: '0.6s', termination: 400}}
              //   ]
              // }
      },
    },

    {
      path: "/object-detection-test-data/:project_id/:page_nr",
      name: "DataObjectDetectionTestData",
      component: DataObjectDetectionTestData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/object-detection-validate-data/:project_id/:page_nr",
      name: "DataObjectDetectionValidateData",
      component: DataObjectDetectionValidateData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/train-object-detection-training-data/:project_id/:run_id/:page_nr",
      name: "TrainObjectDetectionTrainingData",
      component: TrainObjectDetectionTrainingData,     
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/train-object-detection-test-data/:project_id/:run_id/:page_nr",
      name: "TrainObjectDetectionTestData",
      component: TrainObjectDetectionTestData,
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/train-object-detection-validate-data/:project_id/:run_id/:page_nr",
      name: "TrainObjectDetectionValidateData",
      component: TrainObjectDetectionValidateData,
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/production-object-detection-data/:project_id/:page_nr",
      name: "ProductionDataObjectDetection",
      component: ProductionDataObjectDetection,
      meta: {requiresAuth: true, sideBarItem: "Production"},
    },


  // captioning
    {
      path: "/image-captioning-all-data/:project_id/:page_nr",
      name: "DataImageCaptioningAllData",
      component: DataImageCaptioningAllData,     
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/image-captioning-training-data/:project_id/:page_nr",
      name: "DataImageCaptioningTrainingData",
      component: DataImageCaptioningTrainingData,     
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/image-captioning-test-data/:project_id/:page_nr",
      name: "DataImageCaptioningTestData",
      component: DataImageCaptioningTestData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/image-captioning-validate-data/:project_id/:page_nr",
      name: "DataImageCaptioningValidateData",
      component: DataImageCaptioningValidateData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },


    {
      path: "/train-image-captioning-training-data/:project_id/:run_id/:page_nr",
      name: "TrainImageCaptioningTrainingData",
      component: TrainImageCaptioningTrainingData,     
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/train-image-captioning-test-data/:project_id/:run_id/:page_nr",
      name: "TrainImageCaptioningTestData",
      component: TrainImageCaptioningTestData,
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/train-image-captioning-validate-data/:project_id/:run_id/:page_nr",
      name: "TrainImageCaptioningValidateData",
      component: TrainImageCaptioningValidateData,
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/production-image-captioning-data/:project_id/:page_nr",
      name: "ProductionDataImageCaptioning",
      component: ProductionDataImageCaptioning,
      meta: {requiresAuth: true, sideBarItem: "Production"},
    },


  // media2text
    {
      path: "/media2text-all-data/:project_id/:page_nr",
      name: "DataMedia2TextAllData",
      component: DataMedia2TextAllData,     
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/media2text-training-data/:project_id/:page_nr",
      name: "DataMedia2TextTrainingData",
      component: DataMedia2TextTrainingData,     
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/media2text-test-data/:project_id/:page_nr",
      name: "DataMedia2TextTestData",
      component: DataMedia2TextTestData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/media2text-validate-data/:project_id/:page_nr",
      name: "DataMedia2TextValidateData",
      component: DataMedia2TextValidateData,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },

    {
      path: "/train-media2text-training-data/:project_id/:run_id/:page_nr",
      name: "TrainMedia2TextTrainingData",
      component: TrainMedia2TextTrainingData,     
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/train-media2text-test-data/:project_id/:run_id/:page_nr",
      name: "TrainMedia2TextTestData",
      component: TrainMedia2TextTestData,
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/train-media2text-validate-data/:project_id/:run_id/:page_nr",
      name: "TrainMedia2TextValidateData",
      component: TrainMedia2TextValidateData,
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

    {
      path: "/production-media2text-data/:project_id/:page_nr",
      name: "ProductionDataMedia2Text",
      component: ProductionDataMedia2Text,
      meta: {requiresAuth: true, sideBarItem: "Production"},
    },


// dataset components
    {
      path: "/media2text-gold/:projectId/:id/:filePath",
      name: "Media2Text",
      component: Media2Text,
      meta: {requiresAuth: true, sideBarItem: "Data"},
    },


    {
      path: "/media2text-silver/:projectId/:runId/:id/:filePath",
      name: "TrainingMedia2Text",
      component: TrainingMedia2Text,
      meta: {requiresAuth: true, sideBarItem: "Training"},
    },

  ]
});
