<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const questionnaire = ref(null)
const currentQuestionIndex = ref(0)
const userAnswers = ref([])
const quizCompleted = ref(false)
const score = ref(0)
const loading = ref(true)
const error = ref(null)

// Récupérer le questionnaire
const fetchQuestionnaire = async () => {
  const questionnaireId = route.params.id
  if (!questionnaireId) {
    error.value = "Identifiant de questionnaire manquant"
    loading.value = false
    return
  }
  
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/questionnaires/${questionnaireId}`)
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération du questionnaire')
    }
    
    questionnaire.value = await response.json()
    
    // Initialiser les réponses utilisateur
    if (questionnaire.value && questionnaire.value.questions) {
      userAnswers.value = questionnaire.value.questions.map(() => "")
    }
    
    loading.value = false
  } catch (err) {
    error.value = err.message
    loading.value = false
    console.error(err)
  }
}

// Question actuelle
const currentQuestion = computed(() => {
  if (!questionnaire.value || !questionnaire.value.questions) {
    return null
  }
  return questionnaire.value.questions[currentQuestionIndex.value]
})

// Vérifier si c'est la première question
const isFirstQuestion = computed(() => currentQuestionIndex.value === 0)

// Vérifier si c'est la dernière question
const isLastQuestion = computed(() => {
  if (!questionnaire.value || !questionnaire.value.questions) {
    return true
  }
  return currentQuestionIndex.value === questionnaire.value.questions.length - 1
})

// Naviguer à la question précédente
const goToPreviousQuestion = () => {
  if (!isFirstQuestion.value) {
    currentQuestionIndex.value--
  }
}

// Naviguer à la question suivante
const goToNextQuestion = () => {
  if (!isLastQuestion.value) {
    currentQuestionIndex.value++
  }
}

// Soumettre le questionnaire
const submitQuestionnaire = () => {
  if (!questionnaire.value || !questionnaire.value.questions) {
    return
  }
  
  // Calculer le score
  let totalScore = 0
  questionnaire.value.questions.forEach((question, index) => {
    const userAnswer = userAnswers.value[index]
    
    // Pour les QCM, comparer directement
    if (question.type === 'qcm') {
      if (userAnswer.toLowerCase() === question.answer.toLowerCase()) {
        totalScore++
      }
    } 
    // Pour les questions ouvertes, comparer sans tenir compte de la casse
    else {
      if (userAnswer.toLowerCase() === question.answer.toLowerCase()) {
        totalScore++
      }
    }
  })
  
  score.value = totalScore
  quizCompleted.value = true
}

// Recommencer le questionnaire
const restartQuiz = () => {
  currentQuestionIndex.value = 0
  userAnswers.value = questionnaire.value.questions.map(() => "")
  quizCompleted.value = false
  score.value = 0
}

// Retourner à la liste des questionnaires
const backToList = () => {
  router.push('/questionnaires')
}

onMounted(fetchQuestionnaire)
</script>

<template>
  <div class="quiz-container">
    <!-- Affichage du chargement -->
    <div v-if="loading" class="loading">
      <p>Chargement du questionnaire...</p>
    </div>
    
    <!-- Affichage des erreurs -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="backToList" class="btn back-btn">Retour à la liste</button>
    </div>
    
    <!-- Affichage du questionnaire -->
    <div v-else-if="questionnaire && !quizCompleted" class="questionnaire">
      <h2>{{ questionnaire.title }}</h2>
      
      <div class="progress-bar">
        <div class="progress" :style="{ width: `${(currentQuestionIndex + 1) / questionnaire.questions.length * 100}%` }"></div>
      </div>
      
      <div class="progress-text">
        Question {{ currentQuestionIndex + 1 }} / {{ questionnaire.questions.length }}
      </div>
      
      <div v-if="currentQuestion" class="question-card">
        <h3>{{ currentQuestion.text }}</h3>
        
        <!-- Question à choix multiples -->
        <div v-if="currentQuestion.type === 'qcm'" class="qcm-container">
          <div v-for="(choice, index) in currentQuestion.choices.split(',')" :key="index" class="choice-item">
            <input 
              type="radio" 
              :id="`choice-${index}`" 
              :name="`question-${currentQuestionIndex}`"
              :value="choice.trim()"
              v-model="userAnswers[currentQuestionIndex]"
            />
            <label :for="`choice-${index}`">{{ choice.trim() }}</label>
          </div>
        </div>
        
        <!-- Question ouverte -->
        <div v-else class="open-question">
          <input 
            type="text" 
            v-model="userAnswers[currentQuestionIndex]" 
            placeholder="Votre réponse..."
            class="open-answer"
          />
        </div>
      </div>
      
      <div class="navigation-buttons">
        <button 
          @click="goToPreviousQuestion" 
          :disabled="isFirstQuestion"
          class="btn nav-btn"
        >
          Précédent
        </button>
        
        <button 
          v-if="!isLastQuestion" 
          @click="goToNextQuestion" 
          class="btn nav-btn"
        >
          Suivant
        </button>
        
        <button 
          v-else 
          @click="submitQuestionnaire" 
          class="btn submit-btn"
        >
          Terminer
        </button>
      </div>
    </div>
    
    <!-- Affichage des résultats -->
    <div v-else-if="quizCompleted" class="results-container">
      <h2>Résultats</h2>
      
      <div class="score-card">
        <div class="score-header">
          <h3>Votre score</h3>
        </div>
        <div class="score-value">
          {{ score }} / {{ questionnaire.questions.length }}
        </div>
        <div class="score-percentage">
          {{ Math.round((score / questionnaire.questions.length) * 100) }}%
        </div>
      </div>
      
      <div class="questions-review">
        <h3>Détail des réponses</h3>
        
        <div v-for="(question, index) in questionnaire.questions" :key="index" class="review-item">
          <div class="review-question">
            <span class="question-number">{{ index + 1 }}.</span>
            {{ question.text }}
          </div>
          
          <div class="user-answer" :class="{ 
            'correct': userAnswers[index].toLowerCase() === question.answer.toLowerCase(),
            'incorrect': userAnswers[index].toLowerCase() !== question.answer.toLowerCase()
          }">
            <strong>Votre réponse:</strong> {{ userAnswers[index] || 'Non répondu' }}
            <span v-if="userAnswers[index].toLowerCase() === question.answer.toLowerCase()" class="correct-indicator">✓</span>
            <span v-else class="incorrect-indicator">✗</span>
          </div>
          
          <div v-if="userAnswers[index].toLowerCase() !== question.answer.toLowerCase()" class="correct-answer">
            <strong>Réponse correcte:</strong> {{ question.answer }}
          </div>
        </div>
      </div>
      
      <div class="result-actions">
        <button @click="restartQuiz" class="btn restart-btn">Recommencer</button>
        <button @click="backToList" class="btn back-btn">Retour aux questionnaires</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  color: #2c3e50;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.progress-bar {
  height: 10px;
  background-color: #eee;
  border-radius: 5px;
  margin-bottom: 10px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #4a6fa5;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: right;
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
}

.question-card {
  background-color: white;
  border: 1px solid #eee;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.qcm-container {
  margin-top: 15px;
}

.choice-item {
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  display: flex;
  align-items: center;
}

.choice-item:hover {
  background-color: #f5f5f5;
}

.choice-item input[type="radio"] {
  margin-right: 10px;
}

.open-question {
  margin-top: 15px;
}

.open-answer {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-btn {
  background-color: #4a6fa5;
  color: white;
}

.submit-btn {
  background-color: #4caf50;
  color: white;
}

.results-container {
  background-color: white;
  border: 1px solid #eee;
  border-radius: 5px;
  padding: 20px;
}

.score-card {
  text-align: center;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 5px;
  margin-bottom: 30px;
}

.score-header {
  margin-bottom: 10px;
}

.score-value {
  font-size: 3rem;
  font-weight: bold;
  color: #2c3e50;
}

.score-percentage {
  font-size: 1.5rem;
  color: #666;
}

.questions-review {
  margin-top: 30px;
}

.review-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
}

.review-question {
  font-weight: bold;
  margin-bottom: 10px;
}

.question-number {
  color: #4a6fa5;
  margin-right: 5px;
}

.user-answer {
  padding: 8px;
  border-radius: 4px;
  margin-bottom: 8px;
}

.correct {
  background-color: rgba(76, 175, 80, 0.1);
}

.incorrect {
  background-color: rgba(244, 67, 54, 0.1);
}

.correct-indicator {
  color: #4caf50;
  margin-left: 10px;
}

.incorrect-indicator {
  color: #f44336;
  margin-left: 10px;
}

.correct-answer {
  padding: 8px;
  background-color: rgba(76, 175, 80, 0.1);
  border-radius: 4px;
}

.result-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.restart-btn {
  background-color: #4a6fa5;
  color: white;
}

.back-btn {
  background-color: #666;
  color: white;
}

.loading, .error {
  text-align: center;
  padding: 50px 0;
  color: #666;
}

.error {
  color: #f44336;
}
</style>