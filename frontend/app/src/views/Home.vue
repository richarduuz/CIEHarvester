<template>
  <div class="home">
    欢迎来到CIE询价系统
    <button @click="showLogin">开始使用</button>
    <LoginModal @showResetpswModal="showResetpsw"></LoginModal>
    <ResetpswModal @resetpsw="hideResetpsw"></ResetpswModal>
  </div>
</template>

<script>
// @ is an alias to /src
import LoginModal from "@/components/LoginModal";
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
      this.$modal.show('resetpsw')
    },
    hideResetpsw(){
      this.$modal.hide('resetpsw')
    }
  },
  components: {
    LoginModal,
    ResetpswModal
  }
}
</script>
