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
      <v-btn text color="grey" href="/accounts/logout/">
        <span>로그아웃</span>
        <v-icon>exit_to_app</v-icon>
      </v-btn>
    </v-app-bar>

    <li class="nav-item mx-1">
      <router-link :to="{ name: 'question-editor' }" class="btn btn-sm btn-warning">
        요청하기
      </router-link>
    </li>
  </nav>
</template>
<script>
export default {
  name: "NavbarComponent"
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
