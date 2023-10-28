<template>
  <div class="container-fluid">
    <div v-if="fundsErrorBool" class="alert alert-danger sticky-div" role="alert">
      <strong>
        {{ fundsError }}
      </strong>
      <!-- <div class="modal fade" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span
                  aria-hidden="true">&times;</span></button>
              <h4 class="modal-title">Modal title</h4>
            </div>
            <div class="modal-body">
              <p>One fine body&hellip;</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary">Save changes</button>
            </div>
          </div>
        </div>
      </div>/.modal -->
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

.sticky-div {
  position: -webkit-sticky;
  position: sticky;
  top: 20px;
  z-index: 11;
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
