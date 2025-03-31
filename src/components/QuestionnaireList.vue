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

</script>

<template>
    <div>
        <h2>Liste des Questionnaires</h2>
        <ul>
            <li v-for="quiz in questionnaires" :key="quiz.id">
                <div class="quiz-actions">
                    <router-link :to="`/questionnaire/${quiz.id}`" class="action-link">{{ quiz.title }}</router-link>
                    <div class="buttons-group">
                        <button @click="deleteQuestionnaire(quiz.id)" class="action-link">Supprimer</button>
                        <router-link :to="`/questionnaire/${quiz.id}/repondre`" class="action-link repondre-btn">Répondre</router-link>
                    </div>
                </div>
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

.quiz-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.buttons-group {
    display: flex;
    gap: 15px;
}

.action-link {
    text-decoration: none;
    color: rgb(0, 120, 189);;
    cursor: pointer;
}

button.action-link {
    background: none;
    border: none;
    font: inherit;
    cursor: pointer;
    text-decoration: none;
    color: rgb(0, 120, 189);
    transition: 0.4s;
    padding: 3px;
}

button:hover {
    background-color: hsla(246, 100%, 37%, 0.2);
  }

.repondre-btn {
    color: rgb(0, 120, 189);;
}
</style>