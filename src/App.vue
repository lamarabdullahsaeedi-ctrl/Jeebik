<template>
  <div class="app-shell">

    <main class="app-content">
      <RouterView />
    </main>

    <!-- AI COMMITMENT POPUP -->
    <!-- يظهر فقط داخل صفحة Commitments وبعد 4 ثواني -->
    <div
      v-if="
        route.path === '/commitments' &&
        showCommitmentPopup &&
        pendingCommitment
      "
      class="ai-popup"
    >
      <div class="ai-popup-top">
        <div class="ai-popup-badge">
          JEEBIK AI
        </div>

        <button
          type="button"
          class="ai-popup-close"
          @click="closeCommitmentPopup"
        >
          ×
        </button>
      </div>

      <h3>
        Recurring commitment detected
      </h3>

      <p>
        JEEBIK AI noticed a recurring
        <strong>{{ pendingCommitment.name }}</strong>
        payment of
        <strong>
          SAR {{ formatNumber(pendingCommitment.amount) }}
        </strong>
        over the last
        <strong>
          {{ pendingCommitment.occurrences }} months
        </strong>.
      </p>

      <div class="ai-popup-details">
        <span>
          {{ pendingCommitment.frequency }}
        </span>

        <span>
          {{ pendingCommitment.confidence }} confidence
        </span>
      </div>

      <button
        type="button"
        class="ai-popup-review"
        @click="reviewCommitment"
      >
        Review
      </button>
    </div>


    <!-- BOTTOM NAVIGATION -->
    <nav class="bottom-nav">

      <RouterLink
        to="/"
        class="nav-item"
        :class="{ active: route.path === '/' }"
      >
        <svg
          class="nav-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M3 10.5L12 3l9 7.5" />
          <path d="M5 9.5V21h14V9.5" />
          <path d="M9 21v-6h6v6" />
        </svg>

        <span>Home</span>
      </RouterLink>


      <RouterLink
        to="/goals"
        class="nav-item"
        :class="{
          active:
            route.path === '/goals' ||
            route.path === '/goal-tracking' ||
            route.path === '/analysis' ||
            route.path === '/replanning'
        }"
      >
        <svg
          class="nav-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle cx="12" cy="12" r="8.5" />
          <circle cx="12" cy="12" r="5" />
          <circle cx="12" cy="12" r="1.5" />
        </svg>

        <span>Goals</span>
      </RouterLink>


      <RouterLink
        to="/commitments"
        class="nav-item"
        :class="{ active: route.path === '/commitments' }"
      >
        <svg
          class="nav-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <rect
            x="4"
            y="5.5"
            width="16"
            height="15"
            rx="2"
          />
          <path d="M8 3v5" />
          <path d="M16 3v5" />
          <path d="M4 10h16" />
          <path d="M8 14h3" />
          <path d="M13 14h3" />
          <path d="M8 17h3" />
        </svg>

        <span>Commitments</span>
      </RouterLink>


      <RouterLink
        to="/history"
        class="nav-item"
        :class="{ active: route.path === '/history' }"
      >
        <svg
          class="nav-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M3 12a9 9 0 1 0 3-6.7" />
          <path d="M3 4v5h5" />
          <path d="M12 7v5l3 2" />
        </svg>

        <span>History</span>
      </RouterLink>


      <button
        type="button"
        class="nav-item nav-button"
        :class="{ active: showNotifications }"
        @click="toggleNotifications"
      >
        <div class="notification-icon-wrap">

          <svg
            class="nav-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"
            />
            <path d="M10 21h4" />
          </svg>

          <span
            v-if="hasAnyNotification"
            class="notification-dot"
          ></span>

        </div>

        <span>Notifications</span>
      </button>

    </nav>


    <!-- NOTIFICATIONS -->
    <div
      v-if="showNotifications"
      class="notification-overlay"
      @click.self="showNotifications = false"
    >
      <div class="notification-panel">

        <div class="notification-header">

          <div>
            <p class="notification-eyebrow">
              JEEBIK
            </p>

            <h2>
              Notifications
            </h2>
          </div>

          <button
            type="button"
            class="close-button"
            @click="showNotifications = false"
          >
            ×
          </button>

        </div>


        <!-- COMMITMENT NOTIFICATION -->
        <div
          v-if="
            hasCommitmentNotification &&
            pendingCommitment
          "
          class="notification-card"
        >

          <div class="notification-card-top">

            <div class="notification-badge">
              AI
            </div>

            <span class="notification-time">
              Now
            </span>

          </div>

          <h3>
            New commitment detected
          </h3>

          <p>
            JEEBIK AI noticed a recurring
            <strong>
              {{ pendingCommitment.name }}
            </strong>
            payment of
            <strong>
              SAR {{ formatNumber(pendingCommitment.amount) }}
            </strong>
            over the last
            {{ pendingCommitment.occurrences }} months.
          </p>

          <div class="commitment-detection-info">

            <div>
              <span>Frequency</span>
              <strong>
                {{ pendingCommitment.frequency }}
              </strong>
            </div>

            <div>
              <span>Confidence</span>
              <strong class="capitalize">
                {{ pendingCommitment.confidence }}
              </strong>
            </div>

          </div>

          <div class="commitment-actions">

            <button
              type="button"
              class="reject-button"
              @click="rejectCommitment"
            >
              Not a Commitment
            </button>

            <button
              type="button"
              class="add-commitment-button"
              @click="acceptCommitment"
            >
              Add to Commitments
            </button>

          </div>

        </div>


        <!-- PRICE DROP -->
        <div
          v-if="hasPriceNotification"
          class="notification-card price-notification-card"
          @click="openReplanning"
        >

          <div class="notification-card-top">

            <div class="notification-badge">
              AI
            </div>

            <span class="notification-time">
              Now
            </span>

          </div>

          <h3>
            Price change detected
          </h3>

          <p>
            The price of your MacBook Pro 16&quot;
            dropped from SAR 10,499 to SAR 6,999.
            JEEBIK found new planning options for
            your goal.
          </p>

          <button
            type="button"
            class="review-button"
            @click.stop="openReplanning"
          >
            Review New Plan
          </button>

        </div>


        <div
          v-if="!hasAnyNotification"
          class="empty-notifications"
        >
          <div class="empty-bell">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.7"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"
              />
              <path d="M10 21h4" />
            </svg>
          </div>

          <h3>
            You're all caught up
          </h3>

          <p>
            JEEBIK will notify you when something
            important changes in your plan or
            financial activity.
          </p>
        </div>

      </div>
    </div>

  </div>
</template>


<script setup>
import {
  ref,
  computed,
  onMounted,
  onUnmounted,
  watch
} from 'vue'

import {
  useRouter,
  useRoute
} from 'vue-router'


const router = useRouter()
const route = useRoute()

const showNotifications = ref(false)
const showCommitmentPopup = ref(false)

const hasPriceNotification = ref(false)
const hasCommitmentNotification = ref(false)

const pendingCommitment = ref(null)

let notificationChecker = null
let commitmentDetectionStarted = false

// NEW:
// Timer for delayed commitment popup.
let commitmentPopupTimer = null


// ================================================
// DEMO TRANSACTION HISTORY
// ================================================

const transactionHistory = [
  {
    name: 'School Fees',
    amount: 1500,
    date: '2026-08-05',
    category: 'Education',
    type: 'expense'
  },
  {
    name: 'Coffee Shop',
    amount: 28,
    date: '2026-08-04',
    category: 'Food & Drinks',
    type: 'expense'
  },
  {
    name: 'School Fees',
    amount: 1500,
    date: '2026-09-05',
    category: 'Education',
    type: 'expense'
  },
  {
    name: 'Panda',
    amount: 420,
    date: '2026-09-04',
    category: 'Groceries',
    type: 'expense'
  },
  {
    name: 'School Fees',
    amount: 1500,
    date: '2026-10-05',
    category: 'Education',
    type: 'expense'
  },
  {
    name: 'Panda',
    amount: 310,
    date: '2026-10-03',
    category: 'Groceries',
    type: 'expense'
  }
]


const hasAnyNotification = computed(() => {
  return (
    hasPriceNotification.value ||
    hasCommitmentNotification.value
  )
})


function formatNumber(value) {
  return Number(value || 0).toLocaleString(
    'en-US'
  )
}


// ================================================
// PRICE NOTIFICATION
// ================================================

function checkPriceNotificationState() {

  const priceChange =
    sessionStorage.getItem(
      'jeebikPriceChange'
    )

  const replanAccepted =
    sessionStorage.getItem(
      'jeebikReplanAccepted'
    ) === 'true'

  hasPriceNotification.value =
    Boolean(priceChange) &&
    !replanAccepted
}


// ================================================
// COMMITMENT NOTIFICATION
// ================================================

function checkCommitmentNotificationState() {

  const savedCandidate =
    sessionStorage.getItem(
      'jeebikPendingCommitment'
    )

  const decision =
    sessionStorage.getItem(
      'jeebikCommitmentDecision'
    )

  if (
    savedCandidate &&
    decision !== 'accepted' &&
    decision !== 'rejected'
  ) {

    try {

      pendingCommitment.value =
        JSON.parse(savedCandidate)

      hasCommitmentNotification.value = true

    } catch (error) {

      console.error(
        'Could not read commitment:',
        error
      )

      pendingCommitment.value = null
      hasCommitmentNotification.value = false
    }

  } else {

    pendingCommitment.value = null
    hasCommitmentNotification.value = false
  }
}


// ================================================
// 4 SECOND POPUP DELAY
// ================================================

function clearCommitmentPopupTimer() {

  if (commitmentPopupTimer) {

    clearTimeout(
      commitmentPopupTimer
    )

    commitmentPopupTimer = null
  }
}


function scheduleCommitmentPopup() {

  clearCommitmentPopupTimer()

  showCommitmentPopup.value = false


  if (
    route.path !== '/commitments' ||
    !hasCommitmentNotification.value ||
    !pendingCommitment.value
  ) {
    return
  }


  commitmentPopupTimer =
    setTimeout(() => {

      // Check again after 4 seconds.
      // This prevents the popup from appearing
      // if the user already left Commitments
      // or already accepted/rejected it.
      checkCommitmentNotificationState()


      if (
        route.path === '/commitments' &&
        hasCommitmentNotification.value &&
        pendingCommitment.value
      ) {
        showCommitmentPopup.value = true
      }


      commitmentPopupTimer = null

    }, 4000)
}


// ================================================
// GEMINI DETECTION
// ================================================

async function detectRecurringCommitments() {

  if (commitmentDetectionStarted) {
    return
  }

  commitmentDetectionStarted = true


  const decision =
    sessionStorage.getItem(
      'jeebikCommitmentDecision'
    )

  const existingPending =
    sessionStorage.getItem(
      'jeebikPendingCommitment'
    )


  if (
    decision === 'accepted' ||
    decision === 'rejected'
  ) {
    return
  }


  if (existingPending) {

    checkCommitmentNotificationState()

    // If the app happens to open directly
    // on Commitments, still wait 4 seconds.
    if (
      route.path === '/commitments'
    ) {
      scheduleCommitmentPopup()
    }

    return
  }


  try {

    const response =
      await fetch(
        'http://127.0.0.1:8000/detect-commitments',
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            transactions: transactionHistory
          })
        }
      )


    if (!response.ok) {
      throw new Error(
        `Commitment detection failed: ${response.status}`
      )
    }


    const data =
      await response.json()


    console.log(
      'JEEBIK commitment detection:',
      data
    )


    if (
      data.status === 'success' &&
      data.detected === true &&
      data.pending_user_confirmation === true &&
      Array.isArray(data.candidates) &&
      data.candidates.length > 0
    ) {

      const candidate =
        data.candidates[0]


      pendingCommitment.value =
        candidate


      sessionStorage.setItem(
        'jeebikPendingCommitment',
        JSON.stringify(candidate)
      )


      sessionStorage.setItem(
        'jeebikCommitmentAIResult',
        JSON.stringify(
          data.ai_agent || {}
        )
      )


      hasCommitmentNotification.value =
        true


      // Only schedule the popup if the user
      // is currently inside Commitments.
      if (
        route.path === '/commitments'
      ) {
        scheduleCommitmentPopup()
      }
    }

  } catch (error) {

    console.error(
      'JEEBIK AI commitment detection error:',
      error
    )
  }
}


// ================================================
// ROUTE WATCH
// ================================================

watch(
  () => route.path,

  (newPath) => {

    clearCommitmentPopupTimer()

    showCommitmentPopup.value =
      false


    checkCommitmentNotificationState()


    if (
      newPath === '/commitments' &&
      hasCommitmentNotification.value &&
      pendingCommitment.value
    ) {

      // User entered Commitments:
      // wait exactly 4 seconds.
      scheduleCommitmentPopup()
    }
  }
)


// ================================================
// CHECK STATES
// ================================================

function checkNotificationState() {
  checkPriceNotificationState()
  checkCommitmentNotificationState()
}


// ================================================
// START
// ================================================

onMounted(() => {

  checkNotificationState()

  detectRecurringCommitments()


  // Direct opening / refresh on Commitments:
  // also wait 4 seconds.
  if (
    route.path === '/commitments' &&
    hasCommitmentNotification.value &&
    pendingCommitment.value
  ) {
    scheduleCommitmentPopup()
  }


  notificationChecker =
    setInterval(() => {
      checkNotificationState()
    }, 500)
})


// ================================================
// CLEANUP
// ================================================

onUnmounted(() => {

  if (notificationChecker) {

    clearInterval(
      notificationChecker
    )
  }


  clearCommitmentPopupTimer()
})


// ================================================
// NOTIFICATIONS
// ================================================

function toggleNotifications() {

  checkNotificationState()

  showNotifications.value =
    !showNotifications.value
}


// ================================================
// POPUP
// ================================================

function closeCommitmentPopup() {

  clearCommitmentPopupTimer()

  showCommitmentPopup.value =
    false
}


function reviewCommitment() {

  clearCommitmentPopupTimer()

  showCommitmentPopup.value =
    false

  showNotifications.value =
    true
}


// ================================================
// ACCEPT COMMITMENT
// ================================================

function acceptCommitment() {

  if (!pendingCommitment.value) {
    return
  }


  clearCommitmentPopupTimer()


  const confirmedCommitment = {

    ...pendingCommitment.value,

    source: 'AI Detected',

    confirmed: true,

    confirmed_at:
      new Date().toISOString()
  }


  sessionStorage.setItem(
    'jeebikConfirmedAICommitment',
    JSON.stringify(
      confirmedCommitment
    )
  )


  sessionStorage.setItem(
    'jeebikCommitmentDecision',
    'accepted'
  )


  sessionStorage.removeItem(
    'jeebikPendingCommitment'
  )


  hasCommitmentNotification.value =
    false

  pendingCommitment.value =
    null

  showCommitmentPopup.value =
    false

  showNotifications.value =
    false


  window.dispatchEvent(
    new CustomEvent(
      'jeebikCommitmentUpdated'
    )
  )


  if (
    route.path !== '/commitments'
  ) {
    router.push('/commitments')
  }
}


// ================================================
// REJECT COMMITMENT
// ================================================

function rejectCommitment() {

  clearCommitmentPopupTimer()


  sessionStorage.setItem(
    'jeebikCommitmentDecision',
    'rejected'
  )


  sessionStorage.removeItem(
    'jeebikPendingCommitment'
  )


  hasCommitmentNotification.value =
    false

  pendingCommitment.value =
    null

  showCommitmentPopup.value =
    false


  checkNotificationState()
}


// ================================================
// PRICE DROP
// ================================================

function openReplanning() {

  showNotifications.value =
    false

  router.push('/replanning')
}
</script>


<style scoped>
* {
  box-sizing: border-box;
}

.app-shell {
  min-height: 100vh;
}

.app-content {
  min-height: 100vh;
  padding-bottom: 68px;
}


/* POPUP */

.ai-popup {
  position: fixed;

  top: 18px;
  left: 50%;

  transform:
    translateX(-50%);

  width:
    calc(100% - 32px);

  max-width: 398px;

  padding: 16px;

  background:
    rgba(255, 255, 255, 0.98);

  border:
    1px solid #d8e4ed;

  border-radius: 17px;

  box-shadow:
    0 14px 38px
    rgba(31, 47, 61, 0.16);

  backdrop-filter:
    blur(12px);

  z-index: 12000;

  animation:
    popupDown 0.28s ease-out;
}


@keyframes popupDown {

  from {
    opacity: 0;

    transform:
      translate(-50%, -18px);
  }

  to {
    opacity: 1;

    transform:
      translate(-50%, 0);
  }
}


.ai-popup-top {
  display: flex;

  align-items: center;
  justify-content: space-between;

  margin-bottom: 10px;
}


.ai-popup-badge {
  padding:
    5px
    9px;

  border-radius: 20px;

  background: #355f82;

  color: white;

  font-size: 9px;
  font-weight: 800;

  letter-spacing: 0.6px;
}


.ai-popup-close {
  width: 27px;
  height: 27px;

  display: flex;

  align-items: center;
  justify-content: center;

  border: none;

  border-radius: 50%;

  background: #f2f1ee;

  color: #5e5a55;

  font-size: 18px;

  cursor: pointer;
}


.ai-popup h3 {
  margin:
    0
    0
    7px;

  color: #263d52;

  font-size: 15px;
  font-weight: 800;
}


.ai-popup p {
  margin: 0;

  color: #5d6d7b;

  font-size: 11.5px;

  line-height: 1.55;
}


.ai-popup p strong {
  color: #304e68;
}


.ai-popup-details {
  display: flex;

  gap: 7px;

  flex-wrap: wrap;

  margin-top: 11px;
}


.ai-popup-details span {
  padding:
    5px
    8px;

  border-radius: 20px;

  background: #eef3f7;

  color: #587086;

  font-size: 9px;
  font-weight: 700;

  text-transform: capitalize;
}


.ai-popup-review {
  width: 100%;

  margin-top: 12px;

  padding:
    10px
    12px;

  border: none;

  border-radius: 10px;

  background: #6289ad;

  color: white;

  font-family: inherit;

  font-size: 11px;
  font-weight: 800;

  cursor: pointer;
}


/* NAVIGATION */

.bottom-nav {
  position: fixed;

  left: 50%;
  bottom: 0;

  transform:
    translateX(-50%);

  width: 100%;
  max-width: 430px;

  height: 64px;

  background:
    rgba(255, 255, 255, 0.98);

  border-top:
    1px solid #e4e1dc;

  display: grid;

  grid-template-columns:
    repeat(5, 1fr);

  align-items: center;

  padding:
    4px
    3px
    5px;

  z-index: 9999;

  box-shadow:
    0 -4px 14px
    rgba(37, 53, 69, 0.05);

  backdrop-filter:
    blur(12px);
}


.nav-item {
  position: relative;

  width: 100%;
  height: 54px;

  display: flex;

  flex-direction: column;

  align-items: center;
  justify-content: center;

  gap: 2px;

  border: none;
  outline: none;

  background: transparent;

  color: #aaa69f;

  text-decoration: none;

  font-family: inherit;

  font-size: 8.5px;
  font-weight: 700;

  cursor: pointer;

  padding: 0;

  transition:
    color 0.2s ease;
}


.nav-item:hover {
  color: #5f84a8;
}


.nav-item.active {
  color: #355f82;
}


.nav-icon {
  width: 19px;
  height: 19px;

  flex-shrink: 0;
}


.nav-item.active .nav-icon {
  stroke-width: 2.1;
}


.nav-button {
  padding: 0;
}


/* NOTIFICATION DOT */

.notification-icon-wrap {
  position: relative;

  display: flex;

  align-items: center;
  justify-content: center;
}


.notification-dot {
  position: absolute;

  width: 7px;
  height: 7px;

  top: -2px;
  right: -4px;

  border-radius: 50%;

  background: #355f82;

  border:
    1.5px solid white;
}


/* NOTIFICATION OVERLAY */

.notification-overlay {
  position: fixed;

  inset: 0;

  background:
    rgba(30, 38, 47, 0.18);

  z-index: 10000;

  display: flex;

  justify-content: center;
  align-items: flex-end;
}


.notification-panel {
  width: 100%;
  max-width: 430px;

  max-height: 82vh;

  overflow-y: auto;

  background: #ffffff;

  border-radius:
    22px
    22px
    0
    0;

  padding:
    22px
    22px
    82px;

  box-shadow:
    0 -12px 40px
    rgba(30, 45, 60, 0.12);

  animation:
    slideUp 0.22s ease-out;
}


@keyframes slideUp {

  from {
    transform:
      translateY(35px);

    opacity: 0;
  }

  to {
    transform:
      translateY(0);

    opacity: 1;
  }
}


.notification-header {
  display: flex;

  align-items: flex-start;
  justify-content: space-between;

  margin-bottom: 18px;
}


.notification-eyebrow {
  margin:
    0
    0
    4px;

  color: #9c948a;

  font-size: 10px;
  font-weight: 800;

  letter-spacing: 1.4px;
}


.notification-header h2 {
  margin: 0;

  color: #1d1d1d;

  font-size: 22px;
  font-weight: 800;
}


.close-button {
  width: 32px;
  height: 32px;

  border: none;

  border-radius: 50%;

  background: #f3f1ed;

  color: #55514c;

  font-size: 22px;

  cursor: pointer;
}


/* NOTIFICATION CARD */

.notification-card {
  padding: 18px;

  background: #eaf2f7;

  border:
    1px solid #d7e4ed;

  border-radius: 17px;

  margin-bottom: 12px;
}


.price-notification-card {
  cursor: pointer;
}


.notification-card-top {
  display: flex;

  align-items: center;
  justify-content: space-between;

  margin-bottom: 12px;
}


.notification-badge {
  min-width: 36px;

  height: 25px;

  padding:
    0
    9px;

  display: inline-flex;

  align-items: center;
  justify-content: center;

  border-radius: 20px;

  background: #355f82;

  color: white;

  font-size: 10px;
  font-weight: 800;
}


.notification-time {
  color: #918a81;

  font-size: 10px;
}


.notification-card h3 {
  margin:
    0
    0
    7px;

  color: #263d52;

  font-size: 16px;
  font-weight: 800;
}


.notification-card p {
  margin: 0;

  color: #566879;

  font-size: 12px;

  line-height: 1.55;
}


.notification-card p strong {
  color: #304e68;
}


/* COMMITMENT INFO */

.commitment-detection-info {
  display: grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap: 8px;

  margin-top: 14px;
}


.commitment-detection-info div {
  padding: 10px;

  background:
    rgba(255, 255, 255, 0.58);

  border-radius: 10px;
}


.commitment-detection-info span {
  display: block;

  margin-bottom: 3px;

  color: #84909b;

  font-size: 9px;
}


.commitment-detection-info strong {
  color: #344f66;

  font-size: 11px;
}


.capitalize {
  text-transform: capitalize;
}


/* ACTIONS */

.commitment-actions {
  display: grid;

  grid-template-columns:
    1fr
    1.15fr;

  gap: 8px;

  margin-top: 15px;
}


.reject-button,
.add-commitment-button {
  min-height: 42px;

  padding:
    10px
    9px;

  border-radius: 11px;

  font-family: inherit;

  font-size: 10px;
  font-weight: 800;

  cursor: pointer;
}


.reject-button {
  border:
    1px solid #cbd6df;

  background: white;

  color: #607486;
}


.add-commitment-button {
  border: none;

  background: #6289ad;

  color: white;
}


.review-button {
  width: 100%;

  margin-top: 15px;

  padding:
    12px
    14px;

  border: none;

  border-radius: 11px;

  background: #6289ad;

  color: white;

  font-family: inherit;

  font-size: 12px;
  font-weight: 800;

  cursor: pointer;
}


/* EMPTY */

.empty-notifications {
  padding:
    28px
    18px
    14px;

  text-align: center;
}


.empty-bell {
  width: 50px;
  height: 50px;

  margin:
    0
    auto
    14px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #f2f4f5;

  color: #7690a5;
}


.empty-bell svg {
  width: 23px;
  height: 23px;
}


.empty-notifications h3 {
  margin:
    0
    0
    7px;

  color: #344d63;

  font-size: 16px;
  font-weight: 800;
}


.empty-notifications p {
  max-width: 300px;

  margin:
    0
    auto;

  color: #7c858c;

  font-size: 12px;

  line-height: 1.55;
}


/* MOBILE */

@media (max-width: 430px) {

  .bottom-nav {
    left: 0;

    transform: none;

    width: 100%;
    max-width: none;
  }


  .notification-panel {
    width: 100%;
    max-width: none;
  }


  .ai-popup {
    width:
      calc(100% - 28px);

    max-width: none;
  }
}


@media (max-width: 360px) {

  .nav-item {
    font-size: 8px;
  }


  .nav-icon {
    width: 18px;
    height: 18px;
  }


  .commitment-actions {
    grid-template-columns:
      1fr;
  }
}
</style>