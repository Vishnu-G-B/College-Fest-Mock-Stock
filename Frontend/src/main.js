import Vue from "vue";
import VueRouter from "vue-router";
import VueResource from "vue-resource";
// import * as io from "socket.io-client";
// import VueSocketIO from "vue-socket.io";

import App from "./App.vue";
import { routes } from "./routes";
import { store } from "./store/store";

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(VueResource);
// Vue.use(
//     new VueSocketIO({
//         debug: true,
//         connection: io('http://10.29.90.96:5001'),
//     })
// );

Vue.http.options.root = "https://vue-stock-trader-906bc.firebaseio.com/";
Vue.prototype.$funds = 1000000;
Vue.prototype.$currency = "₹";

Vue.filter("currency", (value) => {
    return "₹ " + value.toLocaleString();
});

const router = new VueRouter({
    routes,
    mode: "history",
});

router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (store.getters.isLoggedIn) {
            next();
        } else {
            next({ name: "login" });
        }
    } else {
        next();
    }
});

new Vue({
    router,
    store: store,
    render: (h) => h(App),
}).$mount("#app");
