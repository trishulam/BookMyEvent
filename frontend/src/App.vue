<template>
  <div id="app" class="bg">
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #F8F6F4;
  overflow-y: auto;
  height: 100vh;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
.bg{
background-color: #323232;
opacity: 1;
background-image:  repeating-radial-gradient( circle at 0 0, transparent 0, #323232 31px ), repeating-linear-gradient( #00000055, #000000 );
}

</style>
