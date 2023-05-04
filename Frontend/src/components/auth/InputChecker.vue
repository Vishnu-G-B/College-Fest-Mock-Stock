<script>
export default {
  props: ["inputValue", "email", "password", "confirmPassword"],
  data() {
    return {
      lengthId: 'length-requirement',
      alphaNeumericId: 'alpha-neumeric',
      specialCharacterId: 'special-character',
      confirmPasswordId: 'confirm-password-id',
      emailId: 'email-id'
    }
  },
  watch: {
    inputValue(newValue) {
      this.checkInput(newValue, this.inputValue);
    }
  },
  mounted() {
    this.checkInput("", this.inputValue);
  },
  methods: {
    checkInput(newValue, inputValue) {
      if (this.password) {
        if (newValue.length > 6 || inputValue.length > 6) {
          this.lengthId = this.addToId(this.lengthId, "-correct")
        } else {
          this.lengthId = this.lengthId.replace("-correct", "")
        }
        var regex = /\d/g;
        if (regex.test(newValue) || regex.test(inputValue)) {
          this.alphaNeumericId = this.addToId(this.alphaNeumericId, "-correct")
        } else {
          this.alphaNeumericId = this.alphaNeumericId.replace("-correct", "")
        }

        var regexFormat = /[ `!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?~]/;
        if (regexFormat.test(newValue) || regexFormat.test(inputValue)) {
          this.specialCharacterId = this.addToId(this.specialCharacterId, "-correct");
        } else {
          this.specialCharacterId = this.specialCharacterId.replace("-correct", "")
        }
      }
      else if (this.confirmPassword["truthValue"]) {
        console.log(this.confirmPassword["value"])
        if (newValue == this.confirmPassword["value"] || inputValue == this.confirmPassword["value"]) {
          this.confirmPasswordId = this.addToId(this.confirmPasswordId, "-correct")
        } else {
          this.confirmPasswordId = this.confirmPasswordId.replace("-correct", "")
        }
      }
      // else if (this.email) {
      //   var emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      //   if (emailRegex.test(newValue) || emailRegex.test(inputValue)) {
      //     this.emailId = this.addToId(this.emailId, "-correct")
      //   } else {
      //     this.emailId = this.emailId.replace("-correct", "")
      //   }
      // }
    },
    addToId(idToAddTo, whatToAdd) {
      if (!idToAddTo.includes(whatToAdd)) {
        return idToAddTo + whatToAdd;
      } else {
        return idToAddTo;
      }
    }
  }
}

</script>

<template>
  <div id="expected-input-container">
    <ul id="expected-input-list" v-if="password">
      <li :id="lengthId">Password should be longer than 6 characters</li>
      <li :id="alphaNeumericId">Password should contain at least one numerical character</li>
      <li :id="specialCharacterId">Password should contain at least one special character</li>
    </ul>
    <ul id="expected-input-list" v-if="confirmPassword['truthValue']">
      <li :id="confirmPasswordId">Confirm password must be equal to password</li>
    </ul>
    <ul id="expected-input-list" v-if="email">
      <li :id="emailId">
        Please enter a valid email
      </li>
    </ul>
  </div>
</template>

<style>
ul{
  font-size: 18px;
  text-align: left;
}

li {
  color: red;
}

li[id$="-correct"]{
  color: green;
}
/* 

#alpha-neumeric {
  color: red;
}

#special-character {
  color: red;
}

#length-requirement-correct {
  color: green;
}

#alpha-neumeric-correct {
  color: green;
}

#special-character-correct {
  color: green;
} */
</style>