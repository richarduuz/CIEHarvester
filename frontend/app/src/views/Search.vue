<template>
  <div>
    <span>请输入模型型号</span>
    <input v-model="modelNumber">
    <button @click="submit">搜索</button>
      <div class="price-platform" v-for="(value, key) in prices" :key="key">
        <h2>{{key}}</h2>
        <div class="price-card-container" v-if="value.length !== 0">
          <card :price="item" v-for="(item, index) in value" :key="index"></card>
        </div>
        <div v-else>
          <h2>没有搜索结果</h2>
        </div>
      </div>
    </div>
</template>

<script>
import Card from '../components/PriceCard'

export default {
  name: "Search",
  data(){
    return {
      modelNumber: '',
      prices: {}
    }
  },
  methods: {
    submit(){
      this.prices = {}
      let url = this.$store.state.url + '/prices'
      let postData = {'modelNumber': this.modelNumber}
      postData = JSON.stringify(postData)
      this.$http.post(url, postData)
        .then(response => response.json())
        .then(data => {
          if (data){
            console.log(data)
            for (let keys of Object.keys(data)){
              this.prices[keys] = data[keys]
              if (keys === 'szlcsc'){
                for (let item of this.prices[keys]){
                  item['价格'] = this.sortszlcscPrice(item['价格'])
                }
              }
              if (keys === 'ickey'){
                let tmp = []
                for (let item of this.prices[keys]){
                  item['价格'] = this.sortIckeyPrice(item['价格'])
                }
              }
              if (keys === 'ti'){
                for(let item of this.prices[keys]){
                  item['价格'] = this.sortTiPrice(item['价格'])
                }
              }
            }
            this.modelNumber = ''
          }
        })
        .catch((e) => alert(e))
      console.log(this.prices)
    },

    //Internal methods
    sortszlcscPrice(item){
      let result = {}
      let keys = Object.keys(item)
      keys = keys.map(item => {
        return parseFloat(item)
      })
      for (let i = 0; i<keys.length; i++){
        result[keys[i]] = item[keys[i]]
      }
      return result
    },
    sortIckeyPrice(item){
      let result = {}
      let tmp = Object.keys(item).map(key => {
        return [parseInt(key.slice(0, -1)), item[key]]
      })
      tmp.sort((firstVal, secondVal) => {
        return firstVal[0] - secondVal[0]
      })
      for (let ele of tmp){
        result[ele[0]+'+'] = ele[1]
      }
      return result
    },
    sortTiPrice(item){
      let result = {}
      let tmp = Object.keys(item).map((key) => {
        return [key, parseFloat(item[key].substring(1))]
      })
      tmp.sort((firstVal, secondVal) => {
        return secondVal[1] - firstVal[1]
      })
      for (let ele of tmp){
        result[ele[0]] = '$' + ele[1]
      }
      return result
    }
  },
  components: {
    Card
  }
}
</script>

<style scoped>
div.price-container{
  margin: 15px;
  border: 1px solid blue;
  height: 100px;
}
div.price-platform{
  width: 100%;
}
div.price-card-container{
  display: flex;
  overflow-x: auto;
}
</style>