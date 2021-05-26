function getCookie(name) {
     let cookieValue = null;
     if (document.cookie && document.cookie !== '') {
         const cookies = document.cookie.split(';');
         for (let i = 0; i < cookies.length; i++) {
             const cookie = cookies[i].trim();
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) === (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }


var app = new Vue({
    el: '#app',
    data: {
      errors: [],
      stock: null,
      info: [],
    },
    methods: {
      submit: function (event) {
        if (this.stock) {
            Vue.axios.post('/api/v1/stock/', {
                stock: this.stock,
               }, 
              {headers: {
                 'X-CSRFToken':  getCookie('csrftoken'),
              }})
               .then(response => {
                   console.log(response);
               })
               .catch(error => {
               });
        }
        this.errors = [];

        if (!this.stock) {
            this.errors.push('Требуется указать значение идентификатора');
        }         
         event.preventDefault();
        }
    }
  })
  