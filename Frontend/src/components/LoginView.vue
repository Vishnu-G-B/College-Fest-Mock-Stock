<script>
import AuthBase from './auth/AuthBase.vue'

export default {
	components: {
		AuthBase
	},
	data() {
		return {
			redirectLink: '',
			emailErrorMessage: '',
			passwordErrorMessage: '',
			emailId: 'email',
			passwordId: 'password',
		}
	},
	methods: {
		beforeMount() {
			const data = require('../config_frontend.json');
			this.redirectLink = data['websiteURL'];
		},
		onSubmit(credentials) {
			var data = { "email": credentials['email'], "password": credentials['password']};
			console.log(data);
			fetch(this.$store.state.nb + "api/v1/auth/login", {
				method: "POST",
				headers: {
					"Authorization": "Test",
					"Content-Type": "application/json",
				},
				body: JSON.stringify(data),
			})
				.then((response) => response.json())
				.then((data) => {
					console.log(data);
					this.$store.dispatch("setIsLoggedIn", true);
					this.$router.push({name: "stocks"});
					this.$store.dispatch("setUserId", data['user_id']);
					// if (data['status'] === 'failure') {
					// 	if (data['password_message'] !== "validated") {
					// 		this.passwordId = "password-error"
					// 		this.passwordErrorMessage = data['password_message']
					// 	}
					// 	if (data['email_message'] !== "validated") {
					// 		this.emailId = "email-error"
					// 		this.emailErrorMessage = data['email_message']
					// 	}
					// 	if (data['confirm_message'] !== "validated") {
					// 		this.confirmPasswordId = "confirm-password-error"
					// 		this.confirmPasswordErrorMessage = data['confirm_password_message']
					// 		console.log(this.confirmPasswordErrorMessage);
					// 	}
					// } else if(data['status'] === 'success'){
					// 	this.$store.dispatch("setIsLoggedIn", true);
					// 	this.$router.push({name: 'stocks'});
					// }
				});
		},
	},
}
</script>

<template>
	<AuthBase :divHeadingId="'loginText'" :mainHeadingPId="'login-text'" :explanationPId="'login-explanation'"
		:mainHeadingContent="'Login'" :explanationContent="'Continue on your journey'" :emailId="emailId"
		:password-id="passwordId" :email-error-message="emailErrorMessage" :password-error-message="passwordErrorMessage"
		@form-submitted="onSubmit">
		<template v-slot:redirect-to-opp-page>
			<a id="redirect-link" v-bind:href="redirectLink + '/signup'">Create an account ?</a>
		</template>
	</AuthBase>
</template>

<style>
#login-heading {
	font-size: 25px;
	vertical-align: bottom;
}

#login-text {
	font-size: 35px;
	font-weight: bolder;
}

p {
	margin-top: 10px;
	margin-bottom: 10px;
}

#login-explanation {
	color: #666666;
	font-weight: bold;
	font-size: 18px;
}

#redirect-link {
	font-size: 18px;
	padding-left: 2px;
}
</style>