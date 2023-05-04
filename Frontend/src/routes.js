import Home from "./components/Home.vue";
import Portfolio from "./components/portfolio/Portfolio.vue";
import Stocks from "./components/stocks/Stocks.vue";
import LoginView from "./components/LoginView.vue";
import SignUpView from "./components/SignUpView.vue";
import EmailLinkView from "./components/EmailLinkView.vue";

export const routes = [
    { name: "signup", path: "/signup", component: SignUpView },
    { name: "login", path: "/login", component: LoginView },
    { path: "/signup/verified", component: EmailLinkView },
    {
        path: "/",
        component: Home,
        meta: {
            requiresAuth: true,
        },
    },
    {
        name: "portfolio",
        path: "/portfolio",
        component: Portfolio,
        meta: {
            requiresAuth: true,
        },
    },
    {
        name: "stocks",
        path: "/stocks",
        component: Stocks,
        meta: {
            requiresAuth: true,
        },
    },
];
