<template>
  <div>
    <b-table
      striped
      bordered
      :tbody-tr-class="rowClass"
      :head-variant="headVariant"
      :busy="isBusy"
      :items="stock_state"
      :fields="fields"
      stacked="md"
      show-empty
      small
    >
      <template #table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner small class="align-middle"></b-spinner>
          <strong>Загрузка...</strong>
        </div>
      </template>
      <template #cell(name)="row">{{ row.value.first }} {{ row.value.last }}</template>

      <template #cell(actions)="row">
        <b-button size="sm" @click="info(row.item, row.index, $event.target)">
          Удалить
        </b-button>
      </template>
      <template #table-caption>
        <b class="float-right">Итого: {{stock_state.length}}</b>
      </template>
    </b-table>
    <!-- Info modal -->
    <b-modal :id="infoModal.id" :title="infoModal.title" ok-only @hide="resetInfoModal">
      <pre>{{ infoModal.content }} </pre>
    </b-modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      
      isBusy: false,
      striped: false,
      headVariant: 'light',
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
        id: 'info-modal',
        title: '',
        content: '',
      },
    }
  },
  created() {
  },
  watch: {
    $route: 'ticker',
  },
  computed: {
     stock_state() {
      return this.$store.state.stock
    },
  },
  mounted() {},
  methods: {
    rowClass(item, type) {
      if (!item || type !== 'row') return
      if (item.stock_activity === false) return 'table-row-noactive'
    },
    info(item, index, button) {
      this.infoModal.title = `Row index: ${index}`
      this.infoModal.content = JSON.stringify(item, null, 2)
      this.$root.$emit('bv::show::modal', this.infoModal.id, button)
    },
    resetInfoModal() {
      this.infoModal.title = ''
      this.infoModal.content = ''
    },
  },
}
</script>
