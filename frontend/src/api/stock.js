import {HTTP} from './common'
import Vue from 'vue'

export const Stock = {
  create(config) {
    return HTTP.post('/add_stock/', config)
      .then((response) => {
        notyfyuser(response.data)
        for (var item in response.data) {
          if (response.data[item].status != 'dublicate') {
            return this.get_stock()
          }
        }
      })
      .catch((error) => {
        notyfyuser(error.response.data)
        //return error.response.data
      })
  },
  delete(note) {
    return HTTP.delete(`/delete_stock/${note.id}/`)
  },
  get_stock() {
    return HTTP.get('/get_stock/').then((response) => {
        return response.data
    })
  },
}

export function show_toast(text, variant, title) {
  const mv = new Vue()
  mv.$bvToast.toast(text, {
    title: title,
    autoHideDelay: 15000,
    variant: variant,
    appendToast: true,
    noCloseButton: false,
  })
}

export function notyfyuser(data) {
  var i
  for (i = 0; i < data.length; i++) {
    if (data[i].status == 'found') {
      var text = data[i].message
      var title = data[i].tiker
      var variant = 'success'
      show_toast(text, variant, title)
    }
    if (data[i].status == 'not_found') {
      text = data[i].message
      title = data[i].tiker
      variant = 'danger'
      show_toast(text, variant, title)
    }
    if (data[i].status == 'empty_value') {
      text = data[i].message
      title = 'Ошибка'
      variant = 'danger'
      show_toast(text, variant, title)
    }
    if (data[i].status == 'dublicate') {
      text = data[i].message
      title = data[i].tiker
      variant = 'info'
      show_toast(text, variant, title)
    }
  }
}
