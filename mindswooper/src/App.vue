<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <h1>MindSwooper</h1>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-card class="mx-auto" max-width="400">
        <minesweepergame></minesweepergame>
        
      </v-card>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import minesweepergame from './components/MinesweeperGame.vue';

export default Vue.extend({
  name: 'App',

  components: {
    minesweepergame,
  },

  data: () => ({
    //
  }),
});
</script>
