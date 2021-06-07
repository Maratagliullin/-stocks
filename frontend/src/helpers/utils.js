export const notyfyuser = (data) => {
  var i
  for (i = 0; i < data.length; i++) {
    if (data[i].status == 'found') {
      var text = data[i].message
      var title = data[i].tiker
      var variant = 'success'
      return {text: text, variant: variant, title: title}
    }
    if (data[i].status == 'not_found') {
      text = data[i].message
      title = data[i].tiker
      variant = 'danger'
      return {text: text, variant: variant, title: title}
    }
    if (data[i].status == 'empty_value') {
      text = data[i].message
      title = 'Ошибка'
      variant = 'danger'
      return {text: text, variant: variant, title: title}
    }
    if (data[i].status == 'dublicate') {
      text = data[i].message
      title = data[i].tiker
      variant = 'info'
      return {text: text, variant: variant, title: title}
    }
  }
}
