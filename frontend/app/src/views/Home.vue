<template>
  <div class="home">
    欢迎来到CIE询价系统
    <button @click="showLogin">开始使用</button>
    <LoginModal></LoginModal>
  </div>
</template>

<script>
// @ is an alias to /src
import LoginModal from "@/components/LoginModal";

export default {

  name: 'Home',
  data(){
    return {
      showLoginModal: false
    }
  },
  methods:{
    showLogin(){
      this.$modal.show('login')
    }
  },
  components: {
    LoginModal
  }
}
</script>
