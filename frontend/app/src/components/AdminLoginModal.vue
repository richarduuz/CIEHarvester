<template>
  <modal name="adminlogin" :adaptive="true">
    <!-- <div class="admin-container">
      <div class="input-container">
        <h2>重置密码</h2>
        <div style="display: flex;">
          <div style="float: left">
            <span>请输入管理员密码: </span>
            <input v-model="adminPassword" type="password">
          </div>
          <div class="btn-container">
            <button class="submit-btn" @click="adminAuth">登录</button>
          </div>
        </div>
      </div>
    </div> -->
    <section class="admin-container">
      <h2>重置密码</h2>
      <label for="">请输入管理员登录密码：
        <input v-model="adminPassword" type="password" autofocus>
        <button @click="adminAuth" :disabled="adminPassword.length === 0">登录</button>
      </label>
    </section>
  </modal>
</template>

<script>

export default {
  name: "AdminLoginModal",
  methods: {
    adminAuth(){
      console.log("here")
      let url = this.$store.state.url + '/admin'
      let postData = {}
      postData['adminPassword'] = this.adminPassword;
      postData = JSON.stringify(postData);
      this.$http.post(url, postData)
        .then(response => response.json())
        .then(data => {
          if (data['message'] === 'right'){
            this.$emit('showResetpswModal')
          } else {
            alert('密码不正确')
          }
        })
      .catch(e => {
        alert(e)
      })
    }
  },
  data(){
    return {
      adminPassword: ''
    }
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

.admin-container {
  position: absolute;
  top: 75px;
  left: 100px;
  text-align: center;
}

.admin-container input {
  margin-right: 14px;
  outline: none;
}




/* div.admin-container{
  display: flex;
  align-items: center;
  justify-content: center;
}
div.input-container{
  margin: 10px;
}


div.btn-container{
  padding-left: 10px;
  bottom: 0;
}
button.submit-btn{
  float: right;
} */
</style>