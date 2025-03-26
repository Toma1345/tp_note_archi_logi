<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const questionnaire = ref(null)

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

watch(() => route.params.id, fetchQuestionnaire, { immediate: true })

onMounted(fetchQuestionnaire)
</script>

<template>
    <div v-if="questionnaire">
        <h2>{{ questionnaire.title }}</h2>
        <ul>
            <li v-for="question in questionnaire.questions" :key="question.id">
                {{ question.text }}
            </li>
        </ul>
    </div>
    <p v-else>Sélectionnez un questionnaire</p>
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
</style>