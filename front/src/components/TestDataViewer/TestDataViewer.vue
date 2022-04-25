<template>
    <div class ="container1">
    
        <div class="row">
            <!-- ProjectID : {{project_id}} -->
            <div class="col-sm-2 offset-sm-9">
                        <!-- {{runs}} -->
                        <div class="form-group form-inline">
                          <label for="sel1" class = "my-1 mr-2" >Select run :  </label>
                          <select class="form-control my-1 mr-2 form-control-sm" id="sel1" v-model="currentRunId"  @change="runChanged()">
                            <option v-for="run in runs" :value="run.id"> {{run.id}}</option>
                        <!--     <option> 1</option>
                            <option> 2</option>
                            <option> 3</option>
                            <option> 4</option> -->
                          </select>
                        </div> 
                    
            </div>

            <div v-if="!isLoading" class="row">

                <div class="col-sm-10">        
                    <div class="row">
                        <div class="col" v-for="p in this.currChunkData1">
                            <img height = "150" width = "150" :src=" SERVER_URL() + 'get_testing_file/' + p + `?project_id=` + project_id "  >
                            <div> <span class = "font-weight-bolder h6" >Gold label : </span>{{currClassName}}</div>
                            <div> 
                                    <span  :class="{'text-danger':currClassName != file_2_label[p] , 'text-success':currClassName == file_2_label[p]}">
                                        <span class = "font-weight-bolder "  >Silver label :</span> 
                                    
                                        {{file_2_label[p] ? file_2_label[p] : "Unknown" }} 
                                    </span>
                            </div>
                            <div class="mb-3"> <span class = "font-weight-bolder" >File name : </span>{{p}}</div>
                        </div>
                    </div>
    				
    					<!-- <nav aria-label="Page navigation example" >
                            <ul class="pagination justify-content-center">
                                <li class="page-item"><a class="page-link" href="#" >Previous</a></li>
                                <li class="page-item"><a class="page-link" href="#">1</a></li>
                                <li class="page-item"><a class="page-link" href="#">2</a></li>
                                <li class="page-item"><a class="page-link" href="#">3</a></li>
                                <li class="page-item"><a class="page-link" href="#">Next</a></li>
                            </ul>
    					</nav> -->

                    <br/>
                    
                    <div class ="row justify-content-center">
                        <button @click="prevPage1" :disabled=" canMoveBackward().isPossible != true" class="btn btn-secondary mr-1"> <- Previous </button>
                        <button @click="nextPage1" :disabled=" canMoveForward().isPossible != true" class="btn btn-secondary">Next -> </button>
                    </div>
    				
                </div>


                <div class="col-sm-2">
                    <div class = "font-weight-bolder h5">Gold labels:</div>

                    <div v-for="cl in Object.keys(this.training_data_labels)" :key="cl">
                        <span :class="{'font-weight-bolder h5':currClassName == cl}">
                            <input type="checkbox" :id="'id' + cl" checked @click = "checkboxClicked( cl, 'id' + cl )">       {{cl}}                        
                                ({{"G: " + training_data_labels[cl].length + " / S: " + ( testing_data_silver_labels[cl] ? testing_data_silver_labels[cl].length : "0") }}) <br/>
                        </span>
                    </div>
                    <br/>
                    <button type="button" class="btn btn-secondary mr-2" @click="selectAllCheckboxes()">Select all</button>
                    <button type="button" class="btn btn-secondary"  @click="clearAllCheckboxes()">Clear all</button>
                    <br/>
                    <br/>

                    <div class = "font-weight-bolder h5">Filter :</div>
                    
                    <div class="form-group ">
                        <!-- <label for="fset1">Show : </label> -->
                        <fieldset id="fset1"  @change="filterModeChanged()"  >
                            <!-- <legend>Binding : </legend> -->
                            <div class="form-check-inline">
                                <label class="form-check-label" >
                                    <input class="form-check-input" type="radio" name="binding" id="binding_provided" value="All" checked v-model="filter_mode" disabled="disabled"> All
                                </label>
                            </div>
                            <br/>
                            <div class="form-check-inline">
                                <label class="form-check-label" >
                                    <input class="form-check-input" type="radio" name="binding" id="binding_weak" value="Matching" v-model="filter_mode" disabled="disabled"> Matching (Gold == Silver)
                                </label>
                            </div>
                            <br/>
                            <div class="form-check-inline">
                                <label class="form-check-label" >
                                    <input class="form-check-input" type="radio" name="binding" id="binding_strong" value="Mismatching" v-model="filter_mode" disabled="disabled"> Mismatching (Gold != Silver)
                                </label>
                            </div>
                            
                        </fieldset>
                    </div>
                    
                </div>

            </div>
        </div>
    </div>
</template>

<script src="./TestDataViewer.js"></script>