// Компонент формы
<template>
  <div class="stock_block">
    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label class="col-form-label" for="stock">Идентификатор акции</label>
        <textarea
          rows="3"
          v-model="stock"
          name="stock"
          type="text"
          class="form-control"
          id="stock"
          aria-describedby="phoneHelp"
          placeholder=""
        ></textarea>
        <small id="stockHelp" class="form-text text-muted">
          Допускается ввод как одного, так и нескольких значений, каждое из которых начинается с новой строки
        </small>
      </div>
      <button class="btn btn-primary">
        Добавить
      </button>
      <transition name="fade">
        <b-spinner
          v-show="loading"
          variant="info"
          style="width: 1.5rem; height: 1.5rem; margin-top: 5px;"
          class="float-right"
          label="Floated Right"
        ></b-spinner>
      </transition>
    </form>
  </div>
</template>

<script>
export default {
  name: 'StockForm',
  data() {
    return {
      stock: null,
      loading: false,
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$store.dispatch('add_stock', {stock: this.stock}).then((response) => {
        this.notyfyuser(response)

        // Поиск в ответе хоть одной найденной акции
        var status_found = response.findIndex(function(status) {
          if (status.status == 'found') return true
        })

        // Если акция есть то обновляем стор
        if (status_found !== -1) {
          this.$store.dispatch('get_stock')
        }
        this.loading = false
      })
    },
    // Оповещения
    notyfyuser(data) {
      var i
      for (i = 0; i < data.length; i++) {
        if (data[i].status == 'found') {
          var text = data[i].message
          var title = data[i].tiker
          var variant = 'success'
          this.show_toast(text, variant, title)
        }
        if (data[i].status == 'not_found') {
          text = data[i].message
          title = data[i].tiker
          variant = 'danger'
          this.show_toast(text, variant, title)
        }
        if (data[i].status == 'empty_value') {
          text = data[i].message
          title = 'Ошибка'
          variant = 'danger'
          this.show_toast(text, variant, title)
        }
        if (data[i].status == 'dublicate') {
          text = data[i].message
          title = data[i].tiker
          variant = 'info'
          this.show_toast(text, variant, title)
        }
      }
    },
    // Тост
    show_toast(text, variant, title) {
      this.$root.$bvToast.toast(text, {
        title: title,
        autoHideDelay: 15000,
        variant: variant,
        appendToast: true,
        noCloseButton: false,
      })
    },
  },
}
</script>
