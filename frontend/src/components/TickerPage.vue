<template>
  <div>
    <h5 v-if="getTicker">{{ getTicker.stock_name }}</h5>
    <h5 v-else>Данные отсутсвуют</h5>

    <div>
      <b>Сектор: </b>
      <span v-if="getTicker">{{ getTicker.stock_sector }}</span>
      <span v-else>Данные отсутсвуют</span>
    </div>
    <div>
      <b>Индустрия: </b>
      <span v-if="getTicker">{{ getTicker.stock_industry }}</span>
      <span v-else>Данные отсутсвуют</span>
    </div>
    <div>
      <b>Идентификатор investing.com: </b>
      <span v-if="getTicker">{{ getTicker.investing_dentifier }}</span>
      <span v-else>Данные отсутсвуют</span>
    </div>
    <div>
      <b>Идентификатор tradingview.com: </b>
      <span v-if="getTicker">{{ getTicker.tradingview_dentifier }}</span>
      <span v-else>Данные отсутсвуют</span>
    </div>
    <div>
      <b>Тикер: </b>
      <span v-if="getTicker">{{ getTicker.stock_ticker }}</span>
      <span v-else>Данные отсутсвуют</span>
    </div>
    <div class="mt-3">
      <b-form-group label="Данные tradingview.com:" label-for="textarea-formatter">
        <b-form-textarea
          v-model="getTickerDataJsonTradingview"
          rows="5"
          cols="3"
          name="stock"
          type="text"
          class="form-control"
          id="stock"
          placeholder=""
        ></b-form-textarea>
      </b-form-group>
      <p style="white-space: pre-line">
        <b>Дата: </b>
        {{ getTickerDataDateTradingview }}
      </p>
    </div>
    <div class="mt-3">
      <b-form-group label="Данные investing.com:" label-for="textarea-formatter">
        <b-form-textarea
          v-model="getTickerDataJsonInvesting"
          rows="4"
          cols="3"
          name="stock"
          type="text"
          class="form-control"
          id="stock"
          placeholder=""
        ></b-form-textarea>
      </b-form-group>
      <p style="white-space: pre-line">
        <b>Дата: </b>
        {{ getTickerDataDateInvesting }}
      </p>
    </div>
  </div>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
export default {
  data: function() {
    return {
      getTickerDataDateInvesting: 'Данные отсутсвуют',
      getTickerDataJsonInvesting: 'Данные отсутсвуют',
      getTickerDataDateTradingview: 'Данные отсутсвуют',
      getTickerDataJsonTradingview: 'Данные отсутсвуют',
    }
  },
  name: 'TickerPage',

  computed: {
    ...mapGetters({
      getTickerNameByState: 'getTickerNameByState',
    }),

    getTicker() {
      var id = this.$route.params.id
      return this.$store.getters.getTickerByIdState(Number(id))
    },
    getTickeByServer() {
      var id = this.$route.params.id
      return this.getTickerNameByState(Number(id))
    },
  },
  methods: {
    ...mapActions(['getTickerByIdServer', 'getTickerDataByServer']),
  },
  created() {
    console.log('created')
    var id = this.$route.params.id
    this.getTickerByIdServer(Number(id)).then(() => {
      this.getTickerDataByServer(this.getTickeByServer).then(() => {
        this.getTickerDataDateInvesting = this.$store.getters.getTickerDataDateInvesting
        this.getTickerDataJsonInvesting = this.$store.getters.getTickerDataJsonInvesting
        this.getTickerDataDateTradingview = this.$store.getters.getTickerDataDateTradingview
        this.getTickerDataJsonTradingview = this.$store.getters.getTickerDataJsonTradingview
      })
    })
  },
}
</script>
