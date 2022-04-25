import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore';
import utils from '../../utils/utils'

import TopBarLeftSide from './../TopBarLeftSide/TopBarLeftSide.vue';
import TopBarRightSide from './../TopBarRightSide/TopBarRightSide.vue';

export default {
    name: "TopBar",
    mixins: [mymixin, utils],
    components: {
        TopBarLeftSide,
        TopBarRightSide,
    },
}