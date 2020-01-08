<template>
  <v-app>
    <NavbarComponent :is_authenticated="is_authenticated" />
    <router-view :is_authenticated="is_authenticated" />
  </v-app>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import NavbarComponent from "./components/Navbar.vue";

export default {
  name: "App",
  components: {
    NavbarComponent
  },
  data() {
    return {
      is_authenticated:false
    }
  },
  methods: {
    async setUserInfo() {
      const data = await apiService("/api/user/");
      const requestUser = data["username"];
      const is_authenticated = data["is_authenticated"];
      window.localStorage.setItem("username", requestUser);
      this.is_authenticated=is_authenticated
      console.log(data);
      console.log(requestUser);
      console.log(is_authenticated);
    }
  },
  created() {
    this.setUserInfo();
  }
};
</script>
<style>
html,
body {
  height: 100%;
  font-family: "Nanum Gothic", sans-serif;
}

.btn:focus {
  box-shadow: none !important;
}
</style>
