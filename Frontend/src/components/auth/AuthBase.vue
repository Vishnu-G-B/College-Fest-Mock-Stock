<script>
import InputChecker from './InputChecker.vue';

export default {
  props: ["divHeadingId", "mainHeadingPId", "explanationPId", "mainHeadingContent", "explanationContent", "emailErrorMessage", "passwordErrorMessage", "emailId", "passwordId"],
  components: {
    InputChecker
  },
  data() {
    return {
      email: '',
      password: '',
      emailValidationDisplay: false,
      passwordValidationDisplay: false,
    }
  },
  methods: {
    onSubmit(email, password) {
      console.log("form submitted");
      this.$emit('form-submitted', { email, password })
    },
    removeError(event) {
      this.$emit('removeError', event);
    },
    inputFieldFocused(event) {
      if (event.target.id == this.emailId) {
        this.emailValidationDisplay = true
      } else if (event.target.id == this.passwordId) {
        this.passwordValidationDisplay = true
      }
    },
    inputFieldUnFocused(event) {
      console.log(event.target.id)
      if (event.target.id == this.emailId) {
        this.emailValidationDisplay = false
      } else if (event.target.id == this.passwordId) {
        this.passwordValidationDisplay = false
      }
    }
  },
}
</script>

<template>
  <div id="all-container">
    <div id="info-container">
      <div id="company-name-heading">
        <p id="company-name-text">
          Welcome to BULLS VS BEARS
        </p>
      </div>
      <div id="to-contribute">
        <p id="to-contribute-text">
          Enter the email id and password provided to your team
        </p>
      </div>
    </div>
    <div id="auth-container-wrapper">

      <div id="auth-container">
        <div :id="divHeadingId">
          <p :id="mainHeadingPId">{{ mainHeadingContent }}</p>
          <p :id="explanationPId">{{ explanationContent }}</p>
        </div>
        <div id="email-input">
          <input v-model="email" type="email" name="signemail" :id="emailId" placeholder="Email Id"
            @click="removeError($event)" @focusin="inputFieldFocused($event)" @focusout="inputFieldUnFocused($event)">
          <p id="email-error-message">{{ emailErrorMessage }}</p>
          <InputChecker v-if="emailValidationDisplay" :input-value="email" :confirm-password="{ 'truthValue': false }"
            :password="false" :email="true" />
        </div>
        <div id="password-input">
          <input v-model="password" type="password" name="signpassword" :id="passwordId" placeholder="Password"
            ref="password" @click="removeError($event)" @focusin="inputFieldFocused($event)"
            @focusout="inputFieldUnFocused($event)">
          <p id="password-error-message"> {{ passwordErrorMessage }} </p>
          <InputChecker v-if="passwordValidationDisplay" :input-value="password"
            :confirm-password="{ 'truthValue': false }" :password="true" :email="false" />
        </div>
        <slot name="additional-input-fields"></slot>
        <div id="submit-button-wrapper">
          <input @click="onSubmit(email, password)" type="submit" value="Submit" id="submit">
        </div>
        <slot name="redirect-to-opp-page"></slot>
      </div>

    </div>
  </div>
</template>

<style>
body {
  padding: 5px;
}

#app {
  height: 90vh;
}

#all-container {
  display: grid;
  grid-template-columns: 0.45fr 1fr;
  height: max-content;
  overflow: hidden;
}

#caution-container {
  display: grid;
  grid-template-rows: 1fr 1fr 1fr;
  height: 5%;
  z-index: 3;
}

#info-container {
  padding: 45px;
  display: grid;
  row-gap: 95px;
  grid-template-rows: 0.25fr 1fr;
  height: 100%;
}

#company-name-heading {
  text-align: left;
  align-self: center;
  justify-self: center;
  font-size: 58px;
  font-weight: bolder;
}

#to-contribute {
  font-size: 28px;
  font-weight: bold;
  color: #666666;
  text-align: left;
}

#auth-container-wrapper{
  height: 80%;
  width: 100%;
  display: grid;
}


#auth-container {
  justify-self: center;
  align-self: center;
  overflow-y: auto;
  border-radius: 10px;
  padding-right: 35px;
  padding-left: 35px;
  padding-top: 10px;
  padding-bottom: 25px;
  grid-column-start: 2;
  grid-column-end: -1;
  row-gap: 15px;
  height: 85%;
  width: 75%;
  display: grid;
  grid-template-rows: 0.25fr 1fr 1fr 1fr;
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;
}

#email-input,
#password-input {
  padding-right: 25px;
  padding-left: 10px;
}

#email-input {
  align-self: flex-end;
}

#password-input {
  align-self: flex-start;
}

#email,
#password {
  border: 1px #666666 solid;
  border-radius: 5px;
  font-size: 18px;
  line-height: 45px;
  width: 100%;
  padding: 5px;
}

#email-error,
#password-error {
  border: 3px red solid;
  border-radius: 5px;
  font-size: 18px;
  line-height: 45px;
  width: 100%;
  padding: 5px;
}

#email-error-message,
#password-error-message {
  text-align: left;
  font-size: 18px;
  color: red;
  padding-left: 2px;
}

#submit-button-wrapper {
  width: 100%;
  height: 100%;
  display: grid;
}

#submit {
  width: 100%;
  height: 45px;
  padding: 5px;
  font-size: 18px;
  border: 1px #666666 solid;
  border-radius: 5px;
  align-self: center;
  font-weight: bold;
}
</style>