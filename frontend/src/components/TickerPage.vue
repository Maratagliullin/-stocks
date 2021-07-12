<template>
  <div>
    <!-- <div id="nav"><router-link to="/ticker">Вернуться к списку акций</router-link></div> -->
    <h5>{{ getTicker.stock_name }}</h5>
    <div>
      <b>Сектор:</b>
      {{ getTicker.stock_sector }}
    </div>
    <div>
      <b>Индустрия:</b>
      {{ getTicker.stock_industry }}
    </div>
    <div>
      <b>Идентификатор investing.com:</b>
      {{ getTicker.investing_dentifier }}
    </div>
    <div>
      <b>Идентификатор tradingview.com:</b>
      {{ getTicker.tradingview_dentifier }}
    </div>
    <div>
      <b>Тикер:</b>
      {{ getTicker.stock_ticker }}
    </div>
    <div>
      <b>Данные tradingview.com:</b>
      <br>
      <b>Дата:{{tradingview_date }}</b>
      <textarea
        v-model="tradingview_json"
        rows="5"
        cols="3"
        name="stock"
        type="text"
        class="form-control"
        id="stock"
        placeholder=""
      ></textarea>
    </div>
    <div>
      <b>Данные investing.com:</b>
      <br>
      <b>Дата:{{ investing_date }}</b>
      <textarea
        v-model="investing_json"
        rows="4"
        cols="3"
        name="stock"
        type="text"
        class="form-control"
        id="stock"
        placeholder=""
      ></textarea>
    </div>
  </div>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
export default {
  filters: {
    pretty: function(value) {
      return JSON.stringify(JSON.parse(value), null, 2)
    },
  },
  name: 'TickerPage',

  computed: {
    ...mapGetters({
      getStocks: 'getStocks',
      getTickerByIdState: 'getTickerByIdState',
      getTickerNameByState: 'getTickerNameByState',
      getTickerData: 'getTickerData',
    }),

    getTicker() {
      var id = this.$route.params.id
      if (this.getStocks.length != 0) {
        return this.getTickerByIdState(Number(id))
      } else {
        return this.getTickerByIdServer(Number(id))
      }
    },

    getTickeByServer: {
      get: function() {
        var id = this.$route.params.id
        return this.getTickerNameByState(Number(id))
      },
    },
    investing_json: {
      get: function() {
        return  JSON.stringify(this.getTickerData.investing.investing_data_json_value)
      },
    },
     tradingview_json: {
      get: function() {
        return  JSON.stringify(this.getTickerData.tradingview.tradingview_data_json_value)
      },
    },
    tradingview_date: {
      get: function() {
        return this.getTickerData.tradingview.tradingview_data_date
      },
    },
    investing_date: {
      get: function() {
        return  this.getTickerData.investing.investing_data_date
      },
    },
  },
  methods: {
    ...mapActions(['getTickerByIdServer', 'getTickerDataByServer']),
  },
  created() {
    this.getTickerDataByServer(this.getTickeByServer)
  },
}
</script>
