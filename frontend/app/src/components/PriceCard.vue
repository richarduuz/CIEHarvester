<template>
  <div class="container">
    <div class="card">
      <div v-for="(value, key) in price" :key="key">
        <div v-if="key !== '价格'">
          <span>{{key}}: {{value}}</span>
        </div>
      </div>
      <div>
        <span>价格: </span>
        <div class="price-entry" v-for="(value, key) in price['价格']" :key="key">
          <span>{{key}}个: {{value}}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PriceCard",
  props: {
    price: {
      type: Object,
      default(){
        return {}
      }
    }
  },
  methods: {
    test() {
      console.log(this.price);
    }
  }
}
</script>

<style scoped>
.container {
  padding: 2px 16px;
}
.card {
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  width: 250px;
}

.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}

div.price-entry{
  margin: 5px
}
</style>