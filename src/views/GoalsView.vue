<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const search = ref('')
const selectedCategory = ref('Electronics')
const selectedProduct = ref(null)
const selectedSearchSuggestion = ref(false)

const categories = [
  { name: 'Travel', icon: 'travel' },
  { name: 'Electronics', icon: 'electronics' },
  { name: 'Car', icon: 'car' },
  { name: 'Home', icon: 'home' },
  { name: 'Education', icon: 'education' },
  { name: 'Emergency', icon: 'emergency' },
  { name: 'Personal', icon: 'personal' }
]

const products = [
  {
    id: 1,
    name: 'MacBook Air 13"',
    price: 'SAR 4,499',
    numericPrice: 4499
  },
  {
    id: 2,
    name: 'MacBook Air 15"',
    price: 'SAR 5,999',
    numericPrice: 5999
  },
  {
    id: 3,
    name: 'MacBook Pro 14"',
    price: 'SAR 7,999',
    numericPrice: 7999
  },
  {
    id: 4,
    name: 'MacBook Pro 16"',
    price: 'SAR 10,499',
    numericPrice: 10499
  }
]

const cleanSearch = computed(() => {
  return search.value.trim().toLowerCase()
})

const hasSearch = computed(() => {
  return cleanSearch.value.length > 0
})

const showMacBookSuggestion = computed(() => {
  if (!hasSearch.value || selectedSearchSuggestion.value) {
    return false
  }

  return 'macbook'.startsWith(cleanSearch.value)
})

const showNoResults = computed(() => {
  return (
    hasSearch.value &&
    !selectedSearchSuggestion.value &&
    !showMacBookSuggestion.value
  )
})

function goBack() {
  router.push('/')
}

function selectCategory(category) {
  selectedCategory.value = category
}

function selectProduct(id) {
  selectedProduct.value = id
}

function selectMacBookSuggestion() {
  search.value = 'MacBook'
  selectedSearchSuggestion.value = true
  selectedCategory.value = 'Electronics'
  selectedProduct.value = 2
}

function handleSearchInput() {
  selectedSearchSuggestion.value = false
  selectedProduct.value = null
}

function clearSearch() {
  search.value = ''
  selectedSearchSuggestion.value = false
  selectedProduct.value = null
}

function continueToAnalysis() {
  if (!selectedSearchSuggestion.value || !selectedProduct.value) {
    return
  }

  const product = products.find(
    item => item.id === selectedProduct.value
  )

  if (!product) {
    return
  }

  sessionStorage.setItem(
    'jeebikSelectedGoal',
    JSON.stringify({
      id: product.id,
      name: product.name,
      price: product.numericPrice
    })
  )

  router.push('/analysis')
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
          <svg viewBox="0 0 24 24" aria-hidden="true">
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

        <h1>What are you planning for?</h1>
      </header>

      <!-- SEARCH -->
      <div class="search-area">

        <div
          class="search-box"
          :class="{ 'search-open': showMacBookSuggestion }"
        >
          <svg
            class="search-icon"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              cx="11"
              cy="11"
              r="6.5"
              fill="none"
              stroke="currentColor"
              stroke-width="1.7"
            />
            <path
              d="M16 16l4 4"
              fill="none"
              stroke="currentColor"
              stroke-width="1.7"
              stroke-linecap="round"
            />
          </svg>

          <input
            v-model="search"
            type="text"
            placeholder="Search for a goal"
            aria-label="Search goals"
            autocomplete="off"
            @input="handleSearchInput"
          />

          <button
            v-if="hasSearch"
            type="button"
            class="clear-search"
            aria-label="Clear search"
            @click="clearSearch"
          >
            ×
          </button>
        </div>

        <!-- AUTOCOMPLETE -->
        <div
          v-if="showMacBookSuggestion"
          class="suggestions"
        >
          <button
            type="button"
            class="suggestion-row"
            @click="selectMacBookSuggestion"
          >
            <div class="suggestion-icon">
              <svg viewBox="0 0 28 24" aria-hidden="true">
                <rect
                  x="5"
                  y="3"
                  width="18"
                  height="13"
                  rx="1.5"
                />
                <path d="M3 19h22l-2 2H5l-2-2z" />
              </svg>
            </div>

            <div class="suggestion-text">
              <strong>MacBook</strong>
              <span>Electronics</span>
            </div>

            <svg
              class="suggestion-arrow"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M9 6l6 6-6 6" />
            </svg>
          </button>
        </div>

      </div>

      <!-- CATEGORIES -->
      <section class="categories">

        <button
          v-for="category in categories"
          :key="category.name"
          type="button"
          class="category"
          :class="{ selected: selectedCategory === category.name }"
          @click="selectCategory(category.name)"
        >
          <div class="category-icon">

            <!-- TRAVEL -->
            <svg
              v-if="category.icon === 'travel'"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                d="M12 2v8M12 10L4 14v2l8-2 8 2v-2l-8-4zM12 14v6M9 22l3-2 3 2"
              />
            </svg>

            <!-- ELECTRONICS -->
            <svg
              v-else-if="category.icon === 'electronics'"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <rect
                x="5"
                y="4"
                width="14"
                height="10"
                rx="1"
              />
              <path d="M3 18h18l-2 2H5l-2-2z" />
            </svg>

            <!-- CAR -->
            <svg
              v-else-if="category.icon === 'car'"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M5 11l2-5h10l2 5" />
              <rect
                x="3"
                y="10"
                width="18"
                height="7"
                rx="2"
              />
              <path d="M6 17v2M18 17v2M6.5 13h1M16.5 13h1" />
            </svg>

            <!-- HOME -->
            <svg
              v-else-if="category.icon === 'home'"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M3 11.5L12 4l9 7.5" />
              <path d="M5.5 10v10h13V10" />
            </svg>

            <!-- EDUCATION -->
            <svg
              v-else-if="category.icon === 'education'"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M3 9l9-5 9 5-9 5-9-5z" />
              <path d="M7 12v4c3 2.5 7 2.5 10 0v-4" />
              <path d="M21 9v6" />
            </svg>

            <!-- EMERGENCY -->
            <svg
              v-else-if="category.icon === 'emergency'"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle
                cx="12"
                cy="12"
                r="8"
              />
              <path d="M12 7v6" />
              <circle
                cx="12"
                cy="16.5"
                r="0.7"
                class="filled-dot"
              />
            </svg>

            <!-- PERSONAL -->
            <svg
              v-else-if="category.icon === 'personal'"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle
                cx="12"
                cy="8"
                r="3"
              />
              <path
                d="M6 20c.5-4 2.5-6 6-6s5.5 2 6 6"
              />
            </svg>

          </div>

          <span class="category-name">
            {{ category.name }}
          </span>
        </button>

      </section>

      <!-- INITIAL STATE -->
      <section
        v-if="!hasSearch"
        class="search-state"
      >
        <div class="state-icon">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle
              cx="11"
              cy="11"
              r="6.5"
            />
            <path d="M16 16l4 4" />
          </svg>
        </div>

        <strong>What would you like to plan for?</strong>

        <p>
          Search for something you want to achieve or purchase.
        </p>
      </section>

      <!-- NO RESULTS -->
      <section
        v-else-if="showNoResults"
        class="search-state"
      >
        <div class="state-icon">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle
              cx="11"
              cy="11"
              r="6.5"
            />
            <path d="M16 16l4 4" />
          </svg>
        </div>

        <strong>No results found</strong>

        <p>
          Try searching for "MacBook".
        </p>
      </section>

      <!-- PRODUCT RESULTS -->
      <section
        v-if="selectedSearchSuggestion"
        class="results"
      >

        <p class="results-label">
          RESULTS FOR "MACBOOK"
        </p>

        <div class="product-list">

          <button
            v-for="product in products"
            :key="product.id"
            type="button"
            class="product-row"
            :class="{ selected: selectedProduct === product.id }"
            @click="selectProduct(product.id)"
          >
            <div class="product-left">

              <div class="laptop-icon">
                <svg viewBox="0 0 28 24" aria-hidden="true">
                  <rect
                    x="5"
                    y="3"
                    width="18"
                    height="13"
                    rx="1.5"
                  />
                  <path d="M3 19h22l-2 2H5l-2-2z" />
                </svg>
              </div>

              <strong>
                {{ product.name }}
              </strong>

            </div>

            <span class="product-price">
              {{ product.price }}
            </span>
          </button>

        </div>

      </section>

      <!-- CONTINUE -->
      <button
        v-if="selectedSearchSuggestion && selectedProduct"
        type="button"
        class="continue-button"
        @click="continueToAnalysis"
      >
        Continue
      </button>

    </main>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

button,
input {
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
  padding: 30px 26px 50px;
}

/* HEADER */

.header {
  position: relative;
  display: flex;
  align-items: center;
  min-height: 40px;
  margin-bottom: 25px;
}

.header h1 {
  width: 100%;
  margin: 0;
  padding: 0 25px;
  text-align: center;
  color: #242321;
  font-size: 19px;
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

/* SEARCH */

.search-area {
  position: relative;
  width: 100%;
  z-index: 5;
}

.search-box {
  position: relative;
  width: 100%;
  height: 48px;
  padding: 0 14px;
  border-radius: 14px;
  background: #f2f1ee;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #77746f;
}

.search-box.search-open {
  border-radius: 14px 14px 0 0;
}

.search-icon {
  flex: 0 0 auto;
  width: 20px;
  height: 20px;
}

.search-box input {
  min-width: 0;
  width: 100%;
  padding: 0;
  border: 0;
  outline: 0;
  background: transparent;
  color: #33312e;
  font-size: 13px;
}

.search-box input::placeholder {
  color: #aaa69f;
}

.clear-search {
  flex: 0 0 auto;
  width: 28px;
  height: 28px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: #e3e1dc;
  color: #77736d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
}

/* AUTOCOMPLETE */

.suggestions {
  position: absolute;
  top: 48px;
  left: 0;
  right: 0;
  overflow: hidden;
  border: 1px solid #e3e0db;
  border-top: 0;
  border-radius: 0 0 14px 14px;
  background: #ffffff;
  box-shadow: 0 8px 18px rgba(35, 47, 56, 0.08);
}

.suggestion-row {
  width: 100%;
  min-height: 62px;
  padding: 9px 13px;
  border: 0;
  background: #ffffff;
  display: flex;
  align-items: center;
  text-align: left;
  cursor: pointer;
}

.suggestion-row:hover {
  background: #f6f8f9;
}

.suggestion-icon {
  flex: 0 0 auto;
  width: 39px;
  height: 39px;
  border-radius: 10px;
  background: #e8f0f5;
  color: #527fa3;
  display: flex;
  align-items: center;
  justify-content: center;
}

.suggestion-icon svg {
  width: 23px;
  height: 20px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.suggestion-text {
  min-width: 0;
  margin-left: 11px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.suggestion-text strong {
  color: #33312e;
  font-size: 12px;
}

.suggestion-text span {
  color: #99958e;
  font-size: 9px;
}

.suggestion-arrow {
  width: 17px;
  height: 17px;
  margin-left: auto;
  fill: none;
  stroke: #99958e;
  stroke-width: 1.7;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* CATEGORIES */

.categories {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  column-gap: 12px;
  row-gap: 17px;
  margin-top: 22px;
  margin-bottom: 29px;
}

.category {
  min-width: 0;
  padding: 0;
  border: 0;
  background: transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
  cursor: pointer;
}

.category-icon {
  width: 55px;
  height: 48px;
  border-radius: 14px;
  background: #f1f0ed;
  color: #79766f;
  display: flex;
  align-items: center;
  justify-content: center;
  transition:
    background 0.15s ease,
    color 0.15s ease;
}

.category-icon svg {
  width: 26px;
  height: 26px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.7;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.category-icon .filled-dot {
  fill: currentColor;
  stroke: none;
}

.category.selected .category-icon {
  background: #e3eef6;
  color: #315b7a;
}

.category-name {
  color: #716e68;
  font-size: 10px;
  line-height: 1.2;
  font-weight: 600;
  white-space: nowrap;
}

.category.selected .category-name {
  color: #315b7a;
  font-weight: 750;
}

/* SEARCH STATE */

.search-state {
  min-height: 190px;
  padding: 38px 20px 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.state-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 14px;
  border-radius: 14px;
  background: #f1f0ed;
  color: #7b7771;
  display: flex;
  align-items: center;
  justify-content: center;
}

.state-icon svg {
  width: 22px;
  height: 22px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.7;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.search-state strong {
  color: #3e3b37;
  font-size: 13px;
}

.search-state p {
  max-width: 250px;
  margin: 7px 0 0;
  color: #99958e;
  font-size: 11px;
  line-height: 1.5;
}

/* RESULTS */

.results {
  margin-top: 5px;
}

.results-label {
  margin: 0 0 10px;
  color: #98948e;
  font-size: 9px;
  line-height: 1;
  font-weight: 800;
  letter-spacing: 0.8px;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.product-row {
  width: 100%;
  min-height: 60px;
  padding: 9px 14px;
  border: 1.5px solid #e3e0db;
  border-radius: 13px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: #292825;
  text-align: left;
  cursor: pointer;
  transition:
    border-color 0.15s ease,
    background 0.15s ease,
    transform 0.15s ease;
}

.product-row:active {
  transform: scale(0.99);
}

.product-row.selected {
  border-color: #6c96b6;
  background: #edf4f8;
}

.product-left {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-left strong {
  font-size: 12px;
  line-height: 1.2;
  font-weight: 700;
}

.laptop-icon {
  flex: 0 0 auto;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #f1f0ed;
  color: #6e8da5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-row.selected .laptop-icon {
  background: #dfeaf2;
  color: #527fa3;
}

.laptop-icon svg {
  width: 24px;
  height: 21px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.product-price {
  flex: 0 0 auto;
  color: #34322f;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

/* CONTINUE */

.continue-button {
  width: 100%;
  height: 49px;
  margin-top: 21px;
  border: 0;
  border-radius: 12px;
  background: #527fa4;
  color: #ffffff;
  font-size: 12px;
  font-weight: 750;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.continue-button:active {
  transform: scale(0.99);
}

/* MOBILE */

@media (max-width: 380px) {
  .bank-app {
    padding-left: 20px;
    padding-right: 20px;
  }

  .header h1 {
    font-size: 18px;
  }

  .categories {
    column-gap: 7px;
  }

  .category-icon {
    width: 50px;
    height: 46px;
  }

  .category-icon svg {
    width: 24px;
    height: 24px;
  }

  .product-row {
    padding-left: 11px;
    padding-right: 11px;
  }

  .product-left {
    gap: 9px;
  }

  .product-price {
    font-size: 10px;
  }
}
</style>