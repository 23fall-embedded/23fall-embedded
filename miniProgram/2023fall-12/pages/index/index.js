// index.js
const defaultAvatarUrl = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'


Page({
  /**
   * 页面的初始数据
   */
  data: {
    list: '',
    region: ['山东省', '威海市', '环翠区'],
    now: {
      temp: 0,
      text: '未知',
      vis: 0
    },

    LEDarray: ['off', 'red', 'yellow', 'green', 'all'],
    objectArray: [
      {
        id: 0,
        name: 'off'
      },
      {
        id: 1,
        name: 'red'
      },
      {
        id: 2,
        name: 'yellow'
      },
      {
        id: 3,
        name: 'green'
      },
      {
        id: 4,
        name: 'all'
      }
    ],
    LEDindex: 0
  },
  //触发事件
  houduan: function () {
    var that = this;
    wx.request({
      url: 'http://localhost:8080/toJson',
      method: 'GET',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {//成功交互后触发
        console.log(res.data)//打印到控制台
        
      }
    })
  } ,
  regionChange: function (e) {
    this.setData({region: e.detail.value})
    this.getLocationID().then(result => {
      this.getWeatherInfo()
    })
  },

  getWeatherInfo: function (){
    var that = this
    wx.request({
      url: 'https://devapi.qweather.com/v7/weather/now',
      data: {
        location: that.data.locationID,
        key: 'b1aa1ec43dd04106bfc66420636d2e5c'
      },
      success: function(res) {
        that.setData({now: res.data.now})
        //console.log(res.data)
      }
    })
  },

  getLocationID: function() {
    var that = this
    return new Promise(  //解决异步问题
      resolve => {
        wx.request({
          url: 'https://geoapi.qweather.com/v2/city/lookup?',
          data: {
            location: that.data.region[1],
            adm: that.data.region[0],  //防止地名重复，引入参数adm
            key: 'b1aa1ec43dd04106bfc66420636d2e5c'
          },
          success: res => {
            that.setData({locationID: res.data.location[0].id})
            return resolve()
          }
        })
      }
    )
    
  },

  LEDChange: function(e) {
    this.setData({
      LEDindex: e.detail.value
    })
    console.log(e.detail.value);
    wx.request({
      url: 'http://localhost:8080/LED',
      data: {
        "LEDid": e.detail.value
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      method: 'POST',
      success() {
        console.log('LED success');
      }
    })
  },

  gotoLicense: function() {
    wx.navigateTo({      
      url: '../license/license',    //要跳转到的页面路径
    })
    console.log('okok'); 
  },

  onLoad() {
    this.getLocationID().then(result => {
      this.getWeatherInfo()
    })
  }
  
  
})


