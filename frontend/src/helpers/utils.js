export const notyfyuser = (data) => {
  var response = []
  var i
  for (i = 0; i < data.length; i++) { 
        if (data[i].status == 'found') {
          var text = data[i].message
          var title = data[i].stock_ticker
          var variant = 'success'
          response.push({text: text, variant: variant, title: title})
        }
        if (data[i].status == 'not_found') {
          text = data[i].message
          title = data[i].stock_ticker
          variant = 'danger'
          response.push({text: text, variant: variant, title: title})
        }
        if (data[i].status == 'empty_value') {
          text = data[i].message
          title = 'Ошибка'
          variant = 'danger'
          response.push({text: text, variant: variant, title: title})
        }
        if (data[i].status == 'dublicate') {
          text = data[i].message
          title = data[i].stock_ticker
          variant = 'info'
          response.push({text: text, variant: variant, title: title})
        }
        if (data[i].status == 'connection_error') {
          text = data[i].message
          title = 'Ошибка'
          variant = 'danger'
          response.push({text: text, variant: variant, title: title})
        }
  }
return response
}

export const getCookie = (name) => {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

export const  comparer = (otherArray) => {
  return function(current) {
    return (
      otherArray.filter(function(other) {
        return (
          other.stock_name == current.stock_name &&
          other.stock_sector == current.stock_sector &&
          other.stock_industry == current.stock_industry &&
          other.stock_activity == current.stock_activity &&
          other.investing_dentifier == current.investing_dentifier &&
          other.tradingview_dentifier == current.tradingview_dentifier &&
          other.stock_ticker == current.stock_ticker
        )
      }).length == 0
    )
  }
}