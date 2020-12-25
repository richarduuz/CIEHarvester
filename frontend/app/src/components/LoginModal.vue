<template>
<!--  <modal name="login" :adaptive="true">-->
    <div class="login-container">
      <div class="input-container">
        <h2>输入密码进入系统</h2>
        <div style="float: left;">
          <span>请输入密码: </span>
          <input v-model="password" type="password">
          <br>
        </div>
        <div class="btn-container">
          <button class="submit-btn" @click="authID" :disabled="password.length === 0">确认</button>
        </div>
        <br>
      </div>
      <div style="margin: 10px;">
        <h5>重置密码</h5>
        <button @click="showAdminLogin">管理员登录</button>
        <admin-login-modal></admin-login-modal>
      </div>
    </div>
<!--  </modal>-->
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
div.login-container{
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  background: white;
}

div.input-container{
  margin: 10px;
}

div.btn-container{
  bottom: 0;
  padding-left: 10px;
  display: flex;
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