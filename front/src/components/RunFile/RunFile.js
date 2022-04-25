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

import '../../../public/notebook.js'

// import 'https://cdn.jsdelivr.net/npm/ipynb2html@0.3.0/dist/ipynb2html-full.min.js'

// import * as ipynb from 'ipynb2html'
// import { Document } from 'nodom'


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
            file: {code: "", isNotebook: false},
            filePath: "",
        }
    },

    methods: {
        highlighter(code) {
            return highlight(code, languages.js);
        },


        notebookHighlighter(code, lang) {
            if (typeof lang === 'undefined') lang = 'markup';

            if (!Prism.languages.hasOwnProperty(lang)) {
                try {
                    require('prismjs/components/prism-' + lang + '.js');
                } catch (e) {
                    console.warn('** failed to load Prism lang: ' + lang);
                    Prism.languages[lang] = false;
                }
            }

            return Prism.languages[lang] ? Prism.highlight(code, Prism.languages[lang]) : code;
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

        axios.get(self.SERVER_URL() + 'file-body/' + self.projectId + "/" + self.runId + "?path=" + self.filePath)
                .then(function(response) {
                    console.log("response", response)
                    if (response.status != 200) {
                        throw Error(response.statusText);
                    }
                        
                    if (_.last(self.filePath.split(".")) == "ipynb") {
                        nb.highlighter = function(text, pre, code, lang) {
                                            $(pre).css("background", "white");

                                            var language = lang || 'text';
                                            pre.className = 'language-' + language;
                                            if (typeof code != 'undefined') {
                                                code.className = 'language-' + language;
                                            }

                                            return self.highlighter(text, language);
                                        };

                        var ipynb = JSON.parse(response.data.file_content);
                        var notebook = nb.parse(ipynb);

                        _.extend(self.file, {isNotebook: true, code: notebook.render().outerHTML,});                        
                    }        

                    else {
                        self.file.code = response.data.file_content;
                    }

                })
                .catch(error => {
                    self.processErrorInPromise(error)
                });
    },
	
};