<script>
export default {
  data() {
    return {
      supabaseReturnedParams: [],
      noError: false,
      errorDescription: "",
      errorCode: "",
      messageExclamation: "Error 404",
      messageInformation: "Not Found",
    }
  },
  methods: {
  },
  created() {
    let temp = this.$route.hash;
    let tempList = temp.split("&");
    tempList[0] = tempList[0].replace("#", "");
    if (tempList[0].includes("error")) {
      this.noError = false;
      this.errorCode = tempList[1].replace("error_code=", "");
      this.errorDescription = tempList[2].replace("error_description=", "");
      this.errorDescription = this.errorDescription.replaceAll("+", " ");
      this.messageExclamation = this.errorCode + " Error";
      this.messageInformation = this.errorDescription;
    }
    if (tempList[0].includes("access_token")) {
      this.noError = true;
      this.supabaseReturnedParams[0] = tempList[0].replace("access_token=", "");
      this.messageExclamation = "Email Verified!";
      this.messageInformation = "You can close this page and continue to login";
    }
  },
  mounted() {
    if (this.noError == true) {
      setTimeout(() => this.$router.push({ path: '/login' }), 5000);
    }
  }
}
</script>

<template>
  <div id="main-content">
    <div id="container">
      <div id="image-container">
        <img v-if="noError" src="../assets/verify-email.png" alt="email verified image">
      </div>
      <p id="message-exclamation">
        {{ messageExclamation }}
      </p>
      <p id="message-information">
        {{ messageInformation }}
      </p>
      <p v-if="noError" id="redirect">
        you will soon be redirected 
      </p>
    </div>
  </div>
</template>

<style>
#main-content {
  width: max-content;
  height: max-content;

  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;

  margin: auto;
}

#container {
  display: grid;
  justify-content: center;
  align-items: center;
}

#image-container {
  justify-self: center;
}

#message-exclamation {
  text-align: center;
  font-size: 40px;
  font-weight: bolder;
}

#message-information {
  font-size: 40px;
  text-align: center;
}

#redirect {
  font-size: 35px;
  text-align: center;
}
</style>