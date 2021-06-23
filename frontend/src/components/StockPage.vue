// Компонент страницы
<template>
  <div>
    <!-- {{ stockClassRow }} -->
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
        <div class="text-center text-info my-2">
          <b-spinner small class="align-middle"></b-spinner>
          <strong>Загрузка...</strong>
        </div>
      </template>

       <template #cell(tradingview_dentifier)="data">
        <!-- `data.value` is the value after formatted by the Formatter -->
        <a :href="`${data.value}`" target="_blank">{{ data.value }}</a>
      </template>

      <template #cell(investing_dentifier)="data">
        <!-- `data.value` is the value after formatted by the Formatter -->
        <a :href="`${data.value}`" target="_blank">{{ data.value }}</a>
      </template>

      <template #cell(actions)="row">
        <b-button variant="danger" size="sm" @click="showMsgBoxTwo(row.item, row.index, $event.target)">
          Удалить
        </b-button>
      </template>

      <template v-if="getStocks.length" #table-caption>
        <p class="float-right">Итого: {{ getStocksCount }}</p>
      </template>
    </b-table>
    <div style="text-align:center;">{{ data_status }}</div>
  </div>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
export default {
  name: 'StockPage',
  data() {
    return {
      isBusy: true,
      data_status: '',
      striped: false,
      headVariant: '',
      fields: [
        {key: 'id', thClass: 'd-none', tdClass: 'd-none'},
        {key: 'stock_name', label: 'Акция', sortable: true, sortDirection: 'desc'},
        {key: 'stock_ticker', label: 'Тикер', sortable: true, sortDirection: 'desc'},
        {key: 'stock_sector', label: 'Сектор', sortable: true, sortDirection: 'desc'},
        {key: 'stock_industry', label: 'Индустрия', sortable: true, class: 'text-left'},
        {
          key: 'investing_dentifier',
          label: 'Идентификатор investing.com',
          sortable: true,
          class: 'text-left',
          formatter: (value) => {
            if (value === null || value === '') {
              return 'Ожидается получение идентификатора'
            } else {
              return value
            }
          },
        },
        {key: 'tradingview_dentifier', label: 'Идентификатор tradingview.com ', sortable: true, class: 'text-left'},
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
    }
  },
  watch: {
    $route: 'ticker',
    getStocks(data) {
      if (data.length > 0) {
        this.isBusy = false
        this.data_status=''
      } else if (this.getStocks.length == 0) {
        this.isBusy = false
        this.data_status='Данные отсутствуют'
      } else {
        this.isBusy = true
      }
    },
  },
  computed: {
    ...mapGetters({
      getStocks: 'getStocks',
      getStocksCount: 'getStocksCount',
      stockClassRow: 'stockClassRow',
    }),
  },
  async mounted() {
    this.get_stock(),
      (this.interval = setInterval(
        function() {
          this.get_stock()
        }.bind(this),
        15000
      ))
  },
  methods: {
    ...mapActions(['get_stock']),
    rowClass(item, type) {
      // примерение класса для строки при изменении данных в строке
      if (this.stockClassRow.length > 0) {
        for (var item_id in this.stockClassRow) {
          if (item.id == this.stockClassRow[item_id].id) {
            return 'changed'
          }
        }
      }

      if (!item || type !== 'row') return
      if (item.stock_activity === false) return 'table-row-noactive'
    },
    toggleBusy() {
      this.isBusy = !this.isBusy
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
            this.$store.dispatch('delete_stock', {'id': stock_id, operation: 'delete'})
          }
        })
    },
  },
}
</script>
