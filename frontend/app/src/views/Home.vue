<template>
  <div class="home">
    欢迎来到CIE询价系统
    <button @click="showLogin">开始使用</button>
    <LoginModal @showAdminLogin="showAdminLogin"></LoginModal>
    <admin-login-modal @showResetpswModal="showResetpsw"></admin-login-modal >
    <ResetpswModal @resetpsw="hideResetpsw"></ResetpswModal>
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
