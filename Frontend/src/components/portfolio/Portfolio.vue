<template>
  <div>
    <h3 style="margin-bottom:35px;padding-left:14px;">
      Present in chronological order
    </h3>
    <app-stock v-for="stock in heldStocks" :key="stock.id" :stock="stock"></app-stock>
  </div>
</template>

<script>
import Stock from "./Stock.vue";

export default {
  computed: {
    heldStocks() {
      return this.$store.getters.modifiedHeldStocks;
    },
  },
  components: {
    appStock: Stock,
  },
  mounted() {
    this.$store.dispatch("getHeldStocks");
  },
};
</script>