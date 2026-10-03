<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const showWhy = ref(true)
const isLoading = ref(true)
const apiError = ref(false)

const selectedGoal = ref({
  id: 2,
  name: 'MacBook Air 15"',
  price: 5999
})

const analysis = ref({
  goal: 'MacBook Air 15"',
  price: 5999,
  recommended_purchase: 'November',
  recommended_year: 2026,
  months_needed: 1,
  monthly_allocation: 0,

  goal_progress_amount: 0,
  progress_percentage: 0,
  goal_status: 'On Track',

  available_for_planning: 0,
  safe_to_spend: 0,

  explanation:
    'JEEBIK is analyzing your financial context.',

  ai_agent: {
    status: 'loading',
    agent: 'JEEBIK AI Agent',
    model: '',
    stage: 'initial_planning',
    action: 'financial_context_analyzed',
    message: ''
  },

  financial_context: {
    balance: 10000,
    monthly_income: 15000,
    average_monthly_spending: 4000,
    monthly_commitments: 3000,
    other_goal_name: 'Mauritius Trip',
    other_goal_amount: 8000,
    other_goal_target: 'July 2027',
    required_other_goal_monthly: 0
  }
})

const commitments = [
  {
    name: 'Car Insurance',
    amount: 'SAR 900'
  },
  {
    name: 'School Fees',
    amount: 'SAR 1,500'
  },
  {
    name: 'Electricity',
    amount: 'SAR 350'
  },
  {
    name: 'Subscriptions',
    amount: 'SAR 250'
  }
]

// --------------------------------------------------
// AI DISPLAY
// --------------------------------------------------

const aiIsActive = computed(() => {
  return analysis.value?.ai_agent?.status === 'active'
})

const aiMessage = computed(() => {
  return (
    analysis.value?.ai_agent?.message ||
    analysis.value?.explanation ||
    'JEEBIK analyzed your financial context.'
  )
})

const aiModelLabel = computed(() => {
  const model = analysis.value?.ai_agent?.model || ''

  if (model.toLowerCase().includes('gemini')) {
    return 'GEMINI ACTIVE'
  }

  if (analysis.value?.ai_agent?.status === 'fallback') {
    return 'SAFE FALLBACK'
  }

  return 'JEEBIK AI'
})

// --------------------------------------------------
// LOAD SELECTED GOAL
// --------------------------------------------------

function loadSelectedGoal() {
  const savedGoal =
    sessionStorage.getItem('jeebikSelectedGoal')

  if (savedGoal) {
    try {
      selectedGoal.value =
        JSON.parse(savedGoal)

      analysis.value.goal =
        selectedGoal.value.name

      analysis.value.price =
        selectedGoal.value.price

    } catch (error) {
      console.error(
        'Could not read selected goal:',
        error
      )
    }
  }
}

// --------------------------------------------------
// GET ANALYSIS FROM BACKEND
// --------------------------------------------------

async function getAnalysis() {
  isLoading.value = true
  apiError.value = false

  try {
    const response = await fetch(
      'https://jeebik-backend.onrender.com/analyze-plan',
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          goal_name:
            selectedGoal.value.name,

          goal_price:
            selectedGoal.value.price,

          balance:
            10000,

          monthly_income:
            15000,

          monthly_spending:
            4000,

          monthly_commitments:
            3000,

          other_goal_name:
            'Mauritius Trip',

          other_goal_amount:
            8000,

          other_goal_target_year:
            2027,

          other_goal_target_month:
            7
        })
      }
    )

    if (!response.ok) {
      throw new Error(
        `Backend request failed: ${response.status}`
      )
    }

    const data =
      await response.json()

    analysis.value = data

    console.log(
      'Selected Goal:',
      selectedGoal.value
    )

    console.log(
      'JEEBIK Financial Analysis:',
      data
    )

    console.log(
      'JEEBIK AI Agent:',
      data.ai_agent
    )

  } catch (error) {
    console.error(
      'JEEBIK API error:',
      error
    )

    apiError.value = true

    analysis.value = {
      ...analysis.value,
      goal: selectedGoal.value.name,
      price: selectedGoal.value.price
    }

  } finally {
    isLoading.value = false
  }
}

// --------------------------------------------------
// LIFECYCLE
// --------------------------------------------------

onMounted(async () => {
  loadSelectedGoal()
  await getAnalysis()
})

// --------------------------------------------------
// HELPERS
// --------------------------------------------------

function formatSAR(value) {
  return `SAR ${Number(
    value || 0
  ).toLocaleString()}`
}

function goBack() {
  router.push('/goals')
}

function toggleWhy() {
  showWhy.value =
    !showWhy.value
}

// --------------------------------------------------
// CREATE GOAL
// --------------------------------------------------

function createGoal() {

  // Start a fresh goal monitoring cycle.

  sessionStorage.removeItem(
    'jeebikReplanAccepted'
  )

  sessionStorage.removeItem(
    'jeebikPriceChange'
  )

  const createdPlan = {

    goal_name:
      analysis.value.goal,

    goal_price:
      analysis.value.price,

    target_month:
      analysis.value.recommended_purchase,

    target_year:
      analysis.value.recommended_year,

    months_needed:
      analysis.value.months_needed,

    monthly_allocation:
      analysis.value.monthly_allocation,

    goal_progress_amount:
      analysis.value.goal_progress_amount,

    progress_percentage:
      analysis.value.progress_percentage,

    goal_status:
      analysis.value.goal_status,

    safe_to_spend:
      analysis.value.safe_to_spend,

    balance:
      analysis.value
        .financial_context
        ?.balance || 10000,

    monthly_income:
      analysis.value
        .financial_context
        ?.monthly_income || 15000,

    monthly_spending:
      analysis.value
        .financial_context
        ?.average_monthly_spending || 4000,

    monthly_commitments:
      analysis.value
        .financial_context
        ?.monthly_commitments || 3000,

    existing_goal_name:
      analysis.value
        .financial_context
        ?.other_goal_name ||
      'Mauritius Trip',

    existing_goal_amount:
      analysis.value
        .financial_context
        ?.other_goal_amount || 8000,

    existing_goal_target:
      analysis.value
        .financial_context
        ?.other_goal_target ||
      'July 2027',

    existing_goal_monthly_allocation:
      analysis.value
        .financial_context
        ?.required_other_goal_monthly || 0
  }

  sessionStorage.setItem(
    'jeebikCreatedPlan',
    JSON.stringify(createdPlan)
  )

  console.log(
    'JEEBIK Created Plan:',
    createdPlan
  )

  router.push('/goal-tracking')
}
</script>

<template>
  <div class="page">
    <main class="bank-app">

      <!-- HEADER -->
      <header class="header">

        <button
          type="button"
          class="back-button"
          aria-label="Back"
          @click="goBack"
        >
          <svg viewBox="0 0 24 24">
            <path
              d="M15 18l-6-6 6-6"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>

        <h1>
          AI-Powered Financial Planning
        </h1>

      </header>

      <!-- YOUR GOAL -->
      <section class="goal-section">

        <p class="section-label">
          YOUR GOAL
        </p>

        <div class="goal-card">

          <div class="goal-icon">
            <svg viewBox="0 0 28 24">

              <rect
                x="5"
                y="3"
                width="18"
                height="13"
                rx="1.5"
              />

              <path
                d="M3 19h22l-2 2H5l-2-2z"
              />

            </svg>
          </div>

          <div class="goal-info">

            <strong>
              {{ analysis.goal }}
            </strong>

            <span>
              {{ formatSAR(analysis.price) }}
            </span>

          </div>

        </div>

      </section>

      <!-- ANALYSIS -->
      <section class="analysis-section">

        <div class="analysis-title-row">

          <p class="section-label analysis-label">
            JEEBIK ANALYZED YOUR FINANCES
          </p>

          <div
            v-if="!isLoading"
            class="ai-status"
            :class="{ fallback: !aiIsActive }"
          >
            <span class="status-dot"></span>
            {{ aiModelLabel }}
          </div>

        </div>

        <div class="chips">
          <span>Income</span>
          <span>Spending</span>
          <span>Balance</span>
          <span>Commitments</span>
          <span>Other Goals</span>
        </div>

        <div class="analysis-card">

          <!-- RECOMMENDATION -->
          <div class="recommendation">

            <div class="ai-insight-label">
              <span class="sparkle">✦</span>
              AI FINANCIAL ANALYSIS
            </div>

            <p class="recommendation-label">
              RECOMMENDED PURCHASE
            </p>

            <h2>
              {{
                isLoading
                  ? 'Analyzing...'
                  : `${analysis.recommended_purchase} ${analysis.recommended_year || ''}`
              }}
            </h2>

            <div
              v-if="isLoading"
              class="ai-loading"
            >
              <span class="loading-dot"></span>

              <div>
                <strong>
                  JEEBIK AI is analyzing your finances
                </strong>

                <p>
                  Reviewing your income, spending,
                  balance, commitments, and other goals...
                </p>
              </div>
            </div>

            <template v-else>

              <button
                type="button"
                class="why-button"
                @click="toggleWhy"
              >

                <span>
                  Why
                  {{ analysis.recommended_purchase }}?
                </span>

                <svg
                  viewBox="0 0 24 24"
                  :class="{ rotated: showWhy }"
                >
                  <path
                    d="M6 9l6 6 6-6"
                  />
                </svg>

              </button>

              <div
                v-if="showWhy"
                class="why-explanation"
              >

                <div class="ai-answer-heading">
                  <span class="sparkle">✦</span>

                  <span>
                    JEEBIK AI INTERPRETATION
                  </span>
                </div>

                <p>
                  {{ aiMessage }}
                </p>

                <div class="ai-flow">
                  <span>UNDERSTAND CONTEXT</span>
                  <strong>→</strong>
                  <span>INTERPRET PLAN</span>
                </div>

              </div>

            </template>

          </div>

          <div class="divider"></div>

          <!-- MONTHLY COMMITMENTS -->
          <div class="details-section">

            <div class="detail-heading-row">

              <div class="heading-icon">

                <svg viewBox="0 0 24 24">

                  <rect
                    x="4"
                    y="5.5"
                    width="16"
                    height="14"
                    rx="2"
                  />

                  <path
                    d="M8 3v5M16 3v5M4 10h16"
                  />

                  <path
                    d="M8 14h3M8 17h5"
                  />

                </svg>

              </div>

              <p class="detail-heading">
                Monthly Commitments
              </p>

            </div>

            <div
              v-for="commitment in commitments"
              :key="commitment.name"
              class="detail-row"
            >

              <span>
                {{ commitment.name }}
              </span>

              <strong>
                {{ commitment.amount }}
              </strong>

            </div>

            <div class="total-row">

              <span>
                Total Monthly Commitments
              </span>

              <strong>
                SAR 3,000
              </strong>

            </div>

          </div>

          <div class="divider"></div>

          <!-- EXISTING GOALS -->
          <div
            class="details-section other-goals-section"
          >

            <div class="detail-heading-row">

              <div class="heading-icon">

                <svg viewBox="0 0 24 24">

                  <circle
                    cx="12"
                    cy="12"
                    r="8"
                  />

                  <path
                    d="M12 8v4l3 2"
                  />

                </svg>

              </div>

              <p class="detail-heading">
                Your Other Goals
              </p>

            </div>

            <div class="other-goal">

              <div class="trip-icon">

                <svg viewBox="0 0 24 24">

                  <path
                    d="M12 3v7M12 10L5 13.5v1.8l7-1.7 7 1.7v-1.8L12 10zM12 13.6v5M9.5 21l2.5-2 2.5 2"
                  />

                </svg>

              </div>

              <div class="trip-info">

                <strong>
                  Mauritius Trip
                </strong>

                <span>
                  Target July 2027
                </span>

              </div>

              <div class="trip-values">

                <strong class="trip-price">
                  SAR 8,000 total
                </strong>

                <span class="trip-allocation">
                  {{
                    formatSAR(
                      analysis
                        .financial_context
                        ?.required_other_goal_monthly
                        || 0
                    )
                  }}/mo
                </span>

              </div>

            </div>

          </div>

        </div>

      </section>

      <!-- MONTHLY ALLOCATION -->
      <section class="allocation-card">

        <div>

          <span>
            Suggested Monthly Allocation
          </span>

          <small>
            For your new {{ analysis.goal }} goal
          </small>

        </div>

        <strong>
          {{
            formatSAR(
              analysis.monthly_allocation
            )
          }}

          <span>/mo</span>
        </strong>

      </section>

      <!-- SAFE TO SPEND -->
      <section class="safe-spend-card">

        <div>

          <span>
            Safe to Spend This Month
          </span>

          <small>
            After your regular spending,
            monthly commitments,
            and all goal allocations
          </small>

        </div>

        <strong>
          {{
            formatSAR(
              analysis.safe_to_spend
            )
          }}
        </strong>

      </section>

      <!-- CREATE GOAL -->
      <button
        type="button"
        class="create-button"
        :disabled="isLoading || apiError"
        @click="createGoal"
      >
        Create Goal
      </button>

    </main>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

button {
  font: inherit;
}

.page {
  min-height: 100vh;
  background: #f5f6f7;
  display: flex;
  justify-content: center;
  color: #1d1d1b;

  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Arial,
    sans-serif;
}

.bank-app {
  width: 100%;
  max-width: 430px;
  min-height: 100vh;
  background: #ffffff;
  padding: 28px 26px 42px;
}

/* HEADER */

.header {
  position: relative;
  min-height: 38px;
  display: flex;
  align-items: center;
  margin-bottom: 19px;
}

.header h1 {
  width: 100%;
  margin: 0;
  padding: 0 32px;
  text-align: center;
  color: #242321;
  font-size: 17px;
  line-height: 1.25;
  font-weight: 750;
}

.back-button {
  position: absolute;
  left: -7px;
  top: 50%;
  transform: translateY(-50%);
  width: 38px;
  height: 38px;
  padding: 0;
  border: 0;
  background: transparent;
  color: #44423e;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.back-button svg {
  width: 25px;
  height: 25px;
}

/* LABELS */

.section-label {
  margin: 0 0 8px;
  color: #96918a;
  font-size: 10px;
  line-height: 1;
  font-weight: 800;
  letter-spacing: 0.8px;
}

/* GOAL */

.goal-section {
  margin-bottom: 20px;
}

.goal-card {
  min-height: 62px;
  padding: 9px 13px;
  border-radius: 14px;
  background: #f3f0e9;
  display: flex;
  align-items: center;
  gap: 11px;
}

.goal-icon {
  flex: 0 0 auto;
  width: 39px;
  height: 39px;
  border-radius: 10px;
  background: #ffffff;
  color: #698ba5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.goal-icon svg {
  width: 23px;
  height: 20px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.goal-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.goal-info strong {
  color: #302f2c;
  font-size: 14px;
  font-weight: 750;
}

.goal-info span {
  color: #55514c;
  font-size: 12px;
  font-weight: 700;
}

/* AI STATUS */

.analysis-title-row {
  min-height: 22px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.analysis-label {
  margin-top: 5px;
}

.ai-status {
  flex: 0 0 auto;
  padding: 4px 7px;
  border-radius: 20px;
  background: #e6f2eb;
  color: #397152;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 8px;
  font-weight: 850;
  letter-spacing: 0.4px;
}

.ai-status.fallback {
  background: #f2eee5;
  color: #7c6a47;
}

.status-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
}

/* CHIPS */

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 10px;
}

.chips span {
  padding: 5px 9px;
  border-radius: 20px;
  background: #f1f0ed;
  color: #68645f;
  font-size: 10px;
  line-height: 1;
  font-weight: 700;
}

/* ANALYSIS CARD */

.analysis-card {
  overflow: hidden;
  border-radius: 16px;
  background: #e9f2f7;
}

/* RECOMMENDATION */

.recommendation {
  padding: 15px 18px 14px;
}

.ai-insight-label {
  margin-bottom: 9px;
  color: #58788e;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 8px;
  font-weight: 850;
  letter-spacing: 0.7px;
}

.sparkle {
  color: #315b7a;
  font-size: 12px;
}

.recommendation-label {
  margin: 0 0 4px;
  color: #627b8d;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.7px;
}

.recommendation h2 {
  margin: 0 0 10px;
  color: #315b7a;
  font-size: 28px;
  line-height: 1;
  font-weight: 800;
}

.why-button {
  width: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  color: #315b7a;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  text-align: left;
}

.why-button span {
  font-size: 12px;
  font-weight: 750;
}

.why-button svg {
  width: 17px;
  height: 17px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: transform 0.2s ease;
}

.why-button svg.rotated {
  transform: rotate(180deg);
}

.why-explanation {
  margin-top: 8px;
  padding: 10px;
  border-radius: 9px;
  background: rgba(255, 255, 255, 0.55);
  color: #4f6473;
}

.ai-answer-heading {
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
  color: #315b7a;
  font-size: 8px;
  font-weight: 850;
  letter-spacing: 0.5px;
}

.why-explanation p {
  margin: 0;
  font-size: 11px;
  line-height: 1.5;
}

.ai-flow {
  margin-top: 9px;
  padding-top: 8px;
  border-top: 1px solid rgba(73, 108, 132, 0.13);
  display: flex;
  align-items: center;
  gap: 5px;
  color: #6d8492;
  font-size: 7px;
  font-weight: 800;
  letter-spacing: 0.25px;
}

.ai-flow strong {
  color: #315b7a;
}

.ai-loading {
  margin-top: 10px;
  padding: 10px;
  border-radius: 9px;
  background: rgba(255, 255, 255, 0.55);
  display: flex;
  align-items: flex-start;
  gap: 8px;
  color: #4f6473;
}

.loading-dot {
  flex: 0 0 auto;
  width: 7px;
  height: 7px;
  margin-top: 4px;
  border-radius: 50%;
  background: #527fa4;
  animation: pulse 1s infinite alternate;
}

.ai-loading strong {
  display: block;
  color: #315b7a;
  font-size: 10px;
}

.ai-loading p {
  margin: 3px 0 0;
  font-size: 9px;
  line-height: 1.4;
}

@keyframes pulse {
  from {
    opacity: 0.35;
  }

  to {
    opacity: 1;
  }
}

/* DIVIDER */

.divider {
  height: 1px;
  margin: 0 18px;
  background: rgba(73, 108, 132, 0.14);
}

/* DETAILS */

.details-section {
  padding: 13px 18px 14px;
}

.detail-heading-row {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 10px;
}

.heading-icon {
  flex: 0 0 auto;
  width: 26px;
  height: 26px;
  border-radius: 7px;
  background: rgba(255, 255, 255, 0.58);
  color: #58788e;
  display: flex;
  align-items: center;
  justify-content: center;
}

.heading-icon svg {
  width: 15px;
  height: 15px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.detail-heading {
  margin: 0;
  color: #405e71;
  font-size: 12px;
  font-weight: 750;
}

/* COMMITMENTS */

.detail-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 7px;
  color: #536773;
  font-size: 11px;
}

.detail-row strong {
  color: #3e5868;
  font-size: 11px;
  font-weight: 750;
}

.total-row {
  margin-top: 9px;
  padding-top: 9px;
  border-top:
    1px solid rgba(73, 108, 132, 0.14);
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #31566d;
  font-size: 12px;
  font-weight: 800;
}

.total-row strong {
  font-size: 12px;
}

/* OTHER GOALS */

.other-goals-section {
  padding-bottom: 13px;
}

.other-goal {
  display: flex;
  align-items: center;
  gap: 9px;
}

.trip-icon {
  flex: 0 0 auto;
  width: 32px;
  height: 32px;
  border-radius: 9px;
  background: rgba(255, 255, 255, 0.62);
  color: #66859b;
  display: flex;
  align-items: center;
  justify-content: center;
}

.trip-icon svg {
  width: 16px;
  height: 16px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.trip-info {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.trip-info strong {
  color: #3f596a;
  font-size: 11px;
  font-weight: 750;
}

.trip-info span {
  color: #6d8492;
  font-size: 9px;
  font-weight: 600;
}

.trip-values {
  margin-left: auto;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.trip-price {
  color: #3f596a;
  font-size: 11px;
  font-weight: 800;
  white-space: nowrap;
}

.trip-allocation {
  color: #315b7a;
  font-size: 9px;
  font-weight: 750;
  white-space: nowrap;
}

/* ALLOCATION */

.allocation-card {
  min-height: 64px;
  margin-top: 13px;
  padding: 10px 14px;
  border: 1px solid #e5e2dc;
  border-radius: 13px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.allocation-card > div {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.allocation-card > div > span {
  color: #45423e;
  font-size: 11px;
  font-weight: 750;
}

.allocation-card small {
  color: #85817b;
  font-size: 9px;
  line-height: 1.3;
}

.allocation-card > strong {
  flex: 0 0 auto;
  color: #315b7a;
  font-size: 15px;
  font-weight: 800;
  white-space: nowrap;
}

.allocation-card > strong span {
  font-size: 9px;
  font-weight: 650;
}

/* SAFE TO SPEND */

.safe-spend-card {
  min-height: 64px;
  margin-top: 10px;
  padding: 10px 14px;
  border-radius: 13px;
  background: #d4e6f1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.safe-spend-card > div {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.safe-spend-card > div > span {
  color: #315b7a;
  font-size: 11px;
  font-weight: 800;
}

.safe-spend-card small {
  max-width: 235px;
  color: #627b8d;
  font-size: 9px;
  line-height: 1.3;
}

.safe-spend-card > strong {
  flex: 0 0 auto;
  color: #315b7a;
  font-size: 17px;
  font-weight: 800;
  white-space: nowrap;
}

/* CREATE BUTTON */

.create-button {
  width: 100%;
  height: 47px;
  margin-top: 14px;
  border: 0;
  border-radius: 12px;
  background: #527fa4;
  color: #ffffff;
  font-size: 13px;
  font-weight: 750;
  cursor: pointer;

  transition:
    transform 0.15s ease,
    opacity 0.15s ease;
}

.create-button:active {
  transform: scale(0.99);
}

.create-button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

@media (max-width: 380px) {
  .bank-app {
    padding-left: 20px;
    padding-right: 20px;
  }

  .header h1 {
    font-size: 16px;
  }

  .recommendation h2 {
    font-size: 27px;
  }

  .analysis-title-row {
    align-items: flex-start;
  }

  .ai-status {
    font-size: 7px;
  }
}
</style>