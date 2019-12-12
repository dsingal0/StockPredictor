<template>
  <div>
    <section class="hero is-medium is-primary">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            Laughing Stonks
          </h1>
        </div>
      </div>
    </section>
    <div class="columns is-vcentered is-centered has-text-centered is-8">
      <div class="column is-half">
        <div>
          <h3 class="title is-3">Pick a stock option to predict: </h3>
        </div>
        <div class="select is-vceneterd is-centered">
          <select v-model="selected">
            <option v-for="headers in stockHeaders" v-bind:key="headers.id">  {{ headers }} </option>
          </select>
        </div>
        <button class="button is-primary is-success" v-on:click="submitHandler()"> Submit </button>
      </div>
      <div class="column is-half">
        <img src="./assets/F.png" />
        <!--<h3 class="title is-3"> GRAPH GOES HERE </h3>-->
      </div>
    </div>
    <div class="columns is-vceneterd is-centered has-text-centered is-8">
      <div class="column is-full">
        <h3 class="title is-3"> Predicted Value: {{ output }} </h3>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'App',
  data () {
    return {
      stockHeaders: [],
      output: 9.25,
      selected: ''
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
      const path = 'http://localhost:5000/api/headers'
      axios.get(path)
        .then(response => {
          this.stockHeaders = response.data.stockHeaders
          this.stockHeaders.sort()
        })
        .catch(error => {
          console.log(error)
        })
    },
    getPrediction () {
      const path = 'http://localhost:5000/api/predict'
      axios.get(path, {
        params: {
          ticker: this.selected
        }
      })
        .then(response => {
          this.output = response.data.getPrediction
        })
        .catch(error => {
          console.log(error)
        })
    },
    submitHandler () {
      this.error = false
      console.log(this.selected)
      this.getPrediction()
    }
  },
  created () {
    this.getStockHeaders()
  },
  mounted () {
    this.getStockHeaders()
  }
}
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
