<template>
  <modal name="resetpsw" :adaptive="true">
    <!-- <div class="RPM-container">
      <div style="display: flex">
        <div class="RPM-input-container">
          <h2>请重新设置密码</h2>
          <span>请输入密码: </span>
          <input type="password" v-model="password">
          <br>
          <br>
          <span>请确认新的密码: </span>
          <input type="password" v-model.lazy="password_">
        </div>
        <div class="RPM-btn-container">
          <div style="position: absolute; bottom: 0; ">
            <button class="submit-btn" @click="submit" style="float: left">确认</button>
            <p class="login-alert" v-show="password !== password_">请输入一样的密码</p>
          </div>
        </div>
      </div>
    </div> -->
    <section class="reset-container">
      <h2>请重置密码</h2>
      <label for="">请输入密码:
        <input type="password" v-model="password" autofocus>
      </label>
      <br>
      <label for="">请确认密码:
        <input type="password" v-model="password_">
      </label>
      <button @click="submit" :disabled="password !== password_">确认</button>
      <p v-show="password !== password_">请输入一样的密码</p>
    </section>
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
.reset-container {
  position: absolute;
  top: 60px;
  left: 165px;
  text-align: center;
}

.reset-container input {
  outline: none;
}

.reset-container button {
  display: block;
  margin: 14px auto;
  border: none;
  border-radius: 6px;
  padding: 4px;
  outline: none;
  font-size: 14px;
  font-weight: 400;
  transition: box-shadow .5s;
}

.reset-container button:hover {
  box-shadow: 2px 2px 1px 1px rgba(0,0,0,.2);
}

.reset-container p {
  color: red;
  font-size:14px;
  font-weight: 700;
}

/* div.RPMcontainer{
  position: absolute;
  text-align: left;
  height: 300px;
  width: 100%;
  align-items: center;
  justify-content: center;
  display: flex;
}

div.RPM-input-container{
  margin: 10px;
}

p.login-alert{
  font-size: 15px;
  color: red;
  float: left;
  margin: 0;
}

div.RPM-btn-container{
  margin-bottom: 10px;
  width: 200px;
  position: relative;
}

button.submit-btn{
  float: right;
} */
</style>