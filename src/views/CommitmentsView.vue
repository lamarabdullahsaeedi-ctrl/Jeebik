<script setup>
import {
  ref,
  computed,
  onMounted,
  onUnmounted
} from 'vue'

import {
  useRouter
} from 'vue-router'


const router = useRouter()

const activeTab = ref('ai')

const showForm = ref(false)
const editingSource = ref(null)
const editingId = ref(null)

const form = ref({
  name: '',
  amount: '',
  frequency: 'Monthly'
})


// ================================================
// DEFAULT AI COMMITMENTS
// ================================================

const aiCommitments = ref([
  {
    id: 1,
    name: 'Electricity',
    amount: 350,
    frequency: 'Monthly',
    detail:
      'Detected from recurring transactions',
    icon: '⚡'
  },
  {
    id: 2,
    name: 'Subscriptions',
    amount: 250,
    frequency: 'Monthly',
    detail:
      'Detected from recurring transactions',
    icon: '↻'
  }
])


// ================================================
// DEFAULT MANUAL COMMITMENTS
// ================================================

const manualCommitments = ref([
  {
    id: 1,
    name: 'Car Insurance',
    amount: 900,
    frequency: 'Monthly',
    icon: '◇'
  },
  {
    id: 2,
    name: 'School Fees',
    amount: 1500,
    frequency: 'Monthly',
    icon: '🎓'
  }
])


// ================================================
// LOAD CONFIRMED GEMINI COMMITMENT
// ================================================

function loadConfirmedAICommitment() {

  const saved =
    sessionStorage.getItem(
      'jeebikConfirmedAICommitment'
    )


  if (!saved) {
    return
  }


  try {

    const confirmed =
      JSON.parse(saved)


    if (!confirmed?.name) {
      return
    }


    const confirmedName =
      String(
        confirmed.name
      )
        .trim()
        .toLowerCase()


    // --------------------------------------------
    // REMOVE SAME COMMITMENT FROM MANUAL
    // --------------------------------------------

    manualCommitments.value =
      manualCommitments.value.filter(
        item =>
          String(item.name)
            .trim()
            .toLowerCase() !==
          confirmedName
      )


    // --------------------------------------------
    // CHECK IF ALREADY IN AI
    // --------------------------------------------

    const existingAI =
      aiCommitments.value.find(
        item =>
          String(item.name)
            .trim()
            .toLowerCase() ===
          confirmedName
      )


    if (existingAI) {

      existingAI.amount =
        Number(
          confirmed.amount || 0
        )

      existingAI.frequency =
        confirmed.frequency ||
        'Monthly'

      existingAI.detail =
        confirmed.occurrences
          ? `Detected across ${confirmed.occurrences} recurring transactions`
          : 'Detected from recurring transactions'

    } else {

      aiCommitments.value.push({
        id:
          `confirmed-${confirmedName}`,

        name:
          confirmed.name,

        amount:
          Number(
            confirmed.amount || 0
          ),

        frequency:
          confirmed.frequency ||
          'Monthly',

        detail:
          confirmed.occurrences
            ? `Detected across ${confirmed.occurrences} recurring transactions`
            : 'Detected from recurring transactions',

        icon:
          confirmed.category ===
          'Education'
            ? '🎓'
            : '✦'
      })
    }


    // Show the AI tab immediately after approval.
    activeTab.value = 'ai'


  } catch (error) {

    console.error(
      'Could not load confirmed AI commitment:',
      error
    )
  }
}


// ================================================
// LIVE UPDATE EVENT
// ================================================

function handleCommitmentUpdate() {

  loadConfirmedAICommitment()
}


// ================================================
// LIFECYCLE
// ================================================

onMounted(() => {

  loadConfirmedAICommitment()

  window.addEventListener(
    'jeebikCommitmentUpdated',
    handleCommitmentUpdate
  )
})


onUnmounted(() => {

  window.removeEventListener(
    'jeebikCommitmentUpdated',
    handleCommitmentUpdate
  )
})


// ================================================
// TOTAL
// ================================================

const totalCommitments =
  computed(() => {

    const aiTotal =
      aiCommitments.value.reduce(
        (sum, item) =>
          sum +
          Number(
            item.amount || 0
          ),
        0
      )


    const manualTotal =
      manualCommitments.value.reduce(
        (sum, item) =>
          sum +
          Number(
            item.amount || 0
          ),
        0
      )


    return (
      aiTotal +
      manualTotal
    )
  })


// ================================================
// NAVIGATION
// ================================================

function goBack() {
  router.push('/')
}


// ================================================
// HELPERS
// ================================================

function formatSAR(value) {

  return Number(
    value || 0
  ).toLocaleString(
    'en-US'
  )
}


function switchTab(tab) {

  activeTab.value = tab

  closeForm()
}


// ================================================
// ADD MANUAL
// ================================================

function openAddForm() {

  editingSource.value =
    'manual'

  editingId.value =
    null


  form.value = {
    name: '',
    amount: '',
    frequency: 'Monthly'
  }


  showForm.value =
    true
}


// ================================================
// EDIT
// ================================================

function openEditForm(
  item,
  source
) {

  editingSource.value =
    source

  editingId.value =
    item.id


  form.value = {
    name:
      item.name,

    amount:
      item.amount,

    frequency:
      item.frequency
  }


  showForm.value =
    true
}


// ================================================
// CLOSE FORM
// ================================================

function closeForm() {

  showForm.value =
    false

  editingSource.value =
    null

  editingId.value =
    null


  form.value = {
    name: '',
    amount: '',
    frequency: 'Monthly'
  }
}


// ================================================
// SAVE
// ================================================

function saveCommitment() {

  const cleanName =
    String(
      form.value.name || ''
    ).trim()


  const cleanAmount =
    Number(
      form.value.amount || 0
    )


  if (
    !cleanName ||
    cleanAmount <= 0
  ) {
    return
  }


  // ADD NEW MANUAL
  if (
    editingSource.value ===
      'manual' &&
    editingId.value === null
  ) {

    manualCommitments.value.push({
      id:
        Date.now(),

      name:
        cleanName,

      amount:
        cleanAmount,

      frequency:
        form.value.frequency,

      icon:
        '○'
    })


    closeForm()

    return
  }


  // EDIT EXISTING
  const list =
    editingSource.value === 'ai'
      ? aiCommitments.value
      : manualCommitments.value


  const item =
    list.find(
      commitment =>
        commitment.id ===
        editingId.value
    )


  if (item) {

    const oldName =
      item.name


    item.name =
      cleanName

    item.amount =
      cleanAmount

    item.frequency =
      form.value.frequency


    // If editing confirmed Gemini commitment,
    // update sessionStorage too.
    if (
      editingSource.value ===
      'ai'
    ) {

      const saved =
        sessionStorage.getItem(
          'jeebikConfirmedAICommitment'
        )


      if (saved) {

        try {

          const confirmed =
            JSON.parse(saved)


          if (
            String(
              confirmed.name
            )
              .trim()
              .toLowerCase() ===
            String(
              oldName
            )
              .trim()
              .toLowerCase()
          ) {

            sessionStorage.setItem(
              'jeebikConfirmedAICommitment',

              JSON.stringify({
                ...confirmed,

                name:
                  cleanName,

                amount:
                  cleanAmount,

                frequency:
                  form.value.frequency
              })
            )
          }

        } catch (error) {

          console.error(
            'Could not update confirmed commitment:',
            error
          )
        }
      }
    }
  }


  closeForm()
}


// ================================================
// DELETE
// ================================================

function deleteCommitment() {

  if (
    editingId.value === null
  ) {
    return
  }


  if (
    editingSource.value === 'ai'
  ) {

    const deleting =
      aiCommitments.value.find(
        item =>
          item.id ===
          editingId.value
      )


    aiCommitments.value =
      aiCommitments.value.filter(
        item =>
          item.id !==
          editingId.value
      )


    if (deleting) {

      const saved =
        sessionStorage.getItem(
          'jeebikConfirmedAICommitment'
        )


      if (saved) {

        try {

          const confirmed =
            JSON.parse(saved)


          if (
            String(
              confirmed.name
            )
              .trim()
              .toLowerCase() ===
            String(
              deleting.name
            )
              .trim()
              .toLowerCase()
          ) {

            sessionStorage.removeItem(
              'jeebikConfirmedAICommitment'
            )
          }

        } catch (error) {

          console.error(
            'Could not delete saved commitment:',
            error
          )
        }
      }
    }

  } else {

    manualCommitments.value =
      manualCommitments.value.filter(
        item =>
          item.id !==
          editingId.value
      )
  }


  closeForm()
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
          <svg
            viewBox="0 0 24 24"
          >
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
          My Commitments
        </h1>

      </header>


      <!-- SUMMARY -->
      <section class="month-summary">

        <div>

          <span>
            Confirmed This Month
          </span>

          <small>
            Used in your financial plan
          </small>

        </div>

        <strong>
          SAR {{ formatSAR(totalCommitments) }}
        </strong>

      </section>


      <!-- TABS -->
      <section class="tabs">

        <button
          type="button"
          class="tab-button"
          :class="{
            active:
              activeTab === 'ai'
          }"
          @click="switchTab('ai')"
        >
          AI Detected

          <span class="tab-count">
            {{ aiCommitments.length }}
          </span>
        </button>


        <button
          type="button"
          class="tab-button"
          :class="{
            active:
              activeTab === 'manual'
          }"
          @click="switchTab('manual')"
        >
          Manual

          <span class="tab-count">
            {{ manualCommitments.length }}
          </span>
        </button>

      </section>


      <!-- AI DETECTED -->
      <section
        v-if="
          activeTab === 'ai'
        "
        class="tab-content"
      >

        <div class="ai-explanation">

          <div class="ai-label">
            JEEBIK AI
          </div>

          <div>

            <strong>
              Detected from your banking activity
            </strong>

            <p>
              JEEBIK identifies recurring transaction
              patterns and suggests potential commitments.
              Only confirmed commitments are used in your
              financial plan.
            </p>

          </div>

        </div>


        <div
          v-if="
            aiCommitments.length
          "
          class="commitments-list"
        >

          <div
            v-for="
              item in aiCommitments
            "
            :key="item.id"
            class="commitment-row"
          >

            <div class="commitment-left">

              <div
                class="commitment-icon blue-icon"
              >
                {{ item.icon }}
              </div>


              <div class="commitment-info">

                <div class="title-line">

                  <strong>
                    {{ item.name }}
                  </strong>

                  <span
                    class="badge ai-badge"
                  >
                    AI DETECTED
                  </span>

                </div>


                <span class="due-date">
                  {{ item.frequency }}
                  · Confirmed
                </span>


                <span
                  class="detected-detail"
                >
                  {{ item.detail }}
                </span>

              </div>

            </div>


            <div class="commitment-actions">

              <strong class="amount">
                SAR
                {{ formatSAR(item.amount) }}
              </strong>

              <button
                type="button"
                class="edit-button"
                @click="
                  openEditForm(
                    item,
                    'ai'
                  )
                "
              >
                Edit
              </button>

            </div>

          </div>

        </div>


        <div
          v-else
          class="empty-state"
        >
          <strong>
            No AI-detected commitments
          </strong>

          <p>
            JEEBIK will suggest commitments when it
            identifies meaningful recurring patterns.
          </p>
        </div>

      </section>


      <!-- MANUAL -->
      <section
        v-else
        class="tab-content"
      >

        <div class="manual-explanation">

          <strong>
            Manually added commitments
          </strong>

          <p>
            Add commitments that may not be visible
            from your banking transaction patterns.
          </p>

        </div>


        <div class="commitments-list">

          <div
            v-for="
              item in manualCommitments
            "
            :key="item.id"
            class="commitment-row"
          >

            <div class="commitment-left">

              <div
                class="commitment-icon beige-icon"
              >
                {{ item.icon }}
              </div>


              <div class="commitment-info">

                <div class="title-line">

                  <strong>
                    {{ item.name }}
                  </strong>

                  <span
                    class="badge manual-badge"
                  >
                    MANUAL
                  </span>

                </div>

                <span class="due-date">
                  {{ item.frequency }}
                </span>

              </div>

            </div>


            <div class="commitment-actions">

              <strong class="amount">
                SAR
                {{ formatSAR(item.amount) }}
              </strong>

              <button
                type="button"
                class="edit-button"
                @click="
                  openEditForm(
                    item,
                    'manual'
                  )
                "
              >
                Edit
              </button>

            </div>

          </div>

        </div>


        <button
          type="button"
          class="add-commitment"
          @click="openAddForm"
        >
          <span>+</span>

          Add Commitment
        </button>

      </section>


      <!-- FORM -->
      <div
        v-if="showForm"
        class="modal-overlay"
        @click.self="closeForm"
      >

        <section class="form-panel">

          <div class="form-header">

            <div>

              <p class="form-eyebrow">
                JEEBIK
              </p>

              <h2>
                {{
                  editingId === null
                    ? 'Add Commitment'
                    : 'Edit Commitment'
                }}
              </h2>

            </div>


            <button
              type="button"
              class="close-button"
              @click="closeForm"
            >
              ×
            </button>

          </div>


          <label class="field">

            <span>
              Commitment Name
            </span>

            <input
              v-model="form.name"
              type="text"
              placeholder="e.g. Internet Bill"
            />

          </label>


          <label class="field">

            <span>
              Amount
            </span>

            <div class="amount-input">

              <span>
                SAR
              </span>

              <input
                v-model="form.amount"
                type="number"
                min="1"
                placeholder="0"
              />

            </div>

          </label>


          <label class="field">

            <span>
              Frequency
            </span>

            <select
              v-model="
                form.frequency
              "
            >
              <option>
                Monthly
              </option>

              <option>
                Quarterly
              </option>

              <option>
                Yearly
              </option>

              <option>
                One-time
              </option>
            </select>

          </label>


          <div class="form-actions">

            <button
              v-if="
                editingId !== null
              "
              type="button"
              class="delete-button"
              @click="deleteCommitment"
            >
              Delete
            </button>


            <button
              type="button"
              class="save-button"
              @click="saveCommitment"
            >
              {{
                editingId === null
                  ? 'Add Commitment'
                  : 'Save Changes'
              }}
            </button>

          </div>


          <p
            v-if="
              editingSource === 'ai'
            "
            class="ai-edit-note"
          >
            You remain in control. Editing or deleting
            an AI-detected commitment updates what
            JEEBIK considers in your financial plan.
          </p>

        </section>

      </div>

    </main>

  </div>
</template>


<style scoped>
* {
  box-sizing: border-box;
}

button,
input,
select {
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
    30px
    26px
    110px;
}


/* HEADER */

.header {
  position: relative;

  display: flex;

  align-items: center;

  min-height: 38px;

  margin-bottom: 28px;
}


.header h1 {
  width: 100%;

  margin: 0;

  text-align: center;

  font-size: 20px;

  line-height: 1.2;

  font-weight: 750;

  color: #242321;
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


/* SUMMARY */

.month-summary {
  display: flex;

  justify-content: space-between;

  align-items: center;

  gap: 16px;

  padding-bottom: 18px;

  border-bottom:
    1px solid #e0ddd8;
}


.month-summary span {
  display: block;

  font-size: 13px;

  color: #77736d;
}


.month-summary small {
  display: block;

  margin-top: 4px;

  color: #aaa59e;

  font-size: 9px;
}


.month-summary strong {
  flex-shrink: 0;

  font-size: 16px;

  font-weight: 750;

  color: #252422;
}


/* TABS */

.tabs {
  display: grid;

  grid-template-columns:
    1fr
    1fr;

  gap: 6px;

  margin-top: 22px;

  padding: 4px;

  border-radius: 13px;

  background: #f3f4f5;
}


.tab-button {
  height: 40px;

  border: none;

  border-radius: 10px;

  background: transparent;

  color: #85817b;

  font-size: 11px;

  font-weight: 750;

  cursor: pointer;
}


.tab-button.active {
  background: #ffffff;

  color: #355f82;

  box-shadow:
    0 2px 8px
    rgba(39, 54, 68, 0.08);
}


.tab-count {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  min-width: 18px;

  height: 18px;

  margin-left: 4px;

  padding:
    0
    5px;

  border-radius: 20px;

  background: #e6ebef;

  font-size: 8px;
}


/* CONTENT */

.tab-content {
  margin-top: 20px;
}


.ai-explanation,
.manual-explanation {
  margin-bottom: 12px;

  padding: 14px;

  border-radius: 14px;
}


.ai-explanation {
  display: flex;

  align-items: flex-start;

  gap: 10px;

  background: #f3f7fa;

  border:
    1px solid #dde9f1;
}


.manual-explanation {
  background: #f8f7f4;
}


.ai-label {
  flex-shrink: 0;

  padding:
    5px
    7px;

  border-radius: 7px;

  background: #355f82;

  color: #ffffff;

  font-size: 8px;

  font-weight: 800;

  letter-spacing: 0.4px;
}


.ai-explanation strong,
.manual-explanation strong {
  display: block;

  margin-bottom: 4px;

  color: #2b3e4e;

  font-size: 11px;
}


.ai-explanation p,
.manual-explanation p {
  margin: 0;

  color: #78828b;

  font-size: 9.5px;

  line-height: 1.5;
}


/* COMMITMENTS */

.commitments-list {
  width: 100%;
}


.commitment-row {
  min-height: 91px;

  display: flex;

  justify-content: space-between;

  align-items: center;

  gap: 10px;

  border-bottom:
    1px solid #e7e4df;
}


.commitment-left {
  min-width: 0;

  display: flex;

  align-items: center;

  gap: 11px;
}


.commitment-icon {
  flex:
    0
    0
    auto;

  width: 40px;

  height: 40px;

  border-radius: 12px;

  display: flex;

  align-items: center;
  justify-content: center;

  font-size: 16px;
}


.blue-icon {
  background: #e6eff6;

  color: #5a82a4;
}


.beige-icon {
  background: #f2eee6;

  color: #8d806e;
}


.commitment-info {
  min-width: 0;
}


.title-line {
  display: flex;

  align-items: center;

  flex-wrap: wrap;

  gap: 5px;

  margin-bottom: 5px;
}


.title-line strong {
  font-size: 12px;

  line-height: 1.2;

  font-weight: 700;

  color: #292825;
}


.badge {
  min-height: 18px;

  padding:
    0
    6px;

  border-radius: 20px;

  display: inline-flex;

  align-items: center;
  justify-content: center;

  font-size: 7px;

  line-height: 1;

  font-weight: 800;
}


.ai-badge {
  background: #e4eef5;

  color: #4e7696;
}


.manual-badge {
  background: #f1ede5;

  color: #817564;
}


.due-date {
  display: block;

  color: #8f8b84;

  font-size: 9.5px;
}


.detected-detail {
  display: block;

  max-width: 170px;

  margin-top: 3px;

  color: #a09b94;

  font-size: 8px;

  line-height: 1.3;
}


.commitment-actions {
  flex:
    0
    0
    auto;

  display: flex;

  flex-direction: column;

  align-items: flex-end;

  gap: 6px;
}


.amount {
  color: #282725;

  font-size: 12px;

  font-weight: 700;

  white-space: nowrap;
}


.edit-button {
  padding: 0;

  border: none;

  background: transparent;

  color: #6289ad;

  font-size: 9px;

  font-weight: 750;

  cursor: pointer;
}


/* EMPTY */

.empty-state {
  margin-top: 20px;

  padding:
    28px
    18px;

  border-radius: 15px;

  background: #f7f8f9;

  text-align: center;
}


.empty-state strong {
  display: block;

  margin-bottom: 6px;

  color: #405363;

  font-size: 12px;
}


.empty-state p {
  max-width: 270px;

  margin:
    0
    auto;

  color: #8a939b;

  font-size: 9.5px;

  line-height: 1.5;
}


/* ADD */

.add-commitment {
  width: 100%;

  height: 52px;

  margin-top: 24px;

  border:
    1.5px dashed #91a7b8;

  border-radius: 14px;

  background: #ffffff;

  color: #527895;

  display: flex;

  align-items: center;
  justify-content: center;

  gap: 8px;

  font-size: 12px;

  font-weight: 700;

  cursor: pointer;
}


.add-commitment span {
  font-size: 20px;
}


/* MODAL */

.modal-overlay {
  position: fixed;

  inset: 0;

  z-index: 12000;

  display: flex;

  align-items: flex-end;
  justify-content: center;

  background:
    rgba(30, 38, 47, 0.2);
}


.form-panel {
  width: 100%;

  max-width: 430px;

  padding:
    22px
    22px
    88px;

  border-radius:
    22px
    22px
    0
    0;

  background: #ffffff;

  box-shadow:
    0 -12px 40px
    rgba(30, 45, 60, 0.12);
}


.form-header {
  display: flex;

  align-items: flex-start;

  justify-content: space-between;

  margin-bottom: 20px;
}


.form-eyebrow {
  margin:
    0
    0
    4px;

  color: #9c948a;

  font-size: 9px;

  font-weight: 800;

  letter-spacing: 1.3px;
}


.form-header h2 {
  margin: 0;

  color: #263d52;

  font-size: 20px;
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


.field {
  display: block;

  margin-bottom: 15px;
}


.field > span {
  display: block;

  margin-bottom: 7px;

  color: #69655f;

  font-size: 10px;

  font-weight: 700;
}


.field input,
.field select {
  width: 100%;

  height: 46px;

  padding:
    0
    13px;

  border:
    1px solid #dddfe2;

  border-radius: 11px;

  outline: none;

  background: #ffffff;

  color: #282725;

  font-size: 12px;
}


.amount-input {
  height: 46px;

  display: flex;

  align-items: center;

  border:
    1px solid #dddfe2;

  border-radius: 11px;

  overflow: hidden;
}


.amount-input > span {
  padding-left: 13px;

  color: #7a756e;

  font-size: 11px;

  font-weight: 750;
}


.amount-input input {
  height: 44px;

  border: none;

  padding-left: 8px;
}


.form-actions {
  display: flex;

  gap: 9px;

  margin-top: 22px;
}


.save-button,
.delete-button {
  min-height: 46px;

  border: none;

  border-radius: 12px;

  font-size: 11px;

  font-weight: 800;

  cursor: pointer;
}


.save-button {
  flex: 1;

  background: #6289ad;

  color: #ffffff;
}


.delete-button {
  width: 95px;

  background: #f7eded;

  color: #a05252;
}


.ai-edit-note {
  margin:
    13px
    0
    0;

  color: #929aa1;

  font-size: 9px;

  line-height: 1.5;

  text-align: center;
}


/* MOBILE */

@media (max-width: 430px) {

  .form-panel {
    max-width: none;
  }
}


@media (max-width: 380px) {

  .bank-app {
    padding-left: 20px;

    padding-right: 20px;
  }


  .commitment-row {
    gap: 7px;
  }


  .commitment-left {
    gap: 8px;
  }


  .commitment-icon {
    width: 37px;

    height: 37px;
  }


  .detected-detail {
    max-width: 135px;
  }
}
</style>