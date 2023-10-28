<template>
  <div class="col-sm-6 col-md-4">
    <div class="panel panel-default">
      <apexchart width="500" type="area" :options="options" :series="series" ref="chart"></apexchart>
      <!-- <canvas ref="lineChart" :width="100" :height="100" :datasets="[{ label: '2018', data: [100, 200] }]"></canvas> -->
      <div class="panel-heading">
        <h3 class="panel-title">
          <strong>
            {{ stock.name }}
          </strong>
          <div class="pull-right">
            Price: {{ stock.price }} &nbsp;&nbsp; |
            Quantity: {{ heldStocks[stock.name] || 0 }} |
            Short Quantity: {{ heldStocks["short_quantity"][stock.name] || 0 }}
          </div>
        </h3>
      </div>
      <div class="panel-body">
        <div class="pull-left">
          <input type="number" class="form-control" placeholder="Quantity" v-model.number="quantity"
            :class="{ danger: insufficientFundsBuy || insufficientQuantitySell }" />
        </div>
        <div class="pull-right">
          <button class="btn btn-success" @click="buyStock"
            :disabled="stock.price <= 0 || quantity <= 0 || !Number.isInteger(quantity)">Buy</button>
          <button class="btn btn-danger" @click="sellStock"
            :disabled="stock.price <= 0 || quantity <= 0 || !Number.isInteger(quantity)">
            Sell
          </button>
          <button class="btn btn-success" @click="shortBuyStock"
            :disabled="stock.price <= 0 || quantity <= 0 || !Number.isInteger(quantity)">Short Buy</button>
          <button class="btn btn-danger" @click="shortSellStock"
            :disabled="stock.price <= 0 || quantity <= 0 || !Number.isInteger(quantity)">
            Short Sell
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import Chart from 'chart.js';
export default {
  props: ["stock"],
  data() {
    return {
      quantity: "",
      stockPrices: this.$store.state.stockPrices,
      options: {
        chart: {
          id: 'stock-chart'
        },
        xaxis: {
          // categories: this.$store.state.stockPrices[this.stock.name]
          labels: {
            show: false,
          }
        },
        markers: {
          size: 0,
        },
        dataLabels: {
          enabled: false,
        },
        colors: ["#000000"]
      },
      series: [{
        name: this.stock.name.toString(),
        data: this.$store.state.stockPrices[this.stock.name]
      }]
    };
  },
  computed: {
    funds() {
      return this.$store.state.funds;
    },
    insufficientFundsBuy() {
      return this.quantity * this.stock.price > this.funds;
    },
    insufficientQuantitySell() {
      return this.quantity > this.$store.state.heldStocks[this.stock.name]
    },
    heldStocks() {
      return this.$store.state.heldStocks;
    },
    getStockPrices() {
      return this.$store.state.stockPrices;
    }
  },
  watch: {
    getStockPrices: function (newValue) {
      newValue;
      this.updateStockPrices();
    }
  },
  methods: {
    buyStock() {
      console.log("BUY");
      const order = {
        stockId: this.stock.id,
        name: this.stock.name,
        quantity: this.quantity,
      };
      this.$store.dispatch("buyStocks", order);
      this.quantity = 0;
    },
    sellStock() {
      console.log("SELL");
      const order = {
        stockId: this.stock.id,
        stockName: this.stock.name,
        quantity: this.quantity,
        operation: "sell",
      };
      this.$store.dispatch("sellStocks", order);
      this.quantity = 0;
    },
    shortBuyStock() {
      console.log("Short Buy");
      const order = {
        stockId: this.stock.id,
        name: this.stock.name,
        quantity: this.quantity,
        operation: "short_buy",
      };
      this.$store.dispatch("shortBuyStocks", order);
      this.quantity = 0;
    },
    shortSellStock() {
      console.log("Short Sell");
      const order = {
        stockId: this.stock.id,
        name: this.stock.name,
        quantity: this.quantity,
        operation: "short_buy",
      };
      this.$store.dispatch("shortSellStocks", order);
      this.quantity = 0;
    }
  },
  mounted() {
    var me = this;
    window.setInterval(function () {
      me.$refs.chart.updateSeries([{
        data: me.$store.state.stockPrices[me.stock.name],
      }])
    }, 5000);
  },
};
</script>

<style scoped>
.danger {
  border: 1px solid red;
}
</style>
