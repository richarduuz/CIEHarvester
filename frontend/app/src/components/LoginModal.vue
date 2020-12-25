<template>
  <modal name="login" :adaptive="true">
    <div class="container">
      <div class="input-container">
        <h2>输入密码进入系统</h2>
        <span>请输入密码: </span>
        <input v-model="password" type="password">
        <br>
        <div class="btn-container">
          <button class="submit-btn" @click="authID" :disabled="password.length === 0">确认</button>
        </div>
        <br>
        <h2>或者你是管理员，你想重制密码: </h2>
        <button @click="showAdminLogin">管理员登录</button>
        <admin-login-modal></admin-login-modal>
      </div>

    </div>
  </modal>
</template>

<script>
import AdminLoginModal from "@/components/AdminLoginModal";

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
    showAdminLogin(){
      this.$emit('showAdminLogin')
    },
    authID(){
      let url = this.$store.state.url + '/auth'
      console.log(url);
      let postData = {}
      postData['password'] = this.password;
      postData = JSON.stringify(postData)
      this.$http.post(url, postData)
        .then(response => response.json())
        .then(data => {
          if (data['message'] === 'right'){
            this.password = ''
            this.gotoSearch();
          } else {
            alert('密码不正确')
          }
        })
        .catch((e) => {
          alert(e)
        })
    },
    gotoSearch(){
      let path = '/search'
      this.$router.push({
        path
      })
    }
  },
  components: {
    AdminLoginModal
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