<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const questionnaires = ref([])
const router = useRouter()

const fetchQuestionnaires = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/questionnaires')
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération des questionnaires')
    }
    questionnaires.value = await response.json()
    } catch (error) {
      console.error(error)
  }
}

const deleteQuestionnaire = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/questionnaires/${id}`, {method: 'DELETE'})
        if (response.ok) {
            fetchQuestionnaires()
        } else {
            console.error('Erreur lors de la suppression')
        }
    } catch (error) {
        console.error(error)
    }
}

onMounted(fetchQuestionnaires)


// const viewDetails = (id) => {
//     router.push({name : 'questionnaire-details', params: { id }})
// }

</script>

<template>
    <div>
        <h2>Liste des Questionnaires</h2>
        <ul>
            <li v-for="quiz in questionnaires" :key="quiz.id">
                <router-link :to="`/questionnaire/${quiz.id}`">{{ quiz.title }}</router-link>
                <button @click="deleteQuestionnaire(quiz.id)">Supprimer</button>
            </li>
        </ul>
    </div>
</template>

<style scoped>
ul {
    list-style-type: none;
    padding: 0;
}
li {
    padding: 8px;
    border-bottom: 1px solid #ddd;
}
button {
    background: none;
    border: none;
    color: blue;
    cursor: pointer;
    text-decoration: underline;
}
</style>