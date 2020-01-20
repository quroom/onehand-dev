<template>
  <nav>
    <v-app-bar text>
      <router-link :to="{ name: 'home' }">
        <v-toolbar-title class="text-uppercase grey--text">
          OnePaper
        </v-toolbar-title>
      </router-link>
      <router-link :to="{ name: 'home' }">
        <v-icon>home</v-icon>
      </router-link>
      <v-spacer></v-spacer>
      <v-btn v-show="getCookie('islogin')" text color="grey" href="/accounts/logout/" v-on:click="removeCookie">
        <span>로그아웃</span>
        <v-icon>exit_to_app</v-icon>
      </v-btn>
      <v-btn v-show="!getCookie('islogin')" text color="grey" href="/accounts/login/">
        <span>로그인</span>
        <v-icon>exit_to_app</v-icon>
      </v-btn>
    </v-app-bar>
  </nav>
</template>
<script>
import { getCookie } from "@/common/get_cookie.js";

export default {
  name: "NavbarComponent",
  methods: {
    removeCookie: function () {
      // document.cookie = 'csrftoken= ; expires = Thu, 01 Jan 1970 00:00:00 GMT'
    },
    getCookie: getCookie
  }
};
</script>

<style>
.my-navbar {
  border-bottom: 1px solid #ddd;
}
.navbar-brand {
  font-weight: bold;
  font-size: 130%;
}
.navbar-brand:hover {
  color: green !important;
}
a {
  text-decoration: none;
}
</style>
