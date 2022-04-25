//import {SERVER_URL_CONST} from "../main.js";

export const mymixin = {  
  methods: {
      SERVER_URL() {
		    return "http://" + process.env.VUE_APP_SERVER_URL + "/";
      },

      // DONT USE THIS
      validToken : function() {
        return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJycm9zemN6eWsiLCJlbWFpbCI6InJhZG9zbGF3LnJvc3pjenlrQGVlLnB3LmVkdS5wbCIsImp0aSI6IjdjODJlOTM0LTgxNjctNDZiZC1hOTkyLThlMjY0NmEzY2RiOSIsImV4cCI6MTYwNDEzMzE5NCwiaXNzIjoid3V0LmJhbHRpY2xzYy5ldSIsImF1ZCI6Ind1dC5iYWx0aWNsc2MuZXUifQ.u1X329yQ0tSaF8XQG_30SKKVuPtm0gZjupXVKo-4EuI"
      },      
    }
  }
