<template>
  <nav class="navbar navbar-inverse">
    <div class="container-fluid">
      <div class="navbar-header">
        <!-- Stock Trader text -> click return to home page -->
        <router-link class="navbar-brand" to="/">Stock Trader</router-link>
      </div>
      <div class="collapse navbar-collapse">
        <ul class="nav navbar-nav">
          <!-- Portfolio text -> click return to portfolio page -->
          <router-link to="/portfolio" active-class="active" tag="li">
            <a>Portfolio</a>
          </router-link>
          <!-- Stocks text -> click return to stocks page -->
          <KeepAlive>
            <router-link to="/stocks" active-class="active" tag="li">
              <a>Stocks</a>
            </router-link>
          </KeepAlive>
        </ul>
        <!-- shows amount of funds available on the top right of the navbar -->
        <strong class="navbar-text navbar-right">Funds: {{ funds | currency }}</strong>
        <!-- <ul class="nav navbar-nav navbar-right">
          <li>
            <a href="" @click.prevent="endDay">End Day</a>
          </li>
          <li
            class="dropdown"
            :class="{ open: isDropdownOpen }"
            @click="isDropdownOpen = !isDropdownOpen"
          >
            <a
              href="#"
              @click.prevent
              class="dropdown-toggle"
              data-toggle="dropdown"
              role="button"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Save &amp; Load
              <span class="caret"></span>
            </a>
            <ul class="dropdown-menu">
              <li>
                <a href="" @click.prevent="saveData">Save Data</a>
              </li>
              <li>
                <a href="" @click.prevent="loadData">Load Data</a>
              </li>
            </ul>
          </li>
        </ul> -->
      </div>
    </div>
  </nav>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      isDropdownOpen: false,
    };
  },
  methods: {
    ...mapActions({
      randomizeStocks: 'randomizeStocks',
      fetchData: 'loadData',
    }),
    endDay() {
      this.randomizeStocks();
    },
    saveData() {
      const data = {
        funds: this.$store.getters.funds,
        stockPortfolio: this.$store.getters.stockPortfolio,
        stocks: this.$store.getters.stocks,
      };
      this.$http.put("data.json", data);
    },
    loadData() {
      this.fetchData();
    },
  },
  computed: {
    funds() {
      return this.$store.state.funds;
    }
  },
  // watch: {
  //   funds (newValue){
  //     console.log(newValue);
  //     return this.funds();
  //   }
  // }
};
</script>

<style scoped>
.hidden-text {
  visibility: hidden;
}

.hidden-text:hover {
  visibility: visible;
}
</style>