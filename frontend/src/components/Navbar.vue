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
      <v-btn v-show="is_authenticated" text color="grey" href="/accounts/logout/">
        <span>로그아웃</span>
        <v-icon>exit_to_app</v-icon>
      </v-btn>
      <v-btn v-show="!is_authenticated" text color="grey" href="/accounts/login/">
        <span>로그인</span>
        <v-icon>exit_to_app</v-icon>
      </v-btn>
    </v-app-bar>
  </nav>
</template>
<script>
export default {
  name: "NavbarComponent",
  props: ['is_authenticated']
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
