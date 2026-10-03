<script setup>
import {
  ref,
  computed,
  onMounted
} from 'vue'

import { useRouter } from 'vue-router'

const router = useRouter()


// --------------------------------------------------
// HOME FINANCIAL STATE
// --------------------------------------------------

const monthlyCommitments = ref(3000)

const baseExistingGoalAllocation = ref(900)

const baseSafeToSpend = ref(7100)

const activePlan = ref(null)


// --------------------------------------------------
// LOAD ACTIVE JEEBIK PLAN
// --------------------------------------------------

function loadActivePlan() {

  const savedPlan =
    sessionStorage.getItem('jeebikCreatedPlan')

  if (!savedPlan) {
    activePlan.value = null
    return
  }

  try {

    activePlan.value =
      JSON.parse(savedPlan)

  } catch (error) {

    console.error(
      'Could not read active JEEBIK plan:',
      error
    )

    activePlan.value = null
  }
}


// --------------------------------------------------
// DYNAMIC HOME VALUES
// --------------------------------------------------

const allocatedToGoals = computed(() => {

  // No MacBook goal yet:
  // only the existing Mauritius goal is active.
  if (!activePlan.value) {
    return baseExistingGoalAllocation.value
  }

  const macBookAllocation =
    Number(
      activePlan.value.monthly_allocation || 0
    )

  const mauritiusAllocation =
    Number(
      activePlan.value
        .existing_goal_monthly_allocation ??
      baseExistingGoalAllocation.value
    )

  return (
    macBookAllocation +
    mauritiusAllocation
  )
})


const safeToSpend = computed(() => {

  // Original financial state before creating
  // the MacBook goal.
  if (!activePlan.value) {
    return baseSafeToSpend.value
  }

  return Number(
    activePlan.value.safe_to_spend ??
    baseSafeToSpend.value
  )
})


// --------------------------------------------------
// LIFECYCLE
// --------------------------------------------------

onMounted(() => {
  loadActivePlan()
})


// --------------------------------------------------
// HELPERS
// --------------------------------------------------

function formatSAR(value) {
  return `SAR ${Number(
    value || 0
  ).toLocaleString()}`
}


// --------------------------------------------------
// DEMO RESET
// --------------------------------------------------

function resetDemo() {

  // ------------------------------------------------
  // RESET GOAL / PRICE-DROP DEMO
  // ------------------------------------------------

  sessionStorage.removeItem(
    'jeebikCreatedPlan'
  )

  sessionStorage.removeItem(
    'jeebikPriceChange'
  )

  sessionStorage.removeItem(
    'jeebikReplanAccepted'
  )


  // ------------------------------------------------
  // RESET AI COMMITMENT DETECTION DEMO
  // ------------------------------------------------
  //
  // This allows Gemini to analyze the transaction
  // history again and recreate the proactive
  // commitment-detection flow from the beginning.
  //

  sessionStorage.removeItem(
    'jeebikPendingCommitment'
  )

  sessionStorage.removeItem(
    'jeebikCommitmentDecision'
  )

  sessionStorage.removeItem(
    'jeebikConfirmedAICommitment'
  )

  sessionStorage.removeItem(
    'jeebikCommitmentAIResult'
  )


  // ------------------------------------------------
  // UPDATE HOME IMMEDIATELY
  // ------------------------------------------------

  activePlan.value = null


  console.log(
    'JEEBIK full demo reset successfully.'
  )


  // ------------------------------------------------
  // RELOAD APP
  // ------------------------------------------------
  //
  // App.vue starts a new commitment-detection cycle
  // when the application loads.
  //
  // Reloading after the reset makes the demo behave
  // like a completely fresh user session.
  //

  window.location.reload()
}


// --------------------------------------------------
// NAVIGATION
// --------------------------------------------------

function exploreGoals() {
  router.push('/goals')
}


function openCommitments() {
  router.push('/commitments')
}
</script>


<template>

  <div class="page">

    <main class="bank-app">


      <!-- =========================================== -->
      <!-- TOP BAR -->
      <!-- =========================================== -->

      <header class="top-bar">

        <div class="bank-name">
          MY BANK
        </div>


        <div class="top-actions">

          <span
            class="bell"
            aria-label="Notifications"
          >

            <svg
              viewBox="0 0 24 24"
              aria-hidden="true"
            >

              <path
                d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
              />

              <path
                d="M13.73 21a2 2 0 0 1-3.46 0"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
              />

            </svg>

          </span>


          <div class="profile">
            L
          </div>

        </div>

      </header>


      <!-- =========================================== -->
      <!-- GREETING -->
      <!-- =========================================== -->

      <p class="greeting">
        Good evening, Lamar
      </p>


      <!-- =========================================== -->
      <!-- BALANCE -->
      <!-- =========================================== -->

      <section class="balance-section">

        <p class="label">
          Current Balance
        </p>

        <h1>
          SAR 10,000
        </h1>

        <p class="account-number">
          •••• 4821
        </p>

      </section>


      <!-- =========================================== -->
      <!-- QUICK ACTIONS -->
      <!-- =========================================== -->

      <section class="quick-actions">


        <div class="quick-action">

          <div class="action-icon">

            <span class="transfer-icon">
              ↗
            </span>

          </div>

          <span>
            Transfer
          </span>

        </div>


        <div class="quick-action">

          <div class="action-icon">

            <span class="receipt-icon">
              ▤
            </span>

          </div>

          <span>
            Pay
          </span>

        </div>


        <div class="quick-action">

          <div class="action-icon cards-icon">

            <span class="card-back"></span>

            <span class="card-front"></span>

          </div>

          <span>
            Cards
          </span>

        </div>


        <div class="quick-action">

          <div class="action-icon">

            <span class="more-icon">
              •••
            </span>

          </div>

          <span>
            More
          </span>

        </div>


      </section>


      <!-- =========================================== -->
      <!-- JEEBIK CARD -->
      <!-- =========================================== -->

      <section class="jeebik-card">


        <div class="jeebik-header">


          <div class="jeebik-brand">


            <div class="jeebik-logo-wrapper">

              <img
                src="/jeebik-logo.png"
                alt="JEEBIK Logo"
                class="jeebik-logo-image"
              />

            </div>


            <strong>
              JEEBIK
            </strong>

          </div>


          <div class="ai-badge">
            AI
          </div>

        </div>


        <p class="jeebik-message">
          Plan your goals around what you can safely spend.
        </p>


        <div class="divider"></div>


        <!-- ========================================= -->
        <!-- FINANCIAL SUMMARY -->
        <!-- ========================================= -->

        <div class="financial-summary">


          <!-- COMMITMENTS -->

          <div class="summary-item">

            <span>
              MONTHLY<br />
              COMMITMENTS
            </span>

            <strong>
              {{ formatSAR(monthlyCommitments) }}
            </strong>

          </div>


          <!-- GOALS -->

          <div class="summary-item">

            <span>
              ALLOCATED TO GOALS
            </span>

            <strong>
              {{ formatSAR(allocatedToGoals) }}
            </strong>

          </div>


          <!-- SAFE TO SPEND -->

          <div class="summary-item">

            <span>
              SAFE TO SPEND
            </span>

            <strong class="safe">
              {{ formatSAR(safeToSpend) }}
            </strong>

          </div>


        </div>


        <!-- ========================================= -->
        <!-- BUTTONS -->
        <!-- ========================================= -->

        <div class="jeebik-buttons">


          <button
            type="button"
            class="secondary-button"
            @click="openCommitments"
          >
            My Commitments
          </button>


          <button
            type="button"
            class="primary-button"
            @click="exploreGoals"
          >
            Explore Goals
          </button>


        </div>


      </section>


      <!-- =========================================== -->
      <!-- RECENT ACTIVITY -->
      <!-- =========================================== -->

      <section class="recent-activity">


        <h2>
          Recent Activity
        </h2>


        <div class="activity-row">

          <div>

            <strong>
              Grocery — Panda
            </strong>

            <span>
              Today
            </span>

          </div>


          <strong>
            -SAR 210
          </strong>

        </div>


        <div class="activity-row">

          <div>

            <strong>
              Salary
            </strong>

            <span>
              Sep 1
            </span>

          </div>


          <strong class="income">
            +SAR 15,000
          </strong>

        </div>


      </section>


      <!-- =========================================== -->
      <!-- DEMO RESET -->
      <!-- =========================================== -->

      <div class="demo-tools">

        <button
          type="button"
          class="reset-demo-button"
          @click="resetDemo"
        >
          Reset Demo
        </button>

      </div>


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

  padding: 0;

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
    50px;
}


/* ================================================ */
/* TOP BAR */
/* ================================================ */

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 24px;
}


.bank-name {
  color: #a5a29c;

  font-size: 14px;
  font-weight: 800;

  letter-spacing: 1.6px;
}


.top-actions {
  display: flex;
  align-items: center;

  gap: 14px;
}


/* Notification Bell */

.bell {
  width: 22px;
  height: 22px;

  color: #77746e;

  display: flex;
  align-items: center;
  justify-content: center;
}


.bell svg {
  width: 20px;
  height: 20px;

  display: block;
}


.profile {
  width: 30px;
  height: 30px;

  border-radius: 50%;

  background: #f1efeb;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 12px;

  color: #55524d;
}


/* ================================================ */
/* GREETING */
/* ================================================ */

.greeting {
  color: #65625d;

  font-size: 14px;

  margin: 0 0 18px;
}


/* ================================================ */
/* BALANCE */
/* ================================================ */

.balance-section {
  margin-bottom: 18px;
}


.label {
  color: #696660;

  font-size: 14px;

  margin: 0 0 8px;
}


.balance-section h1 {
  font-size: 34px;

  line-height: 1;

  margin: 0;

  font-weight: 800;

  letter-spacing: -1px;
}


.account-number {
  margin: 14px 0 0;

  color: #a5a19a;

  font-size: 13px;

  letter-spacing: 1px;
}


/* ================================================ */
/* QUICK ACTIONS */
/* ================================================ */

.quick-actions {
  display: grid;

  grid-template-columns:
    repeat(4, 1fr);

  gap: 16px;

  margin:
    18px
    0
    16px;
}


.quick-action {
  display: flex;
  flex-direction: column;
  align-items: center;

  gap: 6px;

  color: #4c4945;

  font-size: 11px;
}


.action-icon {
  position: relative;

  width: 56px;
  height: 48px;

  border-radius: 14px;

  background: #f1f0ed;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #5682a6;
}


.transfer-icon {
  font-size: 27px;

  line-height: 1;
}


.receipt-icon {
  font-size: 25px;
}


.more-icon {
  font-size: 22px;

  letter-spacing: 2px;

  transform:
    translateY(-3px);
}


/* Cards */

.cards-icon {
  position: relative;
}


.card-back,
.card-front {
  position: absolute;

  width: 25px;
  height: 18px;

  border:
    2px solid #5682a6;

  border-radius: 4px;
}


.card-back {
  transform:
    translate(-3px, -3px);

  opacity: 0.7;
}


.card-front {
  transform:
    translate(3px, 2px);
}


/* ================================================ */
/* JEEBIK CARD */
/* ================================================ */

.jeebik-card {
  background: #e5eff6;

  border-radius: 22px;

  padding: 20px;

  margin-top: 12px;
}


.jeebik-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}


.jeebik-brand {
  display: flex;
  align-items: center;

  gap: 13px;

  color: #294f6d;
}


/* Logo area stays controlled */

.jeebik-logo-wrapper {
  width: 52px;
  height: 52px;

  display: flex;
  align-items: center;
  justify-content: center;

  overflow: visible;
}


/* Make the wallet itself visually larger */

.jeebik-logo-image {
  width: 52px;
  height: 52px;

  object-fit: contain;
  object-position: center;

  display: block;

  transform: scale(1.35);

  transform-origin: center;
}


/* Slightly larger JEEBIK text */

.jeebik-brand strong {
  font-size: 18px;

  line-height: 1;

  font-weight: 800;

  letter-spacing: 0.2px;
}


/* AI stays the same size */

.ai-badge {
  min-width: 32px;

  height: 23px;

  padding: 0 9px;

  border-radius: 20px;

  background: #2f5876;

  color: #ffffff;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 10px;

  font-weight: 800;
}


.jeebik-message {
  margin:
    17px
    0
    31px;

  color: #315673;

  font-size: 13px;

  line-height: 1.5;
}


.divider {
  height: 1px;

  background: #abc1d1;

  margin-bottom: 15px;
}


/* ================================================ */
/* FINANCIAL SUMMARY */
/* ================================================ */

.financial-summary {
  display: grid;

  grid-template-columns:
    1fr 1.15fr 1fr;

  gap: 10px;
}


.summary-item {
  min-width: 0;
}


.summary-item span {
  display: block;

  min-height: 34px;

  color: #315673;

  font-size: 10px;

  line-height: 1.35;

  font-weight: 800;

  letter-spacing: 0.15px;
}


.summary-item strong {
  display: block;

  margin-top: 3px;

  font-size: 14px;

  white-space: nowrap;
}


.summary-item .safe {
  color: #315673;
}


/* ================================================ */
/* BUTTONS */
/* ================================================ */

.jeebik-buttons {
  display: grid;

  grid-template-columns:
    1fr 1fr;

  gap: 10px;

  margin-top: 17px;
}


.jeebik-buttons button {
  height: 47px;

  border-radius: 12px;

  font-size: 12px;

  font-weight: 700;

  cursor: pointer;

  transition:
    transform 0.15s ease,
    opacity 0.15s ease;
}


.jeebik-buttons button:active {
  transform: scale(0.98);
}


.secondary-button {
  border:
    2px solid #4f7ea4;

  background: transparent;

  color: #294f6d;
}


.primary-button {
  border:
    2px solid #527fa4;

  background: #527fa4;

  color: #ffffff;
}


/* ================================================ */
/* RECENT ACTIVITY */
/* ================================================ */

.recent-activity {
  margin-top: 19px;
}


.recent-activity h2 {
  font-size: 13px;

  margin:
    0
    0
    14px;
}


.activity-row {
  border-top:
    1px solid #dedbd5;

  padding:
    13px
    0;

  display: flex;

  justify-content:
    space-between;

  align-items:
    flex-start;

  font-size: 12px;
}


.activity-row > div {
  display: flex;

  flex-direction: column;

  gap: 8px;
}


.activity-row span {
  color: #aaa69f;

  font-size: 10px;
}


.activity-row > strong {
  font-size: 12px;
}


.activity-row .income {
  color: #315673;
}


/* ================================================ */
/* DEMO TOOLS */
/* ================================================ */

.demo-tools {
  margin-top: 24px;

  display: flex;
  justify-content: center;
}


.reset-demo-button {
  padding:
    7px
    12px;

  border:
    1px solid #dedbd5;

  border-radius: 8px;

  background: transparent;

  color: #aaa69f;

  font-size: 9px;
  font-weight: 650;

  cursor: pointer;

  transition:
    color 0.2s ease,
    border-color 0.2s ease,
    background 0.2s ease;
}


.reset-demo-button:hover {
  color: #66625d;

  border-color: #c8c4bd;

  background: #faf9f7;
}


/* ================================================ */
/* MOBILE */
/* ================================================ */

@media (max-width: 380px) {

  .bank-app {
    padding-left: 20px;
    padding-right: 20px;
  }


  .quick-actions {
    gap: 8px;
  }


  .action-icon {
    width: 50px;
  }


  .jeebik-card {
    padding: 17px;
  }


  .summary-item strong {
    font-size: 12px;
  }

}

</style>