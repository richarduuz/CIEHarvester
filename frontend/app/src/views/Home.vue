<template>
  <div class="home">
    <div class="container">
      <LoginModal @showAdminLogin="showAdminLogin"></LoginModal>
      <!-- <admin-login-modal @showResetpswModal="showResetpsw"></admin-login-modal > -->
      <ResetpswModal @resetpsw="hideResetpsw"></ResetpswModal>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import LoginModal from "@/components/LoginModal";
import AdminLoginModal from "@/components/AdminLoginModal";
import ResetpswModal from "@/components/ResetpswModal";

export default {

  name: 'Home',
  data(){
    return {
    }
  },
  methods:{
    showLogin(){
      this.$modal.show('login')
    },
    showResetpsw(){
      this.$modal.hide('login')
      this.$modal.hide('adminlogin')
      this.$modal.show('resetpsw')
    },
    hideResetpsw(){
      this.$modal.hide('resetpsw')
    },
    showAdminLogin(){
      this.$modal.hide('login')
      this.$modal.show('adminlogin')
    }
  },
  components: {
    LoginModal,
    AdminLoginModal,
    ResetpswModal
  }
}
</script>
<style>
.home{
  display: flex;
  width: 100%;
  height: 100%;
  background-image: url("../assets/background3.jpg");
  background-size: cover;
  position: absolute;
  align-items: center;
  justify-content: center;
}

.container{
  display: flex;
  background: #f9f9f9;
  margin: auto;
}
.background{
  width: 65%;
  height: 100%;
  float: left;
  background-image: url("../assets/background3.jpg");
  background-size: cover;
}
.login-window{
  display: flex;
  /*margin-left: 25%;*/
  height: 100%;
  background: seashell;
  align-items: center;
  justify-content: center;
}

</style>