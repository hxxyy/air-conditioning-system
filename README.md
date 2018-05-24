

<h1 align="center">Air Conditioning System</h2>

<p align="center">
   <a><img src="https://img.shields.io/badge/language-python-orange.svg"></a>
   <a href="https://github.com/hxxyy/air-conditioning-system/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-000000.svg"></a>
   <a><img src="https://img.shields.io/badge/platform-linux%7CWindows%7COSX-ff69b4.svg"></a>
   <a><img src="https://img.shields.io/badge/Command-passing-brightgreen.svg"></a>  
</p>



### 产品规范

* 《采暖通风与空气调节设计规范》
* 《中央空调设计参考规范与标准》
* 《旅馆建筑设计规范》

### 产品的功能与作用
* **空调系统由中央空调、从控机和酒店前台三部分构成**
* 中央空调能够实时监测各房间的温度和状态，并要求实时刷新的频率能够进行配置；
    * 要求从控机的控制面板能够发送高、中、低风速的请求，要求各小组自定义高、中、低风情况下的温度变化值；比如以中风为基准，高速风的温度变化曲线可以提高25%，低速风的温度变化曲线可以降低25%。
    * 系统中央空调部分具备计费功能：可根据中央空调对从控机的请求时长及高中低风速的供风量进行费用计算；
* 中央空调实时计算每个房间所消耗的能量以及所需支付的金额，并将对应信息发送给每个从控机进行在线显示，以便客户可以实时查看用量和金额。
* 房间内有独立的从控空调机，但没有冷暖控制设备。
    * 从控机具有一个温度传感器，实时监测房间的温度，并与从控机的目标设置温度进行对比，并向中央空调机发出温度调节请求。

### 参考文献

* 《软件工程》 编著:肖丁等

------

### 开发环境
* 语言: Python 3.6/Qt
* 系统:
    * Windows 10 professional edition
    * Mac OS 10.13
* 数据库:
    * MySQL
* Socket
* json
    
### 贡献名单
* [hxxyy](https://github.com/hxxyy)
* [Chijingwen](https://github.com/Chijingwen)
* [Wei Xiao](https://github.com/awybupt)
