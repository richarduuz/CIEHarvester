<template>
  <modal name="login">
    <div class="container">
      <div class="input-container">
        <h2>输入密码进入系统</h2>
        <span>请输入密码: </span>
        <input v-model="password" type="password">
        <br>
        <br>
        <h2>或者你是管理员，你想重制密码: </h2>
        <span>请输入密码: </span>
        <input v-model="adminPassword" type="password">
      </div>
      <div class="btn-container">
        <p class="login-alert" v-show="adminPassword.length !== 0 && password.length !== 0">请只输入一个密码</p>
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
          if (data['message'] === 'right'){
            this.password = ''
            this.adminPassword = ''
            if (data['isAdmin']){
              this.$emit('showResetpswModal')
            }
            else{
              this.gotoSearch()
            }
          } else {
            alert('密码不正确')
          }
        })
        .catch((e) => {
          alert(str(e))
        })
    },
    gotoSearch(){
      let path = '/search'
      this.$router.push({
        path
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

p.login-alert{
  font-size: 15px;
  color: red;
  float: left;
  margin: 0;
}

</style>