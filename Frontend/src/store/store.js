import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export const store = new Vuex.Store({
    plugins: [
        createPersistedState({
            paths: [
                "stock",
                "isLoggedIn",
                "funds",
                "heldStocks",
                "userId",
                "nb",
                "priceb",
                "history",
                "stockPrices",
            ],
            storage: window.sessionStorage,
        }),
    ],
    state: {
        stock: [{}],
        history: [],
        nb: "http://localhost:5000/",
        priceb: "http://localhost:5001/",
        heldStocks: [{}],
        eventSource: new EventSource(
            // "http://172.20.15.33:5001/api/v1/listenforstocks",
            "http://172.20.16.169:5001/api/v1/listenforstocks",
            {}
        ),
        isLoggedIn: false,
        funds: 0,
        fundsError: "",
        fundsErrorBool: false,
        userId: "",
        stockPrices: {},
    },

    getters: {
        isLoggedIn(state) {
            console.log(state.isLoggedIn);
            return state.isLoggedIn;
        },
        modifiedHeldStocks(state) {
            console.log(state.heldStocks["history"][0]);
            return state.heldStocks["history"];
        },
        userId(state) {
            return state.userId;
        },
        nb(state) {
            return state.nb;
        },
        priceb(state) {
            return state.priceb;
        },
    },

    mutations: {
        setStock: (state, value) => {
            state.stock = value;
            for (let index in state.stock) {
                const stockName = state.stock[index].name;
                const stockPrice = parseInt(state.stock[index].price);
                if (!state.stockPrices[stockName]) {
                    state.stockPrices[stockName] = [];
                }
                state.stockPrices[stockName].push(stockPrice);
            }
            console.log(state.stockPrices);
        },
        setIsLoggedIn: (state, value) => {
            state.isLoggedIn = value;
        },
        setFunds: (state, value) => {
            state.funds = value;
        },
        setErrorFunds: (state, value) => {
            state.fundsError = value;
        },
        setErrorFundsBool: (state, value) => {
            state.fundsErrorBool = value;
        },
        setHeldStocks: (state, value) => {
            state.heldStocks = value;
        },
        initFunds: (state, value) => {
            state.funds = value;
        },
        setUserId: (state, value) => {
            state.userId = value;
        },
    },
    actions: {
        setStock: (context, payload) => {
            context.commit("setStock", payload);
        },
        setIsLoggedIn: (context, payload) => {
            context.commit("setIsLoggedIn", payload);
        },
        setUserId: (context, payload) => {
            context.commit("setUserId", payload);
        },
        initFunds: (context) => {
            // fetch("http://172.20.15.33:5000/api/v1/home/getfunds", {
            let data = {
                userId: context.getters.userId,
            };
            fetch(context.getters.nb + "api/v1/home/getfunds", {
                method: "POST",
                headers: {
                    Authorization: "Test",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
                .then((response) => response.json())
                .then((data) => {
                    context.commit("initFunds", data[0]["funds"]);
                });
        },
        buyStocks: (context, payload) => {
            let data = {
                stockName: payload["name"],
                quantity: payload["quantity"],
                operation: "buy",
                userId: context.getters.userId,
            };
            // fetch("http://172.20.15.33:5000/api/v1/home/operation", {
            fetch(context.getters.nb + "api/v1/home/buy", {
                method: "POST",
                headers: {
                    Authorization: "Test",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    if ("error" in data) {
                        context.commit("setErrorFunds", data["error"]);
                        context.commit("setErrorFundsBool", true);
                        setTimeout(() => {
                            context.dispatch("removeFundsError");
                        }, 5000);
                    } else if ("funds" in data) {
                        context.commit("setFunds", data["funds"]);
                        context.commit("setHeldStocks", data["held_stocks"]);
                    }
                });
        },
        shortBuyStocks: (context, payload) => {
            let data = {
                stockName: payload["name"],
                quantity: payload["quantity"],
                operation: "short_buy",
                userId: context.getters.userId,
            };
            // fetch("http://172.20.15.33:5000/api/v1/home/operation", {
            fetch(context.getters.nb + "api/v1/home/short-buy", {
                method: "POST",
                headers: {
                    Authorization: "Test",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    if ("error" in data) {
                        context.commit("setErrorFunds", data["error"]);
                        context.commit("setErrorFundsBool", true);
                        setTimeout(() => {
                            context.dispatch("removeFundsError");
                        }, 5000);
                    } else if ("funds" in data) {
                        context.commit("setFunds", data["funds"]);
                        context.commit("setHeldStocks", data["held_stocks"]);
                    }
                });
        },
        shortSellStocks: (context, payload) => {
            let data = {
                stockName: payload["name"],
                quantity: payload["quantity"],
                operation: "buy",
                userId: context.getters.userId,
            };
            // fetch("http://172.20.15.33:5000/api/v1/home/operation", {
            fetch(context.getters.nb + "api/v1/home/short-sell", {
                method: "POST",
                headers: {
                    Authorization: "Test",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    if ("error" in data) {
                        context.commit("setErrorFunds", data["error"]);
                        context.commit("setErrorFundsBool", true);
                        setTimeout(() => {
                            context.dispatch("removeFundsError");
                        }, 5000);
                    } else if ("funds" in data) {
                        context.commit("setFunds", data["funds"]);
                        context.commit("setHeldStocks", data["held_stocks"]);
                    }
                });
        },
        removeFundsError: (context) => {
            context.commit("setErrorFunds", "");
            context.commit("setErrorFundsBool", false);
        },
        getHeldStocks: (context) => {
            // fetch("http://172.20.15.33:5000/api/v1/home/getheldstocks", {
            let data = {
                userId: context.getters.userId,
            };
            fetch(context.getters.nb + "api/v1/home/getheldstocks", {
                method: "POST",
                headers: {
                    Authorization: "Test",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
                .then((response) => response.json())
                .then((data) => {
                    context.commit("setHeldStocks", data);
                });
        },
        sellStocks: (context, payload) => {
            // fetch("http://172.20.15.33:5000/api/v1/home/operation", {
            payload["userId"] = context.getters.userId;
            fetch(context.getters.nb + "api/v1/home/sell", {
                method: "POST",
                headers: {
                    Authorization: "Test",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            })
                .then((response) => response.json())
                .then((data) => {
                    if ("funds" in data) {
                        context.commit("setHeldStocks", data["held_stocks"]);
                        context.commit("setFunds", data["funds"]);
                    } else if ("error" in data) {
                        context.commit("setErrorFunds", data["error"]);
                        context.commit("setErrorFundsBool", true);
                        setTimeout(() => {
                            context.dispatch("removeFundsError");
                        }, 5000);
                    }
                });
        },
    },
});
