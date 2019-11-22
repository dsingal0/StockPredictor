<template>
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            Laughing Stonks
          </h1>
        </div>
      </div>
    </section>
    <columns>
      <column>
        <div class="control">
          <div class="select is-loading">
            <select>
              <option v-for="headers in stockHeaders" v-bind:key="headers.id">  {{ headers }} </option>
            </select>
          </div>
        </div>
      </column>
    </columns>
    <p>Random number from backend: {{ randomNumber }}</p>
    <p>
      Google predicted value: {{ googleValue }}
      <button @click="getRandomFromBackend">New random number</button>
      <div>
        <button @click="getGooglePrediction">Predict GOOG (Google)</button>
      </div>

      <select>
        <option v-for="headers in stockHeaders" v-bind:key="headers.id">  {{ headers }} </option>
      </select>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      randomNumber: 0,
      googleValue: null,
      stockHeaders: []
    }
  },
  methods: {
    getRandomInt (min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min + 1)) + min
    },
    getRandom () {
      this.randomNumber = this.getRandomInt(-100, 0)
    },
    getRandomFromBackend () {
      const path = `http://localhost:5000/api/random`
      axios.get(path)
        .then(response => {
          this.randomNumber = response.data.randomNumber
        })
        .catch(error => {
          console.log(error)
        })
    },
    getGooglePrediction () {
      const path = 'http://localhost:5000/api/goog'
      axios.get(path)
        .then(response => {
          this.googleValue = response.data.googleValue
        })
        .catch(error => {
          console.log(error)
        })
    },
    getStockHeaders () {
      const path = 'http://127.0.0.1:5000/api/headers'
      axios.get(path)
        .then(response => {
          this.stockHeaders = response.data.stockHeaders
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.getRandom()
    this.getStockHeaders()
  },
  mounted () {
    this.getStockHeaders()
  }
}
</script>

<style>
  @import "bulma/css/bulma.css";
</style>
