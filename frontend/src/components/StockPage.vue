<template>
  <div>
    <b-table
      bordered
      :tbody-tr-class="rowClass"
      :head-variant="headVariant"
      :busy="isBusy"
      :items="getStocks"
      :fields="fields"
      stacked="md"
    >
      <template #table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner small class="align-middle"></b-spinner>
          <strong>Загрузка...</strong>
        </div>
      </template>
      <template #cell(name)="row">{{ row.value.first }} {{ row.value.last }}</template>

      <template #cell(actions)="row">
        <b-button variant="danger" size="sm" @click="showMsgBoxTwo(row.item, row.index, $event.target)">
          Удалить
        </b-button>
      </template>
      <template #table-caption>
        <b class="float-right">Итого: {{ getStocksCount }}</b>
      </template>
    </b-table>
  </div>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
export default {
  data() {
    return {
      isBusy: false,
      striped: false,
      headVariant: '',
      fields: [
        {key: 'stock_name', label: 'Акция', sortable: true, sortDirection: 'desc'},
        {key: 'stock_sector', label: 'Сектор', sortable: true, sortDirection: 'desc'},
        {key: 'stock_industry', label: 'Индустрия', sortable: true, class: 'text-left'},
        {key: 'stock_identifier', label: 'Идентификатор', sortable: true, class: 'text-left'},
        {
          key: 'stock_activity',
          label: 'Активность',
          sortable: true,
          sortByFormatted: true,
          filterByFormatted: true,
          formatter: (value) => {
            if (value == true) {
              return 'Активна'
            } else {
              return 'Не активна'
            }
          },
        },
        {key: 'actions', label: 'Удалить'},
      ],
      infoModal: {
        id: 'modal-1',
        title: '',
        content: '',
        stock_name: '',
      },
    }
  },
  watch: {
    $route: 'ticker',
  },
  computed: {
    ...mapGetters(['getStocks', 'getStocksCount']),
  },
  async mounted() {
    this.get_stock()
  },
  methods: {
    ...mapActions(['get_stock']),
    rowClass(item, type) {
      if (!item || type !== 'row') return
      if (item.stock_activity === false) return 'table-row-noactive'
    },
    showMsgBoxTwo(item) {
      var stock_name = item.stock_name
      var stock_id = item.id
      this.$bvModal
        .msgBoxConfirm('Подтвердите, если хотите удалить акцию ' + stock_name, {
          title: 'Удаление?',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'danger',
          okTitle: 'Да',
          cancelTitle: 'Нет',
          footerClass: 'p-2',
          hideHeaderClose: false,
          centered: false,
        })
        .then((value) => {
          if (value == true) {
            this.$store.dispatch('delete_stock', stock_id)
          }
        })
    },
  },
}
</script>
