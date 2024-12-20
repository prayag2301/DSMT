<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// Url for backend
const backendUrl = computed(() => {
  return import.meta.env.VITE_APP_BACKEND_URL;
});

// Placeholder for supplier
const selectedSupplier = ref('');

// Options for suppliers
const suppliers = ['Aromatico', 'Beans Inc.', 'Fair Trade AG', 'Farmers of Brazil', 'Handelskontor Hamburg'];

// Placeholder for quantity
const quantity = ref(0);

// Placeholder for prediction
const prediction = ref('');

// Loading state
const loading = ref(false);

// Placeholder for warehouse
const selectedWarehouse = ref('');

// Options for warehouses
const warehouses = ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt'];

// Welcome text visibility
const showWelcomeText = ref(true);

// Hide welcome text after 3 seconds
onMounted(() => {
  setTimeout(() => {
    showWelcomeText.value = false;
  }, 3000);
});

// Make a get request to the backend
const getPrediction = async () => {
  window.console.log('fetching data');

  prediction.value = '';

  loading.value = true; // Set loading to true
  try {
    const response = await fetch(`${backendUrl.value}/score_model?supplier=${selectedSupplier.value}&quantity=${quantity.value}`);
    const data = await response.json();
    window.console.log(data);
    if (data.avg_prediction !== undefined) {
      prediction.value = data.avg_prediction.toFixed(2);
      triggerAnimation();
    } else {
      alert('Prediction data is not available');
    }
  } catch (error) {
    alert('Could not fetch data');
    window.console.error('Error fetching data:', error);
  }
  loading.value = false;
};

// Trigger animation
const triggerAnimation = () => {
  const video = document.querySelector('.animation-video') as HTMLVideoElement;
  if (video) {
    video.style.display = 'block';
    video.play();
    setTimeout(() => {
      video.style.display = 'none';
      const components = document.querySelectorAll('.input-tile');
      components.forEach((comp, index) => {
        setTimeout(() => {
          comp.classList.add('move-to-center');
        }, index * 300);
      });

      setTimeout(() => {
        const result = document.querySelector('.prediction-container');
        result?.classList.add('show-result');
      }, components.length * 300);
    }, 3000); // Play video for 3 seconds
  }
};
</script>

<template>
  <div>
    <!-- Welcome text -->
    <h1 v-if="showWelcomeText" class="welcome-text">Welcome to Our Order Prediction App</h1>
    
    <div v-else class="dashboard-tile">
      <div class="dashboard">
        <!-- Animation video -->
        <video class="animation-video" src="/output.mp4" style="display: none; width: 100%; max-width: 600px; margin-bottom: 1em;"></video>
        
        <!-- Prediction input -->
        <div class="input-container">
          <div class="input-tile hover-shadow">
            <label for="supplier">Select a supplier</label>
            <select id="supplier" v-model="selectedSupplier" :style="{ color: selectedSupplier ? 'black' : 'grey' }">
              <option v-for="supplier in suppliers" :key="supplier" :value="supplier">{{ supplier }}</option>
            </select>
          </div>
          <div class="input-tile hover-shadow">
            <label for="quantity">Enter Quantity</label>
            <input id="quantity" type="number" v-model="quantity"/>
          </div>
          <div class="input-tile hover-shadow">
            <label for="warehouse">Select a warehouse </label>
            <select id="warehouse" v-model="selectedWarehouse" :style="{ color: selectedWarehouse ? 'black' : 'grey' }">
              <option v-for="warehouse in warehouses" :key="warehouse" :value="warehouse">{{ warehouse }}</option>
            </select>
          </div>
          <div class="input-tile hover-shadow">
            <button v-if="!loading" type="button" @click="getPrediction">Predict</button>
            <div v-if="loading" class="spinner"></div>
          </div>
        </div>

        <!-- Prediction result -->
        <div class="prediction-container">
          <h3>Predicted Days Late</h3>
          <p class="prediction">{{ prediction }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.welcome-text {
  font-size: 2em;
  color: #00796b;
  text-align: center;
  margin: 2em 0;
  animation: fadeInOut 3s ease-in-out;
}

@keyframes fadeInOut {
  0%, 100% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
}

.dashboard-tile {
  margin: 2em;
  padding: 2em;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.dashboard {
  display: flex;
  flex-direction: column;
  gap: 1.5em;
  padding: 1.5em;
  align-items: center;
}

.input-container {
  display: flex;
  gap: 1em;
  flex-wrap: wrap;
  justify-content: center;
}

.input-tile {
  flex: 1;
  min-width: 200px;
  background: #f9f9f9;
  padding: 1em;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.6s ease, opacity 0.6s ease;
  display: flex;
  flex-direction: column;
}

.hover-shadow:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

label {
  display: block;
  margin-bottom: 0.5em;
  font-weight: bold;
  padding: 0.5em;
  width: 100%;
  box-sizing: border-box;
}

input, option,
select {
  width: 100%;
  margin-bottom: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
  height: 25px;
  background-color: #f9f9f9;
  color: black;
}
.move-to-center {
  transform: translate(0, 200px) scale(0.5);
  opacity: 0;
}

button {
  background: #00796b;
  color: white;
  padding: 0.5em 1em;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #004d40;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top-color: #4caf50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.prediction-container {
  text-align: center;
  opacity: 0;
  transition: opacity 0.6s ease;
  align-self: center;
}

.show-result {
  opacity: 1;
}

.prediction {
  font-size: 2em;
  color: #00796b;
}

.animation-video {
  display: none;
  width: 100%;
  max-width: 600px;
  margin-bottom: 1em;
}
</style>
