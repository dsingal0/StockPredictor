<template>
  <div>
    <p>Home page</p>
    <p>Random number from backend: {{ randomNumber }}</p>
    <p>Google predicted value: {{ googleValue }}
    <button @click="getRandomFromBackend">New random number</button>

    <div>
      <button @click="getGooglePrediction">Predict GOOG (Google)</button>
    </div>
    <h1> This really sucks </h1>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      randomNumber: 0,
      googleValue: null
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
    }

  },
  created () {
    this.getRandom()
  }
}
</script>
