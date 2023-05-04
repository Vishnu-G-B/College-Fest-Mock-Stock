<template>
  <div>
    <app-stock v-for="stock in stockObj" :key="stock.id" :stock="stock"></app-stock>
  </div>
</template>

<script>
import Stock from "./Stock.vue";

export default {
  components: {
    appStock: Stock,
  },
  computed: {
    getData() {
      return this.$store.state.stock;
    }
  },
  watch: {
    getData(newValue) {
      this.stockObj = newValue;
    }
  },
  data() {
    return {
      stockObj: this.$store.state.stock,
    }
  },
  methods: {
  },
  mounted() {
    this.$store.dispatch("initFunds");
    this.$store.dispatch("getHeldStocks");
  }
}
</script>