<template>
  <div class="col-sm-6 col-md-4">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title">
          <strong>
            {{ stock.stock_name }}
          </strong>
          <div class="pull-right">
            Op: {{ stock.operation.toUpperCase() }}
            Price: {{ stock.current_stock_value }} &nbsp;&nbsp;
            Quantity: {{ stock.quantity }}
          </div>
        </h3>
      </div>
      <!-- <div class="panel-body">
        <div class="pull-left">
          <input
            type="number"
            class="form-control"
            placeholder="Quantity"
            v-model.number="quantity"
            :class="{ danger: insufficientQuantity }"
          />
        </div>
        <div class="pull-right">
          <button
            class="btn btn-success"
            @click="sellStock"
            :disabled="insufficientQuantity || quantity <= 0 || !Number.isInteger(quantity)"
          >Sell</button>
        </div>
      </div> -->
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
    insufficientQuantity() {
      return this.quantity > this.stock.quantity;
    },
  },
  methods: {
    sellStock() {
      const order = {
        stockId: this.stock.id,
        stockPrice: this.stock.price,
        quantity: this.quantity,
      };
      this.$store.dispatch("sellStock", order);
      this.quantity = 0;
    },
  },
};
</script>

<style scoped>
.danger {
  border: 1px solid red;
}
</style>
