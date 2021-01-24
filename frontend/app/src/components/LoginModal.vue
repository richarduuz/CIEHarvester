<template>
    <!-- <div class="login-container">
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
    </div> -->
    <div class="login-container">
      <section class="login center">
        <h2>请入密码进入系统</h2>
          <label for="">请输入密码：
            <input v-model="password" type="password" autofocus>
            <button @click="authID" :disabled="password.length === 0">确认</button>
          </label>
      </section>
      <div class="center">
        <h4>重置密码</h4>
        <button @click="showAdminLogin">管理员登录</button>
        <admin-login-modal @showResetpswModal="showResetpswModal"></admin-login-modal>
        <resetpsw-modal @resetpsw="showLoginModal" ></resetpsw-modal>
      </div>
    </div>
</template>

<script>
import AdminLoginModal from "@/components/AdminLoginModal";
import ResetpswModal from "@/components/ResetpswModal";


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
      console.log(this.password);
      console.log(this.adminPassword.length);
    },
    showAdminLogin(){
      // this.$emit('showAdminLogin')
      this.$modal.show('adminlogin')
    },
    showResetpswModal(){
      this.$modal.hide("adminlogin")
      this.$modal.show('resetpsw')
    },

    showLoginModal() {
      this.$modal.hide("adminlogin")
      this.$modal.hide("resetpsw")
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
    AdminLoginModal,
    ResetpswModal
  }
}
</script>

<style scoped>

button {
  border: none;
  border-radius: 6px;
  padding: 4px;
  outline: none;
  font-size: 14px;
  font-weight: 400;
  transition: box-shadow .5s;
}

button:hover {
    box-shadow: 2px 2px 1px 1px rgba(0,0,0,.2);
}

div {
  display: block;
  box-sizing: border-box;
}

.center {
  margin: 0 auto;
  text-align: center;
}

.login-container {
  width: 400px;
  padding: 14px;
  background-color: #fff;
  box-shadow: 4px 4px 2px 2px rgba(0, 0, 0, 0.3);
  transition: box-shadow .5s;
}

.login-container:hover {
    box-shadow: 8px 8px 4px 4px rgba(0, 0, 0, 0.4);

}

.login-container .login {
  margin: 0 auto;
  text-align: center;
}

.login-container .login input {
  margin-right: 14px;
  outline: none;
}


/* div.login-container{
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
} */

</style>