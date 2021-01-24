<template>
  <div>
    <svg aria-hidden="true" style="position: absolute; width: 0; height: 0; overflow: hidden;" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <defs>
        <symbol id="icon-search" viewBox="0 0 32 32">
        <path d="M31.008 27.231l-7.58-6.447c-0.784-0.705-1.622-1.029-2.299-0.998 1.789-2.096 2.87-4.815 2.87-7.787 0-6.627-5.373-12-12-12s-12 5.373-12 12 5.373 12 12 12c2.972 0 5.691-1.081 7.787-2.87-0.031 0.677 0.293 1.515 0.998 2.299l6.447 7.58c1.104 1.226 2.907 1.33 4.007 0.23s0.997-2.903-0.23-4.007zM12 20c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8z"></path>
        </symbol>
        </defs>
        </svg>
    <span>请输入模型型号</span>
    <input v-model="modelNumber" autocomplete="autocomplete" autofocus>
    <button @click="submit">
      <svg><use xlink:href="#icon-search"></use></svg>
    </button>
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
import SearchIcon from '../assets/SearchIcon'

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
    Card,
    SearchIcon
  }
}
</script>

<style scoped>
input {
  height: 22px;
  margin-right: 5px;
  box-sizing: border-box;
  outline: none;
}


button {
  display: inline-block;
  width: 28px;
  height: 22px;
  border: none;
  vertical-align: bottom;
  border-radius: 6px;
  outline: none;
  font-size: 14px;
  font-weight: 400;
  transition: box-shadow .5s;
}

button:hover {
    box-shadow: 2px 2px 1px 1px rgba(0,0,0,.2);
}

.search-icon svg{
  width: 100%;
  height: 100%;
}

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