<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <HelloWorld msg="Application de Gestion de Questionnaires" />
    </div>
  </header>

  <main>
    <router-link to="/questionnaires">Voir les questionnaires</router-link>
    <router-link to="/create">Créer un questionnaire</router-link>
    <router-view />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
