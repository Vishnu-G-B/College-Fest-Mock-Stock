<template>
  <div class="container-fluid">
    <div v-if="fundsErrorBool" class="alert alert-danger" role="alert">
      <strong> 
        {{ fundsError }}
      </strong>
    </div>
    <app-header></app-header>
    <div class="row">
      <div class="col-xs-12">
        <transition name="slide" mode="out-in">
          <router-view></router-view>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import io from 'socket.io-client';

export default {
  components: {
    appHeader: Header,
  },
  data() {
    return {
      loggedin: false,
      connection: '',
    }
  },
  methods: {
    message(e) {
      try {
        if ("data" in e) {
          if (e['data'] === false) {
            console.log('false');
          }
          else {
            this.$store.dispatch("setStock", e);
          }
        } else {
          this.$store.dispatch("setStock", e);
        }
      } catch (err) {
        console.log("false");
      }
    },
  },
  computed: {
    fundsError() {
      return this.$store.state.fundsError;
    },
    fundsErrorBool() {
      return this.$store.state.fundsError;
    }
  },
  mounted() {
    const socket = io.connect(this.$store.state.priceb);
    socket.on('connect', function () {
      console.error('connected to webSocket');
      //sending to server
    });

    // we have to use the arrow function to bind this in the function
    // so that we can access Vue  & its methods
    socket.on('new_data', (data) => {
      this.message(data);
    });
    // this.$socket.on("new_data", (data) => {
    //   console.log(data);
    // });
    // this.$store.state.eventSource.addEventListener("open", () => {
    //   console.log("Connection Established!");
    // });
    // this.$store.state.eventSource.addEventListener("message", (e) => {
    //   this.message(e)
    // });
  },
  beforeUnmount() {
    this.$store.dispatch("setIsLoggedIn", false);
  },
};
</script>

<style>
html {
  font-size: 90px;
}

body {
  padding: 30px;
}

.slide-enter-active {
  animation: slide-in 200ms ease-out forwards;
}

.slide-leave-active {
  animation: slide-out 200ms ease-out forwards;
}

@keyframes slide-in {
  from {
    transform: translateY(-30px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slide-out {
  from {
    transform: translateY(0);
    opacity: 1;
  }

  to {
    transform: translateY(-30px);
    opacity: 0;
  }
}
</style>
