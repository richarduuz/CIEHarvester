<template>
  <modal name="login">
    <div class="container">
      <div class="input-container">
        <h2>输入密码进入系统</h2>
        <span>请输入密码: </span>
        <input v-model="password">
        <br>
        <br>
        <h2>或者你是管理员，你想重制密码: </h2>
        <span>请输入密码: </span>
        <input v-model="adminPassword">
      </div>
      <div class="btn-container">
        <button class="submit-btn" @click="authID" :disabled="password.length === 0 && adminPassword.length === 0">确认</button>
      </div>
    </div>
  </modal>
</template>

<script>
export default {
  name: "LoginModal",
  data(){
    return {
      password: '',
      adminPassword: ''
    }
  },
  methods: {
    test(){
      console.log(this.password.length);
      console.log(this.adminPassword.length);
    },

    authID(){
      let url = this.$store.state.url + '/auth'
      console.log(url);
      let postData = {}
      if (this.password.length === 0){
        postData['adminPassword'] = this.adminPassword
      } else {
        postData['password'] = this.password
      }
      postData = JSON.stringify(postData)
      this.$http.post(url, postData)
        .then(response => response.json())
        .then(data => {
          if (data){
            alert('Okay')
          }
        })
        .catch((e) => {
          alert(str(e))
        })
    }
  }
}
</script>

<style scoped>
div.container{
  position: absolute;
  text-align: left;
  height: 100%;
  width: 100%;
}
div.input-container{
  margin: 10px;
}

div.btn-container{
  margin: 10px;
  bottom: 0;
}
button.submit-btn{
  float: right;
}

</style>