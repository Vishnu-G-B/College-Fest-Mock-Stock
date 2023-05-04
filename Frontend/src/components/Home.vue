<template>
  <div class="col-sm-8 col-md-7">
    <h1>Trade or View your Portfolio</h1>
    <h4>Available stocks with their current price will be available under the stocks tab</h4>
    <h4>Bought stocks with their prices will be available in chronological order under the portfolio tab</h4>
    <h4>Your current available funds is shown on the navbar on the top left</h4>
    <hr />
    <h4>Your Funds: {{ funds | currency }}</h4>
  </div>
</template>

<script>
export default {
  data() {
    return {
      funds: this.$funds,
      currency: this.$currency,
    }
  }
};
</script>