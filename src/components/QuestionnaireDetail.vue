<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const questionnaire = ref(null)
const showAnswers = ref(false)

const fetchQuestionnaire = async () => {
    const questionnaireId = route.params.id
    if (!questionnaireId) {
        return
    }
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/questionnaires/${questionnaireId}`)
        if (!response.ok) {
        throw new Error('Erreur lors de la récupération du questionnaire')
        }
        questionnaire.value = await response.json()
    } catch (error) {
        console.error(error)
    }
}

const toggleAnswers = () => {
    showAnswers.value = !showAnswers.value
}

onMounted(fetchQuestionnaire)
</script>

<template>
    <div v-if="questionnaire" class="questionnaire-details">
        <h2>{{ questionnaire.title }}</h2>
        
        <div class="toggle-container">
            <button @click="toggleAnswers" class="toggle-button">
                {{ showAnswers ? 'Masquer les réponses' : 'Afficher les réponses' }}
            </button>
        </div>
        
        <div v-if="questionnaire.questions.length > 0" class="questions-list">
            <h3>Questions</h3>
            <div v-for="question in questionnaire.questions" :key="question.id" class="question-item">
                <div class="question-text">{{ question.text }}</div>
                <div class="question-type">Type: {{ question.type === 'qcm' ? 'QCM' : 'Question ouverte' }}</div>
                
                <div v-if="question.type === 'qcm' && question.choices" class="choices-list">
                    <h4>Options:</h4>
                    <ul>
                        <li v-for="(choice, index) in question.choices.split(',')" :key="index"
                            :class="{ 'correct-answer': showAnswers && choice.trim().toLowerCase() === question.answer?.toLowerCase() }">
                            {{ choice.trim() }}
                            <span v-if="showAnswers && choice.trim().toLowerCase() === question.answer?.toLowerCase()" class="correct-badge">
                                ✓ Bonne réponse
                            </span>
                        </li>
                    </ul>
                </div>
                
                <div v-if="showAnswers" class="answer-section">
                    <div v-if="question.type === 'ouverte'" class="correct-answer-text">
                        <strong>Réponse attendue:</strong> {{ question.answer }}
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="no-questions">
            Ce questionnaire ne contient pas encore de questions.
        </div>
        
        <div class="actions">
            <router-link :to="`/edit/${questionnaire.id}`" class="edit-link">Modifier le questionnaire</router-link>
            <router-link to="/questionnaires" class="back-link">Retour à la liste</router-link>
        </div>
    </div>
    <p v-else class="loading">Chargement...</p>
</template>

<style scoped>
.questionnaire-details {
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

h3 {
    margin: 20px 0 15px;
    color: #2c3e50;
}

.questions-list {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 15px;
    background-color: #f9f9f9;
}

.question-item {
    background-color: white;
    border: 1px solid #eee;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 15px;
}

.question-text {
    font-size: 18px;
    margin-bottom: 10px;
    color: #333;
}

.question-type {
    font-size: 14px;
    color: #666;
    margin-bottom: 10px;
}

.choices-list {
    margin-top: 10px;
}

.choices-list h4 {
    margin-bottom: 5px;
    font-size: 14px;
    color: #555;
}

.choices-list ul {
    list-style-type: disc;
    padding-left: 20px;
}

.choices-list li {
    margin-bottom: 8px;
    padding: 3px;
    border-radius: 3px;
}

.correct-answer {
    background-color: rgba(76, 175, 80, 0.1);
    font-weight: bold;
}

.correct-badge {
    background-color: #4CAF50;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 12px;
    margin-left: 8px;
}

.answer-section {
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px dashed #ddd;
}

.correct-answer-text {
    padding: 8px;
    background-color: rgba(76, 175, 80, 0.1);
    border-radius: 4px;
}

.no-questions {
    text-align: center;
    padding: 20px;
    color: #666;
    font-style: italic;
}

.actions {
    margin-top: 30px;
    display: flex;
    gap: 15px;
}

.edit-link, .back-link {
    display: inline-block;
    padding: 8px 16px;
    background-color: #4a6fa5;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-weight: bold;
}

.back-link {
    background-color: #666;
}

.loading {
    text-align: center;
    font-style: italic;
    color: #666;
    padding: 40px;
}

.toggle-container {
    margin: 20px 0;
    text-align: right;
}

.toggle-button {
    background-color: #2c3e50;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
}

.toggle-button:hover {
    background-color: #1a2530;
}
</style>