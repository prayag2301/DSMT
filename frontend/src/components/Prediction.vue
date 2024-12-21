<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// Url for backend
const backendUrl = computed(() => {
  return import.meta.env.VITE_APP_BACKEND_URL;
});

// Placeholder for numeric features
const totalQty = ref(0); // Quantity input

// Placeholders for supplier
const selectedSupplier = ref('');
const suppliers = ['Aromatico', 'Beans Inc.', 'Fair Trade AG', 'Farmers of Brazil', 'Handelskontor Hamburg'];

// Placeholders for warehouse
const selectedWarehouse = ref('');
const warehouses = ['Amsterdam - RR', 'Barcelona - RR', 'Hamburg - RR', 'Istanbul - RR', 'London - RR', 'Nairobi - RR', 'Naples - RR'];

// Placeholders for items
const selectedItem = ref('');
const items = ['Arabica', 'Excelsa', 'Liberica', 'Maragogype', 'Maragogype Type B', 'Robusta'];

// Placeholder for set_warehouse
const selectedSetWarehouse = ref('');
const setWarehouses = ['Barcelona - RR', 'Hamburg - RR', 'Istanbul - RR', 'London - RR', 'Nairobi - RR', 'Naples - RR'];

// Placeholder for prediction result
const prediction = ref('');
const loading = ref(false);


// Hide welcome text after 3 seconds
onMounted(() => {
  setTimeout(() => {
    showWelcomeText.value = false;
  }, 3000);
});

// Make a POST request to the backend
const getPrediction = async () => {
  window.console.log('Fetching prediction...');

  prediction.value = ''; // Clear previous prediction
  loading.value = true; // Set loading state

  try {
    const response = await fetch(`${backendUrl.value}/FINAL_best_model`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        total_qty: totalQty.value,
        supplier_Aromatico: selectedSupplier.value === 'Aromatico' ? 1 : 0,
        supplier_Beans_Inc: selectedSupplier.value === 'Beans Inc.' ? 1 : 0,
        supplier_Fair_Trade_AG: selectedSupplier.value === 'Fair Trade AG' ? 1 : 0,
        supplier_Farmers_of_Brazil: selectedSupplier.value === 'Farmers of Brazil' ? 1 : 0,
        supplier_Handelskontor_Hamburg: selectedSupplier.value === 'Handelskontor Hamburg' ? 1 : 0,
        warehouse_Amsterdam_RR: selectedWarehouse.value === 'Amsterdam - RR' ? 1 : 0,
        warehouse_Barcelona_RR: selectedWarehouse.value === 'Barcelona - RR' ? 1 : 0,
        warehouse_Hamburg_RR: selectedWarehouse.value === 'Hamburg - RR' ? 1 : 0,
        warehouse_Istanbul_RR: selectedWarehouse.value === 'Istanbul - RR' ? 1 : 0,
        warehouse_London_RR: selectedWarehouse.value === 'London - RR' ? 1 : 0,
        warehouse_Nairobi_RR: selectedWarehouse.value === 'Nairobi - RR' ? 1 : 0,
        warehouse_Naples_RR: selectedWarehouse.value === 'Naples - RR' ? 1 : 0,
        item_Arabica: selectedItem.value === 'Arabica' ? 1 : 0,
        item_Excelsa: selectedItem.value === 'Excelsa' ? 1 : 0,
        item_Liberica: selectedItem.value === 'Liberica' ? 1 : 0,
        item_Maragogype: selectedItem.value === 'Maragogype' ? 1 : 0,
        item_Maragogype_Type_B: selectedItem.value === 'Maragogype Type B' ? 1 : 0,
        item_Robusta: selectedItem.value === 'Robusta' ? 1 : 0,
        set_warehouse_Barcelona_RR: selectedSetWarehouse.value === 'Barcelona - RR' ? 1 : 0,
        set_warehouse_Hamburg_RR: selectedSetWarehouse.value === 'Hamburg - RR' ? 1 : 0,
        set_warehouse_Istanbul_RR: selectedSetWarehouse.value === 'Istanbul - RR' ? 1 : 0,
        set_warehouse_London_RR: selectedSetWarehouse.value === 'London - RR' ? 1 : 0,
        set_warehouse_Nairobi_RR: selectedSetWarehouse.value === 'Nairobi - RR' ? 1 : 0,
        set_warehouse_Naples_RR: selectedSetWarehouse.value === 'Naples - RR' ? 1 : 0,
      }),
    });

    const data = await response.json();
    window.console.log(data);

    if (data.prediction !== undefined) {
      prediction.value = data.prediction.toFixed(2); // Update the prediction result
      triggerAnimation();
    } else {
      alert('Prediction data is not available.');
    }
  } catch (error) {
    alert('Could not fetch prediction data.');
    window.console.error('Error fetching data:', error);
  } finally {
    loading.value = false; // Reset loading state
  }
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
        <div class="input-container">
          <!-- Supplier Input -->
          <div class="input-tile hover-shadow">
            <label for="supplier">Select Supplier</label>
            <select id="supplier" v-model="selectedSupplier">
              <option v-for="supplier in suppliers" :key="supplier" :value="supplier">{{ supplier }}</option>
            </select>
          </div>
          <!-- Quantity Input -->
          <div class="input-tile hover-shadow">
            <label for="quantity">Enter Quantity</label>
            <input id="quantity" type="number" v-model="totalQty" />
          </div>
        
          <!-- Warehouse Input -->
          <div class="input-tile hover-shadow">
            <label for="warehouse">Select Warehouse</label>
            <select id="warehouse" v-model="selectedWarehouse">
              <option v-for="warehouse in warehouses" :key="warehouse" :value="warehouse">{{ warehouse }}</option>
            </select>
          </div>
        
          <!-- Item Name Input -->
          <div class="input-tile hover-shadow">
            <label for="item">Select Item</label>
            <select id="item" v-model="selectedItem">
              <option v-for="item in items" :key="item" :value="item">{{ item }}</option>
            </select>
          </div>
        
          <!-- Set Warehouse Input -->
          <div class="input-tile hover-shadow">
            <label for="set-warehouse">Select Set Warehouse</label>
            <select id="set-warehouse" v-model="selectedSetWarehouse">
              <option v-for="setWarehouse in setWarehouses" :key="setWarehouse" :value="setWarehouse">
                {{ setWarehouse }}
              </option>
            </select>
          </div>
        
          <!-- Submit Button -->
          <div class="input-tile hover-shadow">
            <button v-if="!loading" @click="getPrediction">Predict</button>
            <div v-if="loading" class="spinner"></div>
          </div>
        </div>
        <!-- Prediction Result -->
        <div class="prediction-container">
          <h3>Predicted Days Late</h3>
          <p class="prediction" v-if="prediction">{{ prediction }} days</p>
          <p v-else>No prediction available.</p>
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
