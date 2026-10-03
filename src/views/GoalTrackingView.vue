<script setup>
import {
  ref,
  computed,
  onMounted,
  onBeforeUnmount
} from 'vue'

import { useRouter } from 'vue-router'

const router = useRouter()

const showNotification = ref(false)

let notificationTimer = null


// --------------------------------------------------
// CREATED PLAN
// --------------------------------------------------

const plan = ref({
  goal_name: 'MacBook Air 15"',
  goal_price: 5999,

  target_month: 'November',
  target_year: 2026,

  months_needed: 1,

  monthly_allocation: 4500,

  goal_progress_amount: 4500,
  progress_percentage: 0,
  goal_status: 'On Track',

  safe_to_spend: 2600,

  balance: 10000,
  monthly_income: 15000,
  monthly_spending: 4000,
  monthly_commitments: 3000,

  existing_goal_name: 'Mauritius Trip',
  existing_goal_amount: 8000,
  existing_goal_target: 'July 2027',
  existing_goal_monthly_allocation: 900
})


// --------------------------------------------------
// LOAD PLAN FROM ANALYSIS
// --------------------------------------------------

function loadCreatedPlan() {

  const savedPlan =
    sessionStorage.getItem('jeebikCreatedPlan')

  if (!savedPlan) {
    return
  }

  try {

    const parsedPlan =
      JSON.parse(savedPlan)

    plan.value = {
      ...plan.value,
      ...parsedPlan
    }

  } catch (error) {

    console.error(
      'Could not read created JEEBIK plan:',
      error
    )
  }
}


// --------------------------------------------------
// COMPUTED VALUES
// --------------------------------------------------

const totalGoalAllocation = computed(() => {

  return (
    Number(plan.value.monthly_allocation || 0) +
    Number(
      plan.value
        .existing_goal_monthly_allocation || 0
    )
  )
})


const progressPercentage = computed(() => {

  const backendProgress =
    Number(plan.value.progress_percentage || 0)

  return Math.min(
    Math.max(backendProgress, 0),
    100
  )
})


const displayedProgressPercentage = computed(() => {

  return Math.round(
    progressPercentage.value
  )
})


// --------------------------------------------------
// DEMO PRICE MONITORING EVENT
// --------------------------------------------------
//
// This represents the simulated external
// market-price change.
//
// IMPORTANT:
//
// Detecting the price change does NOT modify
// the user's active financial plan.
//
// It only creates a notification/event.
//
// The plan changes only after the user reviews
// the replanning options and explicitly accepts one.
// --------------------------------------------------

const priceDropNewPrice = computed(() => {

  if (
    plan.value.goal_name ===
    'MacBook Pro 16"'
  ) {
    return 6999
  }

  if (
    plan.value.goal_name ===
    'MacBook Air 15"'
  ) {
    return 5299
  }

  return Math.max(
    Number(plan.value.goal_price || 0) - 700,
    0
  )
})


const priceDropSavings = computed(() => {

  return Math.max(
    Number(plan.value.goal_price || 0) -
      Number(priceDropNewPrice.value || 0),
    0
  )
})


// --------------------------------------------------
// PRICE CHANGE EVENT
// --------------------------------------------------

function savePriceChangeForReview() {

  const priceChange = {

    goal_name:
      plan.value.goal_name,

    previous_price:
      Number(
        plan.value.goal_price || 0
      ),

    new_price:
      Number(
        priceDropNewPrice.value || 0
      ),

    savings:
      Number(
        priceDropSavings.value || 0
      ),

    detected_at:
      new Date().toISOString()
  }


  sessionStorage.setItem(
    'jeebikPriceChange',
    JSON.stringify(priceChange)
  )
}


// --------------------------------------------------
// LIFECYCLE
// --------------------------------------------------

onMounted(() => {

  loadCreatedPlan()


  // If the user already accepted a replanning option,
  // do not trigger the same price-drop event again.

  const replanAccepted =
    sessionStorage.getItem(
      'jeebikReplanAccepted'
    ) === 'true'


  if (replanAccepted) {

    showNotification.value = false

    return
  }


  // ------------------------------------------------
  // SIMULATED PRICE MONITORING
  // ------------------------------------------------
  //
  // First, the user sees the original goal plan.
  //
  // After 4 seconds JEEBIK detects the simulated
  // external price change.
  //
  // At THAT SAME MOMENT:
  //
  // 1. The top proactive notification appears.
  // 2. The event is saved in the Notification Center.
  //
  // The active financial plan is NOT changed.
  // ------------------------------------------------

  notificationTimer =
    setTimeout(() => {

      savePriceChangeForReview()

      showNotification.value = true

    }, 4000)

})


onBeforeUnmount(() => {

  if (notificationTimer) {

    clearTimeout(
      notificationTimer
    )
  }

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

  router.push('/analysis')
}


function closeNotification() {

  // Closing the top notification does NOT
  // remove it from the Notification Center.

  showNotification.value = false
}


// --------------------------------------------------
// NAVIGATION
// --------------------------------------------------

function reviewNewPlan() {

  // Save again as a safety check.
  // This does not change the active goal.

  savePriceChangeForReview()

  router.push('/replanning')
}


function openPlanUpdates() {

  savePriceChangeForReview()

  router.push('/replanning')
}
</script>


<template>

  <div class="page">


    <!-- ============================================= -->
    <!-- PRICE DROP NOTIFICATION -->
    <!-- ============================================= -->

    <Transition name="notification">

      <div
        v-if="showNotification"
        class="price-notification"
      >

        <div class="notification-header">

          <div class="notification-brand">

            <img
              src="/jeebik-logo.png"
              alt="JEEBIK"
              class="notification-logo"
            />


            <div class="brand-text">

              <div class="brand-name">

                <strong>
                  JEEBIK
                </strong>

                <span class="ai-badge">
                  AI
                </span>

              </div>


              <span class="notification-time">
                Now
              </span>

            </div>

          </div>


          <button
            type="button"
            class="close-button"
            aria-label="Close notification"
            @click="closeNotification"
          >
            ×
          </button>

        </div>


        <div class="notification-body">

          <div class="notification-icon">

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


          <div class="notification-message">

            <strong>
              Price drop detected
            </strong>


            <p>

              {{ plan.goal_name }} is now

              <b>
                {{ formatSAR(priceDropNewPrice) }}
              </b>

              <span class="old-price">
                {{ formatSAR(plan.goal_price) }}
              </span>

            </p>


            <span class="saving">

              You can save
              {{ formatSAR(priceDropSavings) }}

            </span>

          </div>

        </div>


        <button
          type="button"
          class="review-button"
          @click="reviewNewPlan"
        >

          Review New Plan

          <svg viewBox="0 0 24 24">
            <path d="M9 6l6 6-6 6" />
          </svg>

        </button>

      </div>

    </Transition>


    <!-- ============================================= -->
    <!-- MAIN SCREEN -->
    <!-- ============================================= -->

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
          Your Goals
        </h1>

      </header>


      <!-- =========================================== -->
      <!-- GOAL CARD -->
      <!-- =========================================== -->

      <section class="goal-card">

        <div class="goal-top">

          <div class="laptop-icon">

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


          <div class="goal-title">

            <strong>
              {{ plan.goal_name }}
            </strong>


            <span>

              {{ formatSAR(plan.goal_progress_amount) }}

              of

              {{ formatSAR(plan.goal_price) }}

              virtually planned

            </span>

          </div>

        </div>


        <!-- PROGRESS PERCENTAGE -->

        <div class="progress-summary">

          <span>
            Goal Progress
          </span>

          <strong>
            {{ displayedProgressPercentage }}%
          </strong>

        </div>


        <!-- PROGRESS BAR -->

        <div class="progress-track">

          <div
            class="progress-fill"
            :style="{
              width: `${progressPercentage}%`
            }"
          ></div>

        </div>


        <!-- TARGET + STATUS -->

        <div class="goal-bottom">

          <div>

            <span class="small-label">
              Target
            </span>


            <strong>

              {{ plan.target_month }}

              {{ plan.target_year }}

            </strong>

          </div>


          <span class="status">

            <svg
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                d="M5 12.5l4 4L19 7"
              />
            </svg>

            {{ plan.goal_status || 'On Track' }}

          </span>

        </div>

      </section>


      <!-- =========================================== -->
      <!-- MONEY -->
      <!-- =========================================== -->

      <section class="money-section">

        <p class="section-label">
          WHERE YOUR MONEY STANDS
        </p>


        <div class="money-card">


          <!-- BALANCE -->

          <div class="money-row">

            <div class="money-left">

              <div class="money-icon">

                <svg viewBox="0 0 24 24">

                  <rect
                    x="3"
                    y="6"
                    width="18"
                    height="13"
                    rx="2"
                  />

                  <path d="M3 10h18" />

                  <path d="M7 15h3" />

                </svg>

              </div>


              <span>
                Account Balance
              </span>

            </div>


            <strong>
              {{ formatSAR(plan.balance) }}
            </strong>

          </div>


          <div class="divider"></div>


          <!-- COMMITMENTS -->

          <div class="money-row">

            <div class="money-left">

              <div class="money-icon">

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


              <span>
                Monthly Commitments
              </span>

            </div>


            <strong class="deduction">

              −
              {{ formatSAR(plan.monthly_commitments) }}

            </strong>

          </div>


          <div class="divider"></div>


          <!-- GOAL ALLOCATIONS -->

          <div class="money-row">

            <div class="money-left">

              <div class="money-icon">

                <svg viewBox="0 0 24 24">

                  <circle
                    cx="12"
                    cy="12"
                    r="8"
                  />

                  <path
                    d="M12 8v8M8 12h8"
                  />

                </svg>

              </div>


              <span>
                Monthly Goal Allocations
              </span>

            </div>


            <strong class="deduction">

              −
              {{ formatSAR(totalGoalAllocation) }}

            </strong>

          </div>


          <!-- SAFE TO SPEND -->

          <div class="safe-row">

            <div>

              <span>
                Safe to Spend This Month
              </span>


              <small>

                After spending, commitments,
                and all goal allocations

              </small>

            </div>


            <strong>
              {{ formatSAR(plan.safe_to_spend) }}
            </strong>

          </div>

        </div>

      </section>


      <!-- =========================================== -->
      <!-- VIRTUAL ALLOCATION INFO -->
      <!-- =========================================== -->

      <section class="info-card">

        <div class="info-icon">

          <svg viewBox="0 0 24 24">

            <circle
              cx="12"
              cy="12"
              r="9"
            />

            <path
              d="M12 11v6"
            />

            <circle
              cx="12"
              cy="7.5"
              r="0.8"
              fill="currentColor"
              stroke="none"
            />

          </svg>

        </div>


        <div class="info-text">

          <strong>
            Your money stays in your account.
          </strong>


          <span>

            JEEBIK only tracks it against your plan.
            Nothing moves until you decide to spend it.

          </span>

        </div>

      </section>


      <!-- =========================================== -->
      <!-- PLAN UPDATES -->
      <!-- =========================================== -->

      <button
        type="button"
        class="plan-updates"
        @click="openPlanUpdates"
      >

        <div class="plan-update-icon">

          <svg viewBox="0 0 24 24">

            <path
              d="M20 7v5h-5"
            />

            <path
              d="M4 17v-5h5"
            />

            <path
              d="M6.1 8.5A7 7 0 0 1 18.8 7"
            />

            <path
              d="M17.9 15.5A7 7 0 0 1 5.2 17"
            />

          </svg>

        </div>


        <div class="plan-update-text">

          <strong>
            Plan Updates
          </strong>


          <span>
            View changes and updated recommendations
          </span>

        </div>


        <svg
          class="plan-update-arrow"
          viewBox="0 0 24 24"
        >

          <path
            d="M9 6l6 6-6 6"
          />

        </svg>

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


/* ================================================ */
/* PAGE */
/* ================================================ */

.page {
  position: relative;
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

  padding:
    28px
    26px
    45px;
}


/* ================================================ */
/* NOTIFICATION */
/* ================================================ */

.price-notification {
  position: fixed;
  z-index: 1000;

  top: 18px;
  left: 50%;

  transform: translateX(-50%);

  width: calc(100% - 32px);
  max-width: 398px;

  padding: 13px;

  border:
    1px solid #d9e5ec;

  border-radius: 17px;

  background:
    rgba(255, 255, 255, 0.98);

  box-shadow:
    0 18px 45px
      rgba(44, 67, 82, 0.17),
    0 4px 12px
      rgba(44, 67, 82, 0.08);
}


.notification-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}


.notification-brand {
  display: flex;
  align-items: center;
  gap: 8px;
}


.notification-logo {
  width: 34px;
  height: 34px;

  object-fit: contain;
}


.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}


.brand-name {
  display: flex;
  align-items: center;
  gap: 5px;
}


.brand-name strong {
  color: #315d79;

  font-size: 11px;
  font-weight: 850;
}


.ai-badge {
  padding: 2px 5px;

  border-radius: 8px;

  background: #315d79;

  color: #ffffff;

  font-size: 6px;
  font-weight: 850;
}


.notification-time {
  color: #9a9690;

  font-size: 8px;
  font-weight: 600;
}


.close-button {
  width: 27px;
  height: 27px;

  padding: 0;

  border: 0;

  background: transparent;

  color: #99948e;

  font-size: 20px;

  cursor: pointer;
}


.notification-body {
  margin-top: 10px;

  padding: 11px;

  border-radius: 12px;

  background: #edf5f9;

  display: flex;
  align-items: center;
  gap: 10px;
}


.notification-icon {
  flex: 0 0 auto;

  width: 39px;
  height: 39px;

  border-radius: 10px;

  background: #ffffff;

  color: #6286a0;

  display: flex;
  align-items: center;
  justify-content: center;
}


.notification-icon svg {
  width: 22px;
  height: 20px;

  fill: none;
  stroke: currentColor;

  stroke-width: 1.5;

  stroke-linecap: round;
  stroke-linejoin: round;
}


.notification-message {
  min-width: 0;

  display: flex;
  flex-direction: column;
  gap: 3px;
}


.notification-message > strong {
  color: #3e596a;

  font-size: 11px;
  font-weight: 800;
}


.notification-message p {
  margin: 0;

  color: #647985;

  font-size: 9px;
  line-height: 1.4;
}


.notification-message p b {
  color: #315d79;

  font-size: 10px;
}


.old-price {
  margin-left: 4px;

  color: #9b9791;

  text-decoration: line-through;
}


.saving {
  color: #5d7a63;

  font-size: 9px;
  font-weight: 750;
}


.review-button {
  width: 100%;
  min-height: 38px;

  margin-top: 9px;

  border: 0;

  border-radius: 10px;

  background: #527fa4;

  color: #ffffff;

  display: flex;
  align-items: center;
  justify-content: center;

  gap: 5px;

  font-size: 10px;
  font-weight: 800;

  cursor: pointer;
}


.review-button svg {
  width: 14px;
  height: 14px;

  fill: none;
  stroke: currentColor;

  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}


.notification-enter-active,
.notification-leave-active {
  transition:
    opacity 0.4s ease,
    transform 0.4s ease;
}


.notification-enter-from,
.notification-leave-to {
  opacity: 0;

  transform:
    translate(-50%, -35px);
}


/* ================================================ */
/* HEADER */
/* ================================================ */

.header {
  position: relative;

  min-height: 40px;

  display: flex;
  align-items: center;

  margin-bottom: 22px;
}


.header h1 {
  width: 100%;

  margin: 0;

  padding: 0 35px;

  text-align: center;

  color: #242321;

  font-size: 18px;
  font-weight: 750;
}


.back-button {
  position: absolute;

  left: -7px;
  top: 50%;

  transform:
    translateY(-50%);

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


/* ================================================ */
/* GOAL CARD */
/* ================================================ */

.goal-card {
  padding: 17px;

  border:
    1px solid #e7e4df;

  border-radius: 16px;

  background: #ffffff;

  box-shadow:
    0 3px 12px
      rgba(30, 48, 60, 0.04);
}


.goal-top {
  display: flex;
  align-items: center;
  gap: 12px;
}


.laptop-icon {
  flex: 0 0 auto;

  width: 43px;
  height: 43px;

  border-radius: 11px;

  background: #f2f0eb;

  color: #698ba5;

  display: flex;
  align-items: center;
  justify-content: center;
}


.laptop-icon svg {
  width: 25px;
  height: 22px;

  fill: none;
  stroke: currentColor;

  stroke-width: 1.5;

  stroke-linecap: round;
  stroke-linejoin: round;
}


.goal-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}


.goal-title strong {
  color: #302f2c;

  font-size: 14px;
  font-weight: 750;
}


.goal-title span {
  color: #77736d;

  font-size: 11px;
  font-weight: 600;
}


/* ================================================ */
/* PROGRESS */
/* ================================================ */

.progress-summary {
  margin-top: 17px;

  display: flex;
  align-items: center;
  justify-content: space-between;
}


.progress-summary span {
  color: #8b8781;

  font-size: 9px;
  font-weight: 700;
}


.progress-summary strong {
  color: #527fa4;

  font-size: 11px;
  font-weight: 850;
}


.progress-track {
  width: 100%;
  height: 7px;

  margin-top: 6px;

  overflow: hidden;

  border-radius: 20px;

  background: #e9e7e2;
}


.progress-fill {
  height: 100%;

  border-radius: inherit;

  background: #5f88a7;

  transition:
    width 0.3s ease;
}


.goal-bottom {
  margin-top: 13px;

  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}


.goal-bottom > div {
  display: flex;
  flex-direction: column;
  gap: 3px;
}


.small-label {
  color: #99948e;

  font-size: 9px;
  font-weight: 650;
}


.goal-bottom strong {
  color: #4d4a46;

  font-size: 12px;
  font-weight: 750;
}


.status {
  padding: 6px 10px;

  border-radius: 20px;

  background: #edf3ee;

  color: #56715c;

  font-size: 9px;
  font-weight: 750;

  display: inline-flex;
  align-items: center;

  gap: 4px;
}


.status svg {
  width: 11px;
  height: 11px;

  fill: none;
  stroke: currentColor;

  stroke-width: 2.2;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* ================================================ */
/* MONEY */
/* ================================================ */

.money-section {
  margin-top: 27px;
}


.section-label {
  margin: 0 0 10px;

  color: #96918a;

  font-size: 10px;
  font-weight: 800;

  letter-spacing: 0.8px;
}


.money-card {
  overflow: hidden;

  border:
    1px solid #e5e3df;

  border-radius: 16px;

  background: #ffffff;
}


.money-row {
  min-height: 62px;

  padding: 10px 15px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 12px;
}


.money-left {
  display: flex;
  align-items: center;

  gap: 10px;
}


.money-left > span {
  color: #55514d;

  font-size: 12px;
  font-weight: 650;
}


.money-icon {
  flex: 0 0 auto;

  width: 31px;
  height: 31px;

  border-radius: 8px;

  background: #f2f4f5;

  color: #6d8799;

  display: flex;
  align-items: center;
  justify-content: center;
}


.money-icon svg {
  width: 17px;
  height: 17px;

  fill: none;
  stroke: currentColor;

  stroke-width: 1.6;

  stroke-linecap: round;
  stroke-linejoin: round;
}


.money-row > strong {
  color: #33312e;

  font-size: 12px;
  font-weight: 800;

  white-space: nowrap;
}


.money-row > strong.deduction {
  color: #69645e;
}


.divider {
  height: 1px;

  margin: 0 15px;

  background: #efede9;
}


/* ================================================ */
/* SAFE TO SPEND */
/* ================================================ */

.safe-row {
  min-height: 69px;

  padding: 12px 16px;

  background: #dcebf4;

  color: #315b7a;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 15px;
}


.safe-row > div {
  display: flex;
  flex-direction: column;

  gap: 3px;
}


.safe-row span {
  font-size: 13px;
  font-weight: 800;
}


.safe-row small {
  max-width: 220px;

  color: #668094;

  font-size: 9px;
  line-height: 1.35;
  font-weight: 600;
}


.safe-row strong {
  font-size: 18px;
  font-weight: 850;

  white-space: nowrap;
}


/* ================================================ */
/* INFO */
/* ================================================ */

.info-card {
  margin-top: 15px;

  padding: 13px 14px;

  border-radius: 13px;

  background: #f3f6f8;

  display: flex;
  align-items: flex-start;

  gap: 10px;
}


.info-icon {
  flex: 0 0 auto;

  width: 25px;
  height: 25px;

  color: #64839a;

  display: flex;
  align-items: center;
  justify-content: center;
}


.info-icon svg {
  width: 20px;
  height: 20px;

  fill: none;
  stroke: currentColor;

  stroke-width: 1.6;

  stroke-linecap: round;
  stroke-linejoin: round;
}


.info-text {
  display: flex;
  flex-direction: column;

  gap: 4px;
}


.info-text strong {
  color: #526875;

  font-size: 11px;
  font-weight: 750;
}


.info-text span {
  color: #71818a;

  font-size: 10px;
  line-height: 1.45;
}


/* ================================================ */
/* PLAN UPDATES */
/* ================================================ */

.plan-updates {
  width: 100%;
  min-height: 63px;

  margin-top: 12px;

  padding: 11px 13px;

  border:
    1px solid #dce7ed;

  border-radius: 13px;

  background: #ffffff;

  color: inherit;

  display: flex;
  align-items: center;

  gap: 10px;

  text-align: left;

  cursor: pointer;

  transition:
    background 0.2s ease,
    border-color 0.2s ease;
}


.plan-updates:hover {
  background: #f8fbfc;

  border-color: #cbdde7;
}


.plan-update-icon {
  flex: 0 0 auto;

  width: 34px;
  height: 34px;

  border-radius: 10px;

  background: #e8f1f6;

  color: #527c98;

  display: flex;
  align-items: center;
  justify-content: center;
}


.plan-update-icon svg {
  width: 18px;
  height: 18px;

  fill: none;
  stroke: currentColor;

  stroke-width: 1.7;

  stroke-linecap: round;
  stroke-linejoin: round;
}


.plan-update-text {
  min-width: 0;

  flex: 1;

  display: flex;
  flex-direction: column;

  gap: 3px;
}


.plan-update-text strong {
  color: #405d70;

  font-size: 11px;
  font-weight: 800;
}


.plan-update-text span {
  color: #81898e;

  font-size: 9px;
  line-height: 1.3;
}


.plan-update-arrow {
  flex: 0 0 auto;

  width: 17px;
  height: 17px;

  fill: none;
  stroke: #718b9b;

  stroke-width: 1.7;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* ================================================ */
/* MOBILE */
/* ================================================ */

@media (max-width: 380px) {

  .bank-app {
    padding-left: 20px;
    padding-right: 20px;
  }

}

</style>