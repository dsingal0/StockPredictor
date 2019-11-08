<template>
    <div class="home">
        <section class="hero is-medium is-primary is-bold">
            <div class="hero-body has-background-info">
                <div class="container has-text-centered">
                    <h1 class="title has-text-weight-bold is-size-1">
                        THE LAUGHING STONKS
                    </h1>
                </div>
            </div>
        </section>
        <div class="columns is-vcentered has-text-centered is-centered has-background-primary">
            <div class="column">
                <div class="select">
                    <select>
                        <option v-for="(name, index) in stocks" v-bind:key="index">
                            {{ name }}
                        </option>
                    </select>
                </div>
                <!--<div class="dropdown">
                    <div class="dropdown-trigger">
                        <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
                            <span>Dropdown button</span>
                            <span class="icon is-small">
                                <i class="fas fa-angle-down" aria-hidden="true"></i>
                            </span>
                        </button>
                    </div>
                    <div class="dropdown-menu" id="dropdown-menu" role="menu">
                        <div class="dropdown-content">
                            <div class="dropdown-item is-active">
                                TEST
                            </div>
                            <hr class="dropdown-divider" />
                            <a href="#" class="dropdown-item">
                                <div v-for="(name, index) in stocks" v-bind:key="index">
                                    {{ name }}
                                </div>
                            </a>
                        </div>
                    </div>
                </div>-->
                <button class="buttonCalc is-primary has-text-centered">CALCULATE THIS STOCK</button>
            </div>
            <div class="column">
                <strong>
                    PUT TREND GRAPH HERE
                </strong>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Home',
        props: {
            msg: String,
        },

        data()
        {
            return {
                stocks: ['APL', 'GOO']
            }
        }
    };

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
    @import "~bulma/css/bulma.css";

    .column
    {
        width: 100px;
        height: 400px;
    }

    .select
    {
        margin-top: 20px;
        text-align: center;
    }

    .buttonCalc
    {
        margin-top: 50px;
    }
</style>
