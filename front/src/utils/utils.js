import { _ } from 'vue-underscore';
import { EventBus } from '../components/event-bus.js';


export default {
  data: function() {

    let dataComponents = {
        ImageClassification: "DataImageClassificationAllData",
        ImageCaptioning: "DataImageCaptioningAllData",
        Media2Text: "DataMedia2TextAllData",
        ObjectDetection: "DataObjectDetectionAllData"
      };

    let trainComponents = {

        ImageClassification: {
                train: "TrainImageClassificationTrainingData",
                validation: "TrainImageClassificationValidateData",
                test: "TrainImageClassificationTestData",
        },

        ImageCaptioning: {
                train: "TrainImageCaptioningTrainingData",
                validation: "TrainImageCaptioningValidateData",
                test: "TrainImageCaptioningTestData",
        },

        Media2Text: {
                train: "TrainMedia2TextTrainingData",
                validation: "TrainMedia2TextValidateData",
                test: "TrainMedia2TextTestData",
        },
      
        ObjectDetection: {
                train: "TrainObjectDetectionTrainingData",
                validation: "TrainObjectDetectionValidateData",
                test: "TrainObjectDetectionTestData",
        },
      };


    let productionComponents = {
        ImageClassification: "ProductionDataImageClassification",
        ImageCaptioning: "ProductionDataImageCaptioning",
        Media2Text: "ProductionDataMedia2Text",
        ObjectDetection: "ProductionDataObjectDetection",
      };

    return {modalNotification: null,
            dataComponents: dataComponents,
            productionComponents: productionComponents,
            trainComponents: trainComponents,
          }
  },
  
  methods: {
    processResponse(response) {
    	// console.log("response", response);
    	return response.data; 
    	// return response.data.response;
    },

    getToken() {    
      return localStorage.getItem("token");
    },

    getId(obj) {
      if (obj._id && obj._id["$oid"]) {
        return obj._id["$oid"];
      }
      else {
        return obj._id;
      }
    },

    covnertTimeFromDateObject(date_obj) {
      return this.covnertTime(date_obj.$date);
    },

    covnertTime(time) {
      return this.$moment(time).format("YYYY-MM-DD HH:mm:ss");
    },

    getUsername() {    
      return localStorage.getItem("user");
    },

    getHeader() {
    	let token = this.getToken();
  		return {headers: {
      					Authorization: "Bearer " + token,
                "content-type": "application/json"
  					},
  				};
    },
	
  	TimeString(str) {
  		let timestr = this.$moment(str).format("YYYY-MM-DD HH:mm:ss");
  		return timestr == "0001-01-01 00:00:00" ? "" : timestr;
  	},

    addNotification(msg, type_in) {
      EventBus.$emit("add-notification", {msg: msg, type: type_in});
    },

    removeNotification(id) {
      EventBus.$emit("remove-notification", id);
    },

    removeAllNotifications() {
      EventBus.$emit("remove-all-notifications");
    },

    noErrorsInResponse(response, modal = false) {
      if (response.status == 200 && response.data.success != false) {
        return true;
      } else {
        let msg = response.status == 200 ? "Error in the "+response.config.url+" response! Status: OK, but \""+response.data.message+"\""
                                         : "Error in the "+response.config.url+" response! Status:"+response.status+", \""+response.statusText+"\"";
        modal ? this.showModalMessage(msg, "error")
              : this.addNotification(msg,"error"); 
        return false;
      }
    },

    processErrorInPromise(error, modal = false) {
      let msg = ""; 

      if (error.response && error.response.status == 401) {
        console.error("Error not logged in", error.response);
        this.$router.push({name: 'NotLoggedIn'});
      }

      if (error.response) {
         msg = "Error in the endpoint " + error.response.config.url + 
               ". Status:" + error.response.status + " \"" + error.response.statusText + "\". Data: \"" + error.response.data+"\"";
      }
      else {
         msg = error;
      }
      
      modal ? this.showModalMessage(msg, "error") : this.addNotification(msg, "error");
      console.log("Error ", error);
    },

    showModalMessage: function(msg, type_in) {
      const types = {
        info: "info",
        error: "danger",
        warning: "warning",
      };
      let type = types[type_in] || "info";
      this.modalNotification = {msg: msg, type: "alert-"+type };
    },

    clearModalMessage: function() {
      this.modalNotification = null;
    },

    checkPaginationButtons: function() {
      let self = this;

      if (this.currentPage > 1) {
          this.isPrevEnabled = "";
      }
      else {
          this.isPrevEnabled = "disabled";
      }

      this.totalPages = Math.ceil(this.total / this.step);
      if (this.currentPage < this.totalPages) {
          this.isNextEnabled = "";
      }
      else {
          this.isNextEnabled = "disabled";
      }

      let start_button_index = 1;
      const TOTAL_BUTTONS = 11;
      let end_button_index = Math.min(TOTAL_BUTTONS, this.totalPages + 1);

      let middle_button_index = Math.ceil((end_button_index - start_button_index) / 2);
      if (this.currentPage > middle_button_index) {
          start_button_index = this.currentPage - middle_button_index;
          end_button_index = Math.min(this.currentPage + middle_button_index, this.totalPages + 1);
      }

      let button_indexes = _.range(start_button_index, end_button_index);

      this.paginationButtons = _.map(button_indexes, function(index_in) {
                                  let button = {active: "", index: index_in,};

                                  if (index_in == self.currentPage) {
                                      _.extend(button, {active: "active",});
                                  }

                                  return button;
                              });
    },

  }
}
