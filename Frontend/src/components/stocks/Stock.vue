<template>
  <div class="col-sm-6 col-md-4">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title">
          <strong> 
            {{ stock.name }}
          </strong>
          <div class="pull-right">
            Price: {{ stock.price }} &nbsp;&nbsp;
            Quantity: {{ heldStocks[stock.name] || 0}}
          </div>
        </h3>
      </div>
      <div class="panel-body">
        <div class="pull-left">
          <input type="number" class="form-control" placeholder="Quantity" v-model.number="quantity"
            :class="{ danger: insufficientFundsBuy || insufficientQuantitySell}" />
        </div>
        <div class="pull-right">
          <button class="btn btn-success" @click="buyStock"
            :disabled="stock.price <= 0|| quantity <= 0 || !Number.isInteger(quantity)">Buy</button>
          <button class="btn btn-danger" @click="sellStock"
            :disabled="stock.price <= 0 || quantity <= 0 || !Number.isInteger(quantity)">
            Sell
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["stock"],
  data() {
    return {
      quantity: "",
    };
  },
  computed: {
    funds() {
      return this.$store.state.funds;
    },
    insufficientFundsBuy() {
      return this.quantity * this.stock.price > this.funds;
    },
    insufficientQuantitySell(){
      return this.quantity > this.$store.state.heldStocks[this.stock.name]
    },
    heldStocks() {
      return this.$store.state.heldStocks;
    }
  },
  methods: {
    buyStock() {
      const order = {
        stockId: this.stock.id,
        name: this.stock.name,
        quantity: this.quantity,
      };
      this.$store.dispatch("buyStocks", order);
      this.quantity = 0;
    },
    sellStock() {
      const order = {
        stockId: this.stock.id,
        stockName: this.stock.name,
        quantity: this.quantity,
        operation: "sell",
      };
      this.$store.dispatch("sellStocks", order);
      this.quantity = 0;
    }
  },
};
</script>

<style scoped>
.danger {
  border: 1px solid red;
}
</style>
