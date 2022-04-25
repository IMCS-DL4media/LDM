import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

import { PrismEditor } from 'vue-prism-editor';
import 'vue-prism-editor/dist/prismeditor.min.css';

import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css';

export default{	 
    mixins: [mymixin, utils],
    components: {
      PrismEditor,
    },
    
    data: function() {
     return {
            projectId: "",
            runId: "",
            fileName: "",    
            error: null,
            code: "",
            filePath: "",
        }
    },

    methods: {
        highlighter(code) {
            return highlight(code, languages.js);
        },
    },

    mounted: function() {
        var self = this;

        self.projectId = self.$route.params['project_id'];
        self.runId = self.$route.params['run_id'];

        let query = this.$route.query;
        if (!query.path) {
            console.error("No path to file", query);
            return;
        }
        self.filePath = query.path;

        axios.get(self.SERVER_URL() + 'logged-file-body/' + self.projectId + "/" + self.runId + "?path=" + self.filePath)
                .then(function(response) {
                    console.log("response", response)
                    if (response.status != 200) {
                        throw Error(response.statusText);
                    }
                        
                    self.code = response.data.file_content;
                })
                .catch(error => {
                    self.processErrorInPromise(error)
                });
    },
	
};