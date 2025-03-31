<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const questionnaire = ref({ title: '', questions: [] })
const isEdit = ref(false)
const questionnaireId = ref(null)

const fetchQuestionnaire = async () => {
  if (route.params.id) {
    isEdit.value = true
    questionnaireId.value = route.params.id
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
    const questData = { title: questionnaire.value.title }
    
    let questionnaireResponse
    
    if (isEdit.value) {
      questionnaireResponse = await fetch(`http://127.0.0.1:5000/api/questionnaires/${questionnaireId.value}`, {
        method: 'PUT',
        body: JSON.stringify(questData),
        headers: {
          'Content-Type': 'application/json',
        },
      })
    } else {
      questionnaireResponse = await fetch('http://127.0.0.1:5000/api/questionnaires', {
        method: 'POST',
        body: JSON.stringify(questData),
        headers: {
          'Content-Type': 'application/json',
        },
      })
    }

    if (!questionnaireResponse.ok) {
      throw new Error('Erreur lors de l\'enregistrement du questionnaire')
    }

    const savedQuestionnaire = await questionnaireResponse.json()
    const newQuestionnaireId = savedQuestionnaire.id || questionnaireId.value

    let existingQuestions = []
    if (isEdit.value) {
      const questionsResponse = await fetch(`http://127.0.0.1:5000/api/questions`)
      if (questionsResponse.ok) {
        const allQuestions = await questionsResponse.json()
        existingQuestions = allQuestions.filter(q => q.questionnaire_id === parseInt(newQuestionnaireId))
      }
    }

    for (const question of questionnaire.value.questions) {
      const isExistingQuestion = question.id !== undefined
      
      const questionData = {
        text: question.text,
        type: question.type,
        choices: question.choices,
        answer: question.answer,
        questionnaire_id: newQuestionnaireId
      }

      if (isExistingQuestion) {
        await fetch(`http://127.0.0.1:5000/api/questions/${question.id}`, {
          method: 'PUT',
          body: JSON.stringify(questionData),
          headers: {
            'Content-Type': 'application/json',
          },
        })
        
        existingQuestions = existingQuestions.filter(q => q.id !== question.id)
      } else {
        // Créer une nouvelle question
        await fetch('http://127.0.0.1:5000/api/questions', {
          method: 'POST',
          body: JSON.stringify(questionData),
          headers: {
            'Content-Type': 'application/json',
          },
        })
      }
    }

    if (isEdit.value) {
      for (const questionToDelete of existingQuestions) {
        await fetch(`http://127.0.0.1:5000/api/questions/${questionToDelete.id}`, {
          method: 'DELETE'
        })
      }
    }

    router.push('/questionnaires')
  } catch (error) {
    console.error(error)
  }
}

const addQuestion = () => {
  questionnaire.value.questions.push({ 
    text: '',
    type: 'ouverte',
    choices: '',
    answer: ''
  })
}

const removeQuestion = (index) => {
  questionnaire.value.questions.splice(index, 1)
}

const isAnswerValid = (question) => {
  if (question.type !== 'qcm' || !question.answer || !question.choices) {
    return true
  }
  
  const choices = question.choices.split(',').map(choice => choice.trim().toLowerCase())
  return choices.includes(question.answer.toLowerCase())
}

onMounted(fetchQuestionnaire)
</script>

<template>
  <div>
    <h2>{{ isEdit ? 'Modifier le questionnaire' : 'Créer un questionnaire' }}</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="title">Titre</label>
        <input type="text" id="title" v-model="questionnaire.title" required />
      </div>

      <div v-if="questionnaire.questions.length > 0" class="questions-container">
        <h3>Questions</h3>
        <div v-for="(question, index) in questionnaire.questions" :key="index" class="question-item">
          <div class="form-group">
            <label :for="'question' + index">Question {{ index + 1 }}</label>
            <input
              v-model="question.text"
              :id="'question' + index"
              type="text"
              :placeholder="'Entrez la question ' + (index + 1)"
              required
            />
          </div>
          
          <div class="form-group">
            <label :for="'type' + index">Type de question</label>
            <select v-model="question.type" :id="'type' + index" required>
              <option value="ouverte">Question ouverte</option>
              <option value="qcm">QCM</option>
            </select>
          </div>
          
          <div class="form-group" v-if="question.type === 'qcm'">
            <label :for="'choices' + index">Options (séparées par des virgules)</label>
            <input
              v-model="question.choices"
              :id="'choices' + index"
              type="text"
              placeholder="Option 1, Option 2, Option 3"
              required
            />
          </div>
          
          <div class="form-group">
            <label :for="'answer' + index">Bonne réponse</label>
            <div v-if="question.type === 'qcm' && question.choices">
              <select v-model="question.answer" :id="'answer' + index" required>
                <option value="" disabled>Sélectionnez la bonne réponse</option>
                <option v-for="(choice, choiceIndex) in question.choices.split(',')" 
                        :key="choiceIndex" 
                        :value="choice.trim()">
                  {{ choice.trim() }}
                </option>
              </select>
            </div>
            <div v-else>
              <input
                v-model="question.answer"
                :id="'answer' + index"
                type="text"
                :placeholder="question.type === 'ouverte' ? 'Entrez la réponse attendue' : 'Ajoutez d\'abord des options'"
                required
              />
            </div>
            <div v-if="question.type === 'qcm' && question.answer && !isAnswerValid(question)" class="error-message">
              La réponse doit être l'une des options proposées
            </div>
          </div>
          
          <button type="button" class="remove-btn" @click="removeQuestion(index)">Supprimer la question</button>
        </div>
      </div>
      
      <div class="buttons-container">
        <button type="button" class="add-btn" @click="addQuestion">Ajouter une question</button>
        <button type="submit" class="submit-btn">{{ isEdit ? 'Mettre à jour' : 'Créer' }}</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input, select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.question-item {
  border: 1px solid #eee;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
}

.buttons-container {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.add-btn {
  background-color: #4a6fa5;
  color: white;
}

.submit-btn {
  background-color: #4caf50;
  color: white;
}

.remove-btn {
  background-color: #f44336;
  color: white;
  margin-top: 10px;
}

h3 {
  margin-bottom: 15px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}

.questions-container {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 20px;
  background-color: #fff;
}

.error-message {
  color: #f44336;
  font-size: 14px;
  margin-top: 5px;
}
</style>