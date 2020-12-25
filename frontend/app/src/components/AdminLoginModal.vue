<template>
  <modal name="adminlogin" :adaptive="true">
    <div class="admin-container">
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
div.admin-container{
  /*text-align: left;*/
  display: flex;
  align-items: center;
  justify-content: center;
  /*height: 100%;*/
  /*width: 100%;*/
}
div.input-container{
  margin: 10px;
  /*display: flex;*/
}


div.btn-container{
  padding-left: 10px;
  bottom: 0;
}
button.submit-btn{
  float: right;
}
</style>