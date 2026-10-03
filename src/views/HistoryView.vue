<template>
  <div class="bank-app">
    <header class="page-header">
      <div>
        <p class="eyebrow">JEEBIK</p>
        <h1>Transaction History</h1>
        <p class="subtitle">
          Your recent banking activity
        </p>
      </div>

      <div class="history-icon">
        ↻
      </div>
    </header>

    <section class="ai-note">
      <div class="ai-badge">
        JEEBIK AI
      </div>

      <div>
        <strong>Smart transaction analysis</strong>
        <p>
          JEEBIK analyzes transaction patterns to identify
          potential recurring commitments.
        </p>
      </div>
    </section>

    <section
      v-for="month in transactionHistory"
      :key="month.month"
      class="month-section"
    >
      <div class="month-heading">
        <h2>{{ month.month }}</h2>

        <span>
          {{ month.transactions.length }} transactions
        </span>
      </div>

      <div class="transactions-card">
        <div
          v-for="transaction in month.transactions"
          :key="`${month.month}-${transaction.date}-${transaction.name}`"
          class="transaction"
        >
          <div
            class="transaction-icon"
            :class="transaction.type"
          >
            {{ transaction.icon }}
          </div>

          <div class="transaction-info">
            <div class="transaction-title-row">
              <strong>
                {{ transaction.name }}
              </strong>

              <span
                class="amount"
                :class="transaction.type"
              >
                {{ transaction.type === 'income' ? '+' : '-' }}
                SAR {{ formatNumber(transaction.amount) }}
              </span>
            </div>

            <div class="transaction-details">
              <span>
                {{ transaction.category }}
              </span>

              <span>
                {{ transaction.date }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="privacy-note">
      <div>🔒</div>

      <p>
        JEEBIK uses banking activity already available
        within the bank. No direct connection to every
        external provider is required.
      </p>
    </section>
  </div>
</template>

<script setup>
const transactionHistory = [
  {
    month: 'October 2026',
    transactions: [
      {
        name: 'School Fees',
        amount: 1500,
        category: 'Education',
        date: 'Oct 5',
        type: 'expense',
        icon: '🎓'
      },
      {
        name: 'Panda',
        amount: 310,
        category: 'Groceries',
        date: 'Oct 3',
        type: 'expense',
        icon: '🛒'
      },
      {
        name: 'ChatGPT',
        amount: 80,
        category: 'Subscription',
        date: 'Oct 2',
        type: 'expense',
        icon: '✦'
      },
      {
        name: 'Salary',
        amount: 15000,
        category: 'Income',
        date: 'Oct 1',
        type: 'income',
        icon: '↗'
      }
    ]
  },

  {
    month: 'September 2026',
    transactions: [
      {
        name: 'School Fees',
        amount: 1500,
        category: 'Education',
        date: 'Sep 5',
        type: 'expense',
        icon: '🎓'
      },
      {
        name: 'Panda',
        amount: 420,
        category: 'Groceries',
        date: 'Sep 4',
        type: 'expense',
        icon: '🛒'
      },
      {
        name: 'ChatGPT',
        amount: 80,
        category: 'Subscription',
        date: 'Sep 2',
        type: 'expense',
        icon: '✦'
      },
      {
        name: 'Salary',
        amount: 15000,
        category: 'Income',
        date: 'Sep 1',
        type: 'income',
        icon: '↗'
      }
    ]
  },

  {
    month: 'August 2026',
    transactions: [
      {
        name: 'School Fees',
        amount: 1500,
        category: 'Education',
        date: 'Aug 5',
        type: 'expense',
        icon: '🎓'
      },
      {
        name: 'Coffee Shop',
        amount: 28,
        category: 'Food & Drinks',
        date: 'Aug 4',
        type: 'expense',
        icon: '☕'
      },
      {
        name: 'ChatGPT',
        amount: 80,
        category: 'Subscription',
        date: 'Aug 2',
        type: 'expense',
        icon: '✦'
      },
      {
        name: 'Salary',
        amount: 15000,
        category: 'Income',
        date: 'Aug 1',
        type: 'income',
        icon: '↗'
      }
    ]
  }
]

function formatNumber(value) {
  return Number(value || 0).toLocaleString('en-US')
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.bank-app {
  width: 100%;
  max-width: 430px;
  min-height: 100vh;
  margin: 0 auto;
  background: #ffffff;
  padding: 28px 26px 110px;
  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
  color: #182230;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 22px;
}

.eyebrow {
  margin: 0 0 5px;
  color: #1c63d5;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1.5px;
}

.page-header h1 {
  margin: 0;
  font-size: 25px;
  line-height: 1.2;
}

.subtitle {
  margin: 7px 0 0;
  color: #7b8794;
  font-size: 13px;
}

.history-icon {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  background: #edf4ff;
  color: #1c63d5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
}

.ai-note {
  display: flex;
  gap: 12px;
  padding: 15px;
  margin-bottom: 27px;
  border: 1px solid #d8e7ff;
  border-radius: 16px;
  background: #f6f9ff;
}

.ai-badge {
  height: fit-content;
  flex-shrink: 0;
  padding: 5px 7px;
  border-radius: 7px;
  background: #1c63d5;
  color: white;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.6px;
}

.ai-note strong {
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
}

.ai-note p {
  margin: 0;
  color: #647181;
  font-size: 11px;
  line-height: 1.55;
}

.month-section {
  margin-bottom: 27px;
}

.month-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.month-heading h2 {
  margin: 0;
  font-size: 15px;
}

.month-heading span {
  color: #909aa6;
  font-size: 10px;
}

.transactions-card {
  overflow: hidden;
  border: 1px solid #edf0f3;
  border-radius: 18px;
  background: white;
  box-shadow: 0 5px 18px rgba(31, 42, 55, 0.04);
}

.transaction {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px 14px;
  border-bottom: 1px solid #f0f2f4;
}

.transaction:last-child {
  border-bottom: none;
}

.transaction-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  border-radius: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f6f8;
  font-size: 17px;
}

.transaction-icon.income {
  background: #eef9f2;
}

.transaction-info {
  min-width: 0;
  flex: 1;
}

.transaction-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.transaction-title-row strong {
  overflow: hidden;
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.amount {
  flex-shrink: 0;
  color: #263342;
  font-size: 12px;
  font-weight: 700;
}

.amount.income {
  color: #218653;
}

.transaction-details {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 5px;
  color: #929ca8;
  font-size: 10px;
}

.privacy-note {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 14px;
  border-radius: 15px;
  background: #f7f8fa;
}

.privacy-note div {
  font-size: 14px;
}

.privacy-note p {
  margin: 0;
  color: #707c89;
  font-size: 10px;
  line-height: 1.55;
}

@media (max-width: 430px) {
  .bank-app {
    padding-left: 22px;
    padding-right: 22px;
  }
}
</style>