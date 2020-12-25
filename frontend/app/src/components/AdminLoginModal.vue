<template>
  <modal name="adminlogin" :adaptive="true">
    <div class="container">
      <div class="input-container">
        <h2>重置密码</h2>
        <span>请输入管理员密码: </span>
        <input v-model="adminPassword" type="password">
        <div class="btn-container">
          <button class="submit-btn" @click="adminAuth">登录</button>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
export default {
  name: "AdminLoginModal",
  methods: {
    adminAuth(){
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