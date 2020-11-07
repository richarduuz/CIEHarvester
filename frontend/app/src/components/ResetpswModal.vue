<template>
  <modal name="resetpsw" :height="'200px'" :adaptive="true">
    <div class="container">
      <div class="input-container">
        <h2>请重新设置密码</h2>
        <span>请输入密码: </span>
        <input type="password" v-model="password">
        <br>
        <br>
        <span>请确认新的密码: </span>
        <input type="password" v-model.lazy="password_">
      </div>
      <div class="btn-container">
        <p class="login-alert" v-show="password !== password_">请输入一样的密码</p>
        <button class="submit-btn" @click="submit">确认</button>
      </div>
    </div>
  </modal>
</template>

<script>
export default {
  name: "ResetpswModal",
  data() {
    return {
      password: "",
      password_: "",
      height: 'auto'
    }
  },
  methods: {
    submit(){
      if (this.password_ === this.password){
        if (confirm("确认要修改密码吗？")) {
          let url = this.$store.state.url + '/password';
          let postData = {'newPassword': this.password}
          postData = JSON.stringify(postData)
          this.$http.post(url, postData)
            .then(response => response.json())
            .then(data => {
              if (data){
                if (data['status'] === 'Okay'){
                  this.password_ = ''
                  this.password = ''
                  alert('修改成功')
                  this.$emit('resetpsw')
                } else {
                  alert('修改错误')
                }
              }
            })
            .catch(e => alert(str(e)))
        }
      } else {
        alert('两次密码不一样！')
      }
    },
    gotoHome(){
      let path = '/home'
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

p.login-alert{
  font-size: 15px;
  color: red;
  float: left;
  margin: 0;
}

div.btn-container{
  margin: 10px;
  bottom: 0;
}

button.submit-btn{
  float: right;
}
</style>