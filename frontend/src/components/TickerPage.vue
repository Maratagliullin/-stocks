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
    <div  v-if="getTickerData">
    <div>
      <b>Данные tradingview.com:</b>
      <br />
     <b v-if="getTickerData.tradingview">Дата: {{getTickerData.tradingview.tradingview_data_date }}</b>
      <textarea v-if="getTickerData.tradingview"
        v-model="getTickerDataJsonTradingviewGetter"
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
      <b v-if="getTickerData.investing">Дата: {{getTickerData.investing.investing_data_date }}</b>
      <textarea
        v-model="getTickerDataJsonInvestingGetter"
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
      getTickerDataJsonInvestingGetter:'getTickerDataJsonInvesting',
      getTickerDataJsonTradingviewGetter:'getTickerDataJsonTradingview'
    }),

    getTicker() {
      var id = this.$route.params.id
      if (this.getStocks.length != 0) {
      return this.getTickerByIdState(Number(id))
      } else {
        return  this.getTickerByIdServer(Number(id))
      }
    },

    getTickeByServer: {
      get: function() {
        var id = this.$route.params.id
        return this.getTickerNameByState(Number(id))
      },
    },
    
  },
  methods: {
    ...mapActions(['getTickerByIdServer', 'getTickerDataByServer']),
  },

  created() {
    var id = this.$route.params.id
    this.getTickerByIdServer(Number(id)).then(() => {
      this.getTickerDataByServer(this.getTickeByServer)
    })
  },
}
</script>
