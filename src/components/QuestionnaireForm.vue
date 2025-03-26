<script setup>
import { ref, watchEffect, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const questionnaire = ref({ title: '', questions: [] })
const isEdit = ref(false)

const fetchQuestionnaire = async () => {
  if (route.params.id) {
    isEdit.value = true
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/questionnaires/${route.params.id}`)
      if (!response.ok) {
        throw new Error('Erreur lors de la récupération du questionnaire')
      }
      questionnaire.value = await response.json()
    } catch (error) {
      console.error(error)
    }
  }
}

const submitForm = async () => {
  try {
    const response = isEdit.value
      ? await fetch(`http://127.0.0.1:5000/api/questionnaires/${route.params.id}`, {
          method: 'PUT',
          body: JSON.stringify(questionnaire.value),
          headers: {
            'Content-Type': 'application/json',
          },
        })
      : await fetch('http://127.0.0.1:5000/api/questionnaires', {
          method: 'POST',
          body: JSON.stringify(questionnaire.value),
          headers: {
            'Content-Type': 'application/json',
          },
        })

    if (response.ok) {
      router.push('/questionnaires')
    } else {
      console.error('Erreur lors de l\'enregistrement du questionnaire')
    }
  } catch (error) {
    console.error(error)
  }
}

const addQuestion = () => {
  questionnaire.value.questions.push({ text: '' })
}

const removeQuestion = (index) => {
  questionnaire.value.questions.splice(index, 1)
}

onMounted(fetchQuestionnaire)
</script>

<template>
  <div>
    <h2>{{ isEdit ? 'Modifier le questionnaire' : 'Créer un questionnaire' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="title">Titre</label>
        <input type="text" id="title" v-model="questionnaire.title" required />
      </div>

      <div v-for="(question, index) in questionnaire.questions" :key="index">
        <label :for="'question' + index">Question {{ index + 1 }}</label>
        <input
          v-model="question.text"
          :id="'question' + index"
          type="text"
          :placeholder="'Entrez la question ' + (index + 1)"
          required
        />
        <button type="button" @click="removeQuestion(index)">Supprimer la question</button>
      </div>

      <button type="button" @click="addQuestion">Ajouter une question</button>
      <button type="submit">{{ isEdit ? 'Mettre à jour' : 'Créer' }}</button>
    </form>
  </div>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
input,
button {
  padding: 8px;
  margin-bottom: 10px;
}
button {
  background-color: green;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
