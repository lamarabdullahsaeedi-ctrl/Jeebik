<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectedOption = ref('buy_earlier')
const planUpdated = ref(false)
const loading = ref(true)
const errorMessage = ref('')

const currentPlan = ref(null)
const priceChange = ref(null)
const replanData = ref(null)

function formatMoney(value) {
  const number = Number(value || 0)

  return new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 0
  }).format(number)
}

function goBack() {
  router.push('/goal-tracking')
}

function selectOption(option) {
  selectedOption.value = option
  planUpdated.value = false
}

const buyEarlierOption = computed(() => {
  if (!replanData.value?.options) {
    return null
  }

  return replanData.value.options.find(
    option => option.id === 'buy_earlier'
  )
})

const reduceAllocationOption = computed(() => {
  if (!replanData.value?.options) {
    return null
  }

  return replanData.value.options.find(
    option =>
      option.id === 'keep_target_reduce_allocation'
  )
})

const selectedPlanOption = computed(() => {
  if (!replanData.value?.options) {
    return null
  }

  return replanData.value.options.find(
    option => option.id === selectedOption.value
  )
})

const aiIsActive = computed(() => {
  return replanData.value?.ai_agent?.status === 'active'
})

const aiMessage = computed(() => {
  return (
    replanData.value?.ai_agent?.message ||
    replanData.value?.explanation ||
    ''
  )
})

const aiModelLabel = computed(() => {
  const model = replanData.value?.ai_agent?.model

  if (!model) {
    return 'JEEBIK AI'
  }

  if (model.includes('gemini')) {
    return 'GEMINI'
  }

  return 'AI'
})

async function loadReplanning() {
  loading.value = true
  errorMessage.value = ''

  try {
    const savedPlan =
      sessionStorage.getItem(
        'jeebikCreatedPlan'
      )

    const savedPriceChange =
      sessionStorage.getItem(
        'jeebikPriceChange'
      )

    if (!savedPlan) {
      throw new Error(
        'No active JEEBIK goal was found.'
      )
    }

    if (!savedPriceChange) {
      throw new Error(
        'No price change was found for this goal.'
      )
    }

    currentPlan.value =
      JSON.parse(savedPlan)

    priceChange.value =
      JSON.parse(savedPriceChange)

    const requestBody = {
      goal_name:
        currentPlan.value.goal_name ||
        priceChange.value.goal_name ||
        'MacBook Pro 16"',

      previous_price:
        Number(
          priceChange.value.previous_price ??
          currentPlan.value.goal_price ??
          0
        ),

      new_price:
        Number(
          priceChange.value.new_price ?? 0
        ),

      current_progress_amount:
        Number(
          currentPlan.value
            .goal_progress_amount ?? 0
        ),

      current_monthly_allocation:
        Number(
          currentPlan.value
            .monthly_allocation ?? 0
        ),

      current_target_month:
        currentPlan.value.target_month ||
        'December',

      current_target_year:
        Number(
          currentPlan.value.target_year ||
          new Date().getFullYear()
        ),

      balance:
        Number(
          currentPlan.value.balance ??
          10000
        ),

      monthly_income:
        Number(
          currentPlan.value.monthly_income ??
          15000
        ),

      monthly_spending:
        Number(
          currentPlan.value.monthly_spending ??
          4000
        ),

      monthly_commitments:
        Number(
          currentPlan.value
            .monthly_commitments ??
          3000
        ),

      other_goal_name:
        currentPlan.value
          .existing_goal_name ||
        'Mauritius Trip',

      other_goal_amount:
        Number(
          currentPlan.value
            .existing_goal_amount ??
          8000
        ),

      other_goal_target_year:
        2027,

      other_goal_target_month:
        7
    }

    const response = await fetch(
      'https://jeebik-backend.onrender.com/replan',
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify(
          requestBody
        )
      }
    )

    if (!response.ok) {
      const errorText =
        await response.text()

      throw new Error(
        errorText ||
        'JEEBIK could not recalculate the plan.'
      )
    }

    replanData.value =
      await response.json()

    if (
      replanData.value?.options?.length > 0
    ) {
      selectedOption.value =
        replanData.value.options[0].id
    }

  } catch (error) {
    console.error(
      'Replanning error:',
      error
    )

    errorMessage.value =
      error.message ||
      'Something went wrong while recalculating your plan.'

  } finally {
    loading.value = false
  }
}

function updatePlan() {
  const option =
    selectedPlanOption.value

  if (
    !option ||
    !currentPlan.value ||
    !replanData.value
  ) {
    return
  }

  const updatedPlan = {
    ...currentPlan.value,

    goal_name:
      replanData.value.goal,

    goal_price:
      Number(
        replanData.value.new_price
      ),

    target_month:
      option.target_month,

    target_year:
      Number(
        option.target_year
      ),

    monthly_allocation:
      Number(
        option.monthly_allocation
      ),

    future_monthly_allocation:
      Number(
        option.future_monthly_allocation ??
        option.monthly_allocation
      ),

    goal_progress_amount:
      Number(
        option.goal_progress_amount
      ),

    progress_percentage:
      Number(
        option.progress_percentage
      ),

    goal_status:
      option.goal_status ||
      'On Track',

    safe_to_spend:
      Number(
        option.safe_to_spend
      ),

    total_goal_allocations:
      Number(
        option.total_goal_allocations ?? 0
      ),

    released_monthly_capacity:
      Number(
        option.released_monthly_capacity ?? 0
      ),

    remaining_amount:
      Number(
        option.remaining_amount ?? 0
      ),

    available_for_planning:
      Number(
        replanData.value
          ?.financial_context
          ?.available_for_planning ?? 0
      ),

    replan_choice:
      option.id,

    replanned:
      true,

    previous_price:
      Number(
        replanData.value.previous_price
      ),

    price_savings:
      Number(
        replanData.value.savings
      )
  }

  sessionStorage.setItem(
    'jeebikCreatedPlan',
    JSON.stringify(updatedPlan)
  )

  sessionStorage.setItem(
    'jeebikReplanAccepted',
    'true'
  )

  sessionStorage.removeItem(
    'jeebikPriceChange'
  )

  planUpdated.value = true

  setTimeout(() => {
    router.push('/goal-tracking')
  }, 900)
}

onMounted(() => {
  loadReplanning()
})
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

        <div class="page-title">
          <h1>Plan Update</h1>

          <span>
            PROACTIVE REPLANNING BY JEEBIK
          </span>
        </div>
      </header>

      <!-- LOADING -->
      <section
        v-if="loading"
        class="state-card"
      >
        <div class="loader"></div>

        <strong>
          JEEBIK AI is analyzing the change
        </strong>

        <span>
          Checking the new price against your
          financial context and active goals...
        </span>
      </section>

      <!-- ERROR -->
      <section
        v-else-if="errorMessage"
        class="state-card error"
      >
        <strong>
          We couldn't update the plan
        </strong>

        <span>
          {{ errorMessage }}
        </span>

        <button
          type="button"
          class="retry-button"
          @click="loadReplanning"
        >
          Try Again
        </button>
      </section>

      <!-- CONTENT -->
      <template
        v-else-if="replanData"
      >

        <!-- UPDATE LABEL -->
        <div class="update-label">
          <span class="pulse-dot"></span>
          PRICE CHANGE DETECTED
        </div>

        <!-- PRODUCT -->
        <section class="product-card">
          <div class="product-icon">
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

          <div class="product-info">
            <span>YOUR GOAL</span>

            <strong>
              {{ replanData.goal }}
            </strong>
          </div>
        </section>

        <!-- PRICE CHANGE -->
        <section class="price-card">
          <div class="price-heading">
            <div class="price-icon">
              <svg viewBox="0 0 24 24">
                <path d="M12 3v18" />
                <path d="M7 16l5 5 5-5" />
              </svg>
            </div>

            <div>
              <span>
                New lower price detected
              </span>

              <strong>
                You can now save SAR
                {{
                  formatMoney(
                    replanData.savings
                  )
                }}
              </strong>
            </div>
          </div>

          <div class="price-comparison">
            <div class="price-box">
              <span>
                Previous Price
              </span>

              <strong class="old-price">
                SAR
                {{
                  formatMoney(
                    replanData.previous_price
                  )
                }}
              </strong>
            </div>

            <div class="arrow">
              <svg viewBox="0 0 24 24">
                <path d="M5 12h14" />
                <path d="M15 8l4 4-4 4" />
              </svg>
            </div>

            <div class="price-box new">
              <span>New Price</span>

              <strong>
                SAR
                {{
                  formatMoney(
                    replanData.new_price
                  )
                }}
              </strong>
            </div>
          </div>
        </section>

        <!-- LIVE AI INSIGHT -->
        <section class="jeebik-card">
          <div class="jeebik-heading">
            <img
              src="/jeebik-logo.png"
              alt="JEEBIK"
            />

            <div class="jeebik-title-area">
              <div class="brand-line">
                <strong>JEEBIK</strong>
                <span>AI</span>
              </div>

              <p>
                AI financial insight
              </p>
            </div>

            <div
              class="ai-status"
              :class="{
                active: aiIsActive,
                fallback: !aiIsActive
              }"
            >
              <span class="status-dot"></span>

              {{
                aiIsActive
                  ? `${aiModelLabel} ACTIVE`
                  : 'SAFE FALLBACK'
              }}
            </div>
          </div>

          <div class="ai-insight-label">
            <span class="sparkle">✦</span>
            AI AGENT INTERPRETATION
          </div>

          <p class="jeebik-message">
            {{ aiMessage }}
          </p>

          <div class="ai-flow">
            <span>UNDERSTAND</span>
            <b>→</b>
            <span>TRIGGER</span>
            <b>→</b>
            <span>INTERPRET</span>
          </div>

          <div class="progress-summary">
            <span>
              Updated goal coverage
            </span>

            <strong>
              {{
                replanData
                  .updated_goal
                  .progress_percentage
              }}%
            </strong>
          </div>
        </section>

        <!-- OPTIONS -->
        <section class="options-section">
          <p class="section-label">
            CHOOSE WHAT WORKS FOR YOU
          </p>

          <!-- OPTION 1 -->
          <button
            v-if="buyEarlierOption"
            type="button"
            class="option-card"
            :class="{
              selected:
                selectedOption ===
                'buy_earlier'
            }"
            @click="
              selectOption('buy_earlier')
            "
          >
            <div class="radio">
              <div
                v-if="
                  selectedOption ===
                  'buy_earlier'
                "
                class="radio-dot"
              ></div>
            </div>

            <div class="option-content">
              <div class="option-top">
                <div>
                  <span class="option-number">
                    OPTION 1
                  </span>

                  <strong>
                    {{
                      buyEarlierOption.title
                    }}
                  </strong>
                </div>

                <span class="month-badge">
                  {{
                    buyEarlierOption
                      .target_month
                  }}
                </span>
              </div>

              <p>
                {{
                  buyEarlierOption
                    .description
                }}
              </p>

              <div class="option-result">
                <span>
                  Target date
                </span>

                <strong>
                  <span class="crossed">
                    {{
                      replanData
                        .previous_plan
                        .target_month
                    }}
                  </span>

                  <span class="result-arrow">
                    →
                  </span>

                  {{
                    buyEarlierOption
                      .target_month
                  }}

                  {{
                    buyEarlierOption
                      .target_year
                  }}
                </strong>
              </div>

              <div class="option-detail">
                <span>
                  Remaining monthly allocation
                </span>

                <strong>
                  SAR
                  {{
                    formatMoney(
                      buyEarlierOption
                        .monthly_allocation
                    )
                  }}
                </strong>
              </div>

              <div class="safe-benefit">
                <svg viewBox="0 0 24 24">
                  <path d="M12 21V3" />
                  <path d="M7 8l5-5 5 5" />
                </svg>

                <span>
                  Safe to Spend:
                  SAR
                  {{
                    formatMoney(
                      buyEarlierOption
                        .safe_to_spend
                    )
                  }}
                </span>
              </div>
            </div>
          </button>

          <!-- OPTION 2 -->
          <button
            v-if="reduceAllocationOption"
            type="button"
            class="option-card"
            :class="{
              selected:
                selectedOption ===
                'keep_target_reduce_allocation'
            }"
            @click="
              selectOption(
                'keep_target_reduce_allocation'
              )
            "
          >
            <div class="radio">
              <div
                v-if="
                  selectedOption ===
                  'keep_target_reduce_allocation'
                "
                class="radio-dot"
              ></div>
            </div>

            <div class="option-content">
              <div class="option-top">
                <div>
                  <span class="option-number">
                    OPTION 2
                  </span>

                  <strong>
                    {{
                      reduceAllocationOption
                        .title
                    }}
                  </strong>
                </div>

                <span
                  class="month-badge neutral"
                >
                  Keep
                  {{
                    reduceAllocationOption
                      .target_month
                  }}
                </span>
              </div>

              <p>
                {{
                  reduceAllocationOption
                    .description
                }}
              </p>

              <div class="option-result">
                <span>
                  Monthly allocation
                </span>

                <strong>
                  <span class="crossed">
                    SAR
                    {{
                      formatMoney(
                        replanData
                          .previous_plan
                          .monthly_allocation
                      )
                    }}
                  </span>

                  <span class="result-arrow">
                    →
                  </span>

                  SAR
                  {{
                    formatMoney(
                      reduceAllocationOption
                        .monthly_allocation
                    )
                  }}
                </strong>
              </div>

              <div class="option-detail">
                <span>
                  Goal coverage
                </span>

                <strong>
                  {{
                    reduceAllocationOption
                      .progress_percentage
                  }}%
                </strong>
              </div>

              <div class="safe-benefit">
                <svg viewBox="0 0 24 24">
                  <path d="M12 21V3" />
                  <path d="M7 8l5-5 5 5" />
                </svg>

                <span>
                  Safe to Spend increases to
                  SAR
                  {{
                    formatMoney(
                      reduceAllocationOption
                        .safe_to_spend
                    )
                  }}
                </span>
              </div>
            </div>
          </button>
        </section>

        <!-- UPDATE BUTTON -->
        <button
          type="button"
          class="update-button"
          :disabled="planUpdated"
          @click="updatePlan"
        >
          {{
            planUpdated
              ? 'Updating Plan...'
              : 'Update My Plan'
          }}
        </button>

        <!-- SUCCESS -->
        <Transition name="success">
          <div
            v-if="planUpdated"
            class="success-message"
          >
            <div class="check">
              <svg viewBox="0 0 24 24">
                <path
                  d="M5 12l4 4 10-10"
                />
              </svg>
            </div>

            <div>
              <strong>
                Plan updated
              </strong>

              <span
                v-if="
                  selectedOption ===
                  'buy_earlier'
                "
              >
                Your new target is
                {{
                  buyEarlierOption
                    ?.target_month
                }}
                {{
                  buyEarlierOption
                    ?.target_year
                }}.
              </span>

              <span v-else>
                Your monthly allocation is now
                SAR
                {{
                  formatMoney(
                    reduceAllocationOption
                      ?.monthly_allocation
                  )
                }}.
              </span>
            </div>
          </div>
        </Transition>

        <p class="final-line">
          Plans change. JEEBIK adapts.
        </p>

      </template>

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
  color: #242321;

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
  padding: 26px 25px 40px;
  background: #ffffff;
}

/* HEADER */

.header {
  position: relative;
  min-height: 48px;
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.page-title {
  width: 100%;
  padding: 0 38px;
  text-align: center;

  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}

.page-title h1 {
  margin: 0;
  color: #242321;
  font-size: 17px;
  font-weight: 760;
}

.page-title span {
  color: #7890a0;
  font-size: 7px;
  font-weight: 850;
  letter-spacing: 0.65px;
  white-space: nowrap;
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

/* STATES */

.state-card {
  min-height: 230px;
  padding: 28px 20px;

  border: 1px solid #e5e7e8;
  border-radius: 16px;
  background: #fafafa;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;

  text-align: center;
}

.state-card strong {
  color: #3f4b52;
  font-size: 12px;
}

.state-card span {
  max-width: 270px;
  color: #7d888e;
  font-size: 10px;
  line-height: 1.5;
}

.state-card.error {
  background: #fbf5f4;
}

.loader {
  width: 27px;
  height: 27px;

  border: 3px solid #e2e9ed;
  border-top-color: #5f88a7;
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.retry-button {
  margin-top: 5px;
  padding: 8px 15px;

  border: 0;
  border-radius: 9px;

  background: #527fa4;
  color: white;

  font-size: 9px;
  font-weight: 800;

  cursor: pointer;
}

/* UPDATE LABEL */

.update-label {
  margin-bottom: 9px;
  color: #718797;
  font-size: 9px;
  font-weight: 850;
  letter-spacing: 0.9px;

  display: flex;
  align-items: center;
  gap: 6px;
}

.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #5f88a7;
  box-shadow: 0 0 0 4px #e6f0f5;
}

/* PRODUCT */

.product-card {
  min-height: 61px;
  padding: 10px 13px;

  border: 1px solid #e6e3de;
  border-radius: 14px;

  background: #faf9f7;

  display: flex;
  align-items: center;
  gap: 11px;
}

.product-icon {
  width: 38px;
  height: 38px;
  flex: 0 0 auto;

  border-radius: 10px;
  background: #f0eee9;
  color: #6888a0;

  display: flex;
  align-items: center;
  justify-content: center;
}

.product-icon svg {
  width: 22px;
  height: 20px;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.product-info span {
  color: #a09b94;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.product-info strong {
  color: #393733;
  font-size: 13px;
}

/* PRICE */

.price-card {
  margin-top: 12px;
  padding: 14px;

  border-radius: 15px;
  background: #edf5f9;
  border: 1px solid #dce9f0;
}

.price-heading {
  display: flex;
  align-items: center;
  gap: 9px;
}

.price-icon {
  width: 29px;
  height: 29px;

  border-radius: 50%;
  background: #d8e8f1;
  color: #477492;

  display: flex;
  align-items: center;
  justify-content: center;
}

.price-icon svg {
  width: 15px;
  height: 15px;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.price-heading > div:last-child {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.price-heading span {
  color: #708592;
  font-size: 9px;
  font-weight: 650;
}

.price-heading strong {
  color: #315d79;
  font-size: 12px;
}

.price-comparison {
  margin-top: 12px;

  display: flex;
  align-items: center;
  gap: 8px;
}

.price-box {
  flex: 1;
  padding: 9px 8px;

  border-radius: 9px;
  background: rgba(255, 255, 255, 0.65);

  display: flex;
  flex-direction: column;
  gap: 3px;
}

.price-box span {
  color: #8b9295;
  font-size: 8px;
}

.price-box strong {
  color: #67645f;
  font-size: 12px;
}

.price-box.new {
  background: #ffffff;
}

.price-box.new strong {
  color: #315d79;
}

.old-price {
  text-decoration: line-through;
}

.arrow {
  color: #7c99ab;
}

.arrow svg {
  width: 17px;
  height: 17px;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* JEEBIK AI */

.jeebik-card {
  margin-top: 12px;
  padding: 13px 14px;

  border-radius: 14px;
  background: #f4f8fa;
  border: 1px solid #e2edf2;
}

.jeebik-heading {
  display: flex;
  align-items: center;
  gap: 9px;
}

.jeebik-heading img {
  width: 34px;
  height: 34px;
  object-fit: contain;
}

.jeebik-title-area {
  min-width: 0;
  flex: 1;
}

.brand-line {
  display: flex;
  align-items: center;
  gap: 6px;
}

.brand-line strong {
  color: #315d79;
  font-size: 11px;
  font-weight: 850;
}

.brand-line span {
  padding: 2px 5px;

  border-radius: 10px;
  background: #315d79;
  color: #ffffff;

  font-size: 7px;
  font-weight: 800;
}

.jeebik-heading p {
  margin: 1px 0 0;
  color: #8a9296;
  font-size: 9px;
}

.ai-status {
  flex: 0 0 auto;
  padding: 5px 7px;
  border-radius: 10px;

  display: flex;
  align-items: center;
  gap: 4px;

  font-size: 6.5px;
  font-weight: 850;
  letter-spacing: 0.35px;
}

.ai-status.active {
  background: #e7f2ea;
  color: #58765f;
}

.ai-status.fallback {
  background: #f1eee8;
  color: #81796e;
}

.status-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
}

.ai-insight-label {
  margin-top: 12px;
  color: #718797;

  display: flex;
  align-items: center;
  gap: 5px;

  font-size: 7px;
  font-weight: 850;
  letter-spacing: 0.55px;
}

.sparkle {
  color: #527fa4;
  font-size: 10px;
}

.jeebik-message {
  margin: 7px 0 0;

  color: #526773;
  font-size: 9.5px;
  line-height: 1.55;
}

.ai-flow {
  margin-top: 10px;
  padding: 7px 8px;

  border-radius: 8px;
  background: rgba(255, 255, 255, 0.72);

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;

  color: #7890a0;
  font-size: 6.5px;
  font-weight: 850;
  letter-spacing: 0.35px;
}

.ai-flow b {
  color: #9aabb5;
  font-weight: 600;
}

.progress-summary {
  margin-top: 9px;
  padding-top: 9px;

  border-top: 1px solid #e1e9ed;

  display: flex;
  align-items: center;
  justify-content: space-between;
}

.progress-summary span {
  color: #839097;
  font-size: 8px;
}

.progress-summary strong {
  color: #315d79;
  font-size: 11px;
}

/* OPTIONS */

.options-section {
  margin-top: 18px;
}

.section-label {
  margin: 0 0 9px;

  color: #96918a;
  font-size: 9px;
  font-weight: 850;
  letter-spacing: 0.7px;
}

.option-card {
  width: 100%;
  margin-bottom: 10px;
  padding: 13px;

  border: 1px solid #e3e1dc;
  border-radius: 14px;

  background: #ffffff;
  color: inherit;

  text-align: left;

  display: flex;
  align-items: flex-start;
  gap: 10px;

  cursor: pointer;

  transition: 0.2s ease;
}

.option-card.selected {
  border-color: #7298b3;
  background: #f3f8fb;

  box-shadow:
    0 0 0 1px rgba(95, 136, 167, 0.08);
}

.radio {
  width: 17px;
  height: 17px;
  margin-top: 2px;
  flex: 0 0 auto;

  border: 1.5px solid #9ba7ae;
  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;
}

.option-card.selected .radio {
  border-color: #5f88a7;
}

.radio-dot {
  width: 9px;
  height: 9px;

  border-radius: 50%;
  background: #5f88a7;
}

.option-content {
  min-width: 0;
  flex: 1;
}

.option-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.option-top > div {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.option-number {
  color: #9a9690;
  font-size: 7px;
  font-weight: 850;
  letter-spacing: 0.5px;
}

.option-top strong {
  color: #3e3b37;
  font-size: 12px;
}

.month-badge {
  flex: 0 0 auto;

  padding: 5px 8px;

  border-radius: 12px;
  background: #dceaf2;

  color: #416b87;
  font-size: 8px;
  font-weight: 800;
}

.month-badge.neutral {
  background: #f0eee9;
  color: #716d67;
}

.option-content > p {
  margin: 6px 0 9px;

  color: #77736d;
  font-size: 9px;
  line-height: 1.4;
}

.option-result,
.option-detail {
  padding: 8px 9px;

  border-radius: 9px;
  background: rgba(255, 255, 255, 0.8);

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.option-detail {
  margin-top: 6px;
}

.option-result > span,
.option-detail > span {
  color: #8e8983;
  font-size: 8px;
}

.option-result strong,
.option-detail strong {
  color: #416b87;
  font-size: 10px;
  white-space: nowrap;
}

.crossed {
  color: #a29e98;
  text-decoration: line-through;
  font-weight: 600;
}

.result-arrow {
  margin: 0 4px;
  color: #8da1ae;
}

.safe-benefit {
  margin-top: 7px;

  color: #65806d;

  display: flex;
  align-items: center;
  gap: 4px;
}

.safe-benefit svg {
  width: 12px;
  height: 12px;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.safe-benefit span {
  font-size: 8px;
  font-weight: 700;
}

/* UPDATE BUTTON */

.update-button {
  width: 100%;
  min-height: 46px;
  margin-top: 3px;

  border: 0;
  border-radius: 12px;

  background: #527fa4;
  color: #ffffff;

  font-size: 11px;
  font-weight: 800;

  cursor: pointer;
}

.update-button:active {
  transform: scale(0.99);
}

.update-button:disabled {
  opacity: 0.7;
  cursor: default;
}

/* SUCCESS */

.success-message {
  margin-top: 10px;
  padding: 11px 12px;

  border-radius: 11px;
  background: #edf4ee;

  display: flex;
  align-items: center;
  gap: 9px;
}

.check {
  width: 25px;
  height: 25px;
  flex: 0 0 auto;

  border-radius: 50%;
  background: #6d8972;
  color: #ffffff;

  display: flex;
  align-items: center;
  justify-content: center;
}

.check svg {
  width: 15px;
  height: 15px;

  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.success-message > div:last-child {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.success-message strong {
  color: #536d58;
  font-size: 10px;
}

.success-message span {
  color: #738077;
  font-size: 9px;
}

.success-enter-active,
.success-leave-active {
  transition: 0.25s ease;
}

.success-enter-from,
.success-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

/* END */

.final-line {
  margin: 14px 0 0;

  text-align: center;

  color: #8d8983;
  font-size: 9px;
  font-weight: 650;
}

@media (max-width: 380px) {
  .bank-app {
    padding-left: 20px;
    padding-right: 20px;
  }

  .page-title span {
    font-size: 6px;
    letter-spacing: 0.45px;
  }

  .ai-status {
    font-size: 6px;
    padding: 4px 6px;
  }
}
</style>