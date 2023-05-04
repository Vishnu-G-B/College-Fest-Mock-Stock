<script>
import AuthBase from './auth/AuthBase.vue';

export default {
	components: {
		AuthBase,
	},
	data() {
		return {
			redirectLink: '',
			confirmPassword: '',
			emailErrorMessage: '',
			passwordErrorMessage: '',
			confirmPasswordErrorMessage: '',
			emailId: 'email',
			passwordId: 'password',
			confirmPasswordId: 'confirm-password',
			confirmPasswordFocused: false,
			tempPasswordValue: '',
		}
	},
	methods: {
		beforeMount() {
			const data = require('../config_frontend.json');
			this.redirectLink = data['websiteURL'];
		},
		onSubmit(credentials) {
			console.log(credentials['email']);
			var data = { "email": credentials['email'], "password": credentials['password'], "confirmPassword": this.confirmPassword };
			fetch("http://localhost:5000/api/v1/auth/signup", {
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
					if (data['status'] === 'failure') {
						if (data['password_message'] !== "validated") {
							this.passwordId = "password-error"
							this.passwordErrorMessage = data['password_message']
						}
						if (data['email_message'] !== "validated") {
							this.emailId = "email-error"
							this.emailErrorMessage = data['email_message']
						}
						if (data['confirm_message'] !== "validated") {
							this.confirmPasswordId = "confirm-password-error"
							this.confirmPasswordErrorMessage = data['confirm_password_message']
							console.log(this.confirmPasswordErrorMessage);
						}
					}
				});
		},
		removeError(event) {
			if (event.currentTarget.id === "email-error") {
				this.emailId = this.emailId.replace("-error", "")
				this.emailErrorMessage = '';
			}
			else if (event.currentTarget.id === "password-error") {
				this.passwordId = this.passwordId.replace("-error", "");
				this.passwordErrorMessage = '';
			}
			else {
				this.confirmPasswordId = this.confirmPasswordId.replace("-error", "");
				this.confirmPasswordErrorMessage = '';
			}
		},
	}
}
</script>

<template>
	<AuthBase :divHeadingId="'signUpText'" :mainHeadingPId="'sign-up-text'" :explanationPId="'sign-up-explanation'"
		:mainHeadingContent="'Sign Up'" :explanationContent="'Get started with your typing journey'"
		@form-submitted="onSubmit" @remove-error="removeError" :emailId="emailId" :password-id="passwordId"
		:email-error-message="emailErrorMessage" :password-error-message="passwordErrorMessage">
		<template v-slot:additional-input-fields>
			<div id="confirm-password-input">
				<input v-model="confirmPassword" type="password" name="signconfirmpassword" :id="confirmPasswordId"
					placeholder="Confirm Password" @click="removeError($event)">
				<p id="confirm-password-error-message"> {{ confirmPasswordErrorMessage }} </p>
			</div>
		</template>
		<template v-slot:redirect-to-opp-page>
			<a id="redirect-link" v-bind:href="redirectLink + '/login'">Already have an account ?</a>
		</template>
	</AuthBase>
</template>


<style>
#sign-up-heading {
	font-size: 25px;
	vertical-align: bottom;
}

#sign-up-text {
	font-size: 35px;
	font-weight: bolder;
}

p {
	margin-top: 10px;
	margin-bottom: 10px;
}

#sign-up-explanation {
	color: #666666;
	font-weight: bold;
	font-size: 18px;
}

#redirect-link {
	font-size: 18px;
	padding-left: 2px;
}

#confirm-password {
	border: 1px #666666 solid;
	border-radius: 5px;
	font-size: 18px;
	line-height: 45px;
	width: 100%;
	padding: 5px;
}

#confirm-password-error {
	border: 3px red solid;
	border-radius: 5px;
	font-size: 18px;
	line-height: 45px;
	width: 100%;
	padding: 5px;
}

#confirm-password-error-message {
	text-align: left;
	font-size: 18px;
	color: red;
	padding-left: 2px;
}

#confirm-password-input {
	padding-right: 25px;
	padding-left: 10px;
}
</style>
