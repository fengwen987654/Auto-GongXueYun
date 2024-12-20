### *GitHub工作流或云函数简易部署+微信消息推送，支持多用户同时打卡、消息合并推送，轻量零成本。*

基于下方项目做的合并简化，**只保留了打卡功能**

1. https://github.com/Rockytkg/AutoMoGuDingCheckIn
2. https://github.com/XuanRanDev/Auto-GongXueYun-2

> # 免费 / 快捷部署

> ## GitHub工作流（新版推荐）

可以不看文字直接看图片，几步就走完了，另外说一下如果频繁利用工作流的话可能会被GitHub判定为滥用，但本项目的频率无碍，且方便好用。

1. Fork仓库，修改一下上方的json配置文件，复制内容
2. 依次进入克隆后的仓库页面上方的:`Settings`  → `Actions secrets and variables` → `Actions`
3. 点击`New repository secret`，Name输入框填写`USER`，Secret输入框里粘贴刚刚复制的`json配置`，如果要多用户，则复制一次数据体自己改改，然后点击下方绿色`Add secret`按钮保存
4. 回到仓库左上角的`Actions`，点击左侧的`打卡`，点击右侧的`Run workflow`，**再次点击**绿色的Run workflow按钮即可开始定时任务

![](https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN@master/img/server/readme/AutoGongXueYun/01.webp)

![](https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN@master/img/server/readme/AutoGongXueYun/02.webp)

![](https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN@master/img/server/readme/AutoGongXueYun/03.webp)

![](https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN@master/img/server/readme/AutoGongXueYun/04.webp)

- 新用户的话，进入Actions后，点击页面黄色块里的按钮开启功能再继续，没什么好讲的，页面看不懂可以自行用翻译APP拍屏。

![](https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN@master/img/server/readme/AutoGongXueYun/05.webp)

- 到这里就结束了，手机上应该能收到通知，配置了微信推送且没收到通知的话，看一下工作流日志，下面是运行成功的日志
- 注：如果在日志中显示解密失败，一定是你的环境变量没有添加正确，确定键名是`USER`四个大写字母。

![](https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN@master/img/server/readme/AutoGongXueYun/06.webp)

- 默认在工作流文件设置了两个打卡时间，注意：这里不是北京时间，有8个小时的偏移自行参考计算并且保持字数规范。如果要修改，自行百度cron表达式，然后去修改工作流文件👇

![](https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN@master/img/server/readme/AutoGongXueYun/07.webp)

> ## 华为云函数（暂时废弃）

由于新版本需要使用`opencv-python`包来越过`滑块验证码`，而这个包在华为云函数**没有公用依赖包**，如果自己上传私有依赖包又太大了受到限制（100MB左右），所以先废弃着吧。

但你也可以自行部署到**个人服务器**，通过宝塔面板或是其他**面板的定时任务**执行命令

```
py index.py
```

如果你有好的建议，可以提出issue，或是通过我主页个人简介的邮箱联系我。

1. [下载最新版](https://github.com/4444TENSEI/Auto-GongXueYun/releases/latest)压缩包(.zip)
2. 跟着**图文教程**走：[华为云函数部署Python定时任务](https://blog.yokaze.top/archives/930)
3. 创建云函数导入ZIP源码后，滚动到页面底部，点击左下角**添加依赖包**、搜索: `cryptography_41.0.7_python39`
4. **环境变量键名**为`USER`，参考文档下方配置文件示例，自行修改后复制，在云函数设置中创建**环境变量**

> ## 开发环境 / 测试 / 部署到服务器使用

- 安装依赖

```
pip install -r requirements.txt
```

- 运行

```
py index.py
```



> ## ※基于提到的项目所做的修改: 

1. 多用户时，打卡推送的消息内容**合并到同一条pushplus消息**，避免了每个用户都会单独推送。

2. 增加了详细的调试语句输出

3. 更新登录/获取token的接口为最新的v6（这里的滑块验证码和AES解密方法大力感谢参考的项目作者[Rockytkg](https://github.com/Rockytkg)，大家可以去帮忙点点star）

4. 简化减少了没必要的配置项，更新了获取token的接口and加解密用的库

5. 新增了配置项: `remark`，作为用户名备注

6. 加入并发、解耦、模块化

   

   ## 配置文件示例（环境变量键名设置为`USER`）: 

   

   ```
   [
     {
       "remark": "自定义用户名，用于通知中标识用户",
       "phone": "手机号",
       "password": "密码",
       "province": "xx省",
       "city": "xx市",
       "area": "xx区",
       "address": "最终打卡页面显示的文字，xx省 · xx市 · 某路边",
       "longitude": "经度(精确到小数点后六位)",
       "latitude": "纬度(精确到小数点后六位)",
       "randomLocation": true,
       "enable": true,
       "desc": "打卡备注",
       "pushKey": "pushplus官网获取的key，需要实名"
     }
   ]
   ```

### 各项配置含义: 

| 参数名称        | 含义                                                         |
| --------------- | :----------------------------------------------------------- |
| remark          | 自定义打卡用户名，会出现在推送消息内容                       |
| phone           | 手机号                                                       |
| password        | 密码                                                         |
| province        | 省份                                                         |
| city            | 城市                                                         |
| area            | 区/县                                                        |
| address         | 详细地址，如果你打卡的时候中间带的有·这个符号你也就手动加上，这里填什么，打卡后工学云就会显示你填的内容（工学云默认·这个符号左右都会有一个空格） |
| longitude       | 打卡位置经度,通过坐标拾取来完成(仅需精确到小数点后6位)，[自行查询传送门](https://jingweidu.bmcx.com/) |
| latitude        | 打卡位置纬度,通过坐标拾取来完成(仅需精确到小数点后6位)，[自行查询传送门](https://jingweidu.bmcx.com/) |
| randomLocation  | 是否启用打卡位置浮动，启用后每次打卡会在原有位置基础上进行位置浮动 |
| enable          | 打卡功能总开关                                               |
| desc            | 打卡备注                                                     |
| passwordpushKey | 密码打卡结果微信推送，微信推送使用的是pushPlus，请到官网绑定微信([传送门](https://www.pushplus.plus/))，然后在发送消息里面把你的token复制出来粘贴到pushKey这项 |

## 多用户配置文件示例

```
[
  {
    "remark": "用户1111111111111",
    "phone": "手机号",
    "password": "密码",
    "province": "xx省",
    "city": "xx市",
    "area": "xx区",
    "address": "最终打卡页面显示的文字，xx省 · xx市 · 某路边",
    "longitude": "经度(精确到小数点后六位)",
    "latitude": "纬度(精确到小数点后六位)",
    "randomLocation": true,
    "enable": true,
    "desc": "打卡备注，顺便说一下：根据用户数量的增加，只要保持标准json格式也就是现在这个样子，一个用户复制一次花括号加进来就行，这里展示三个用户的情况。不限量但是太多了容易造成崩溃",
    "pushKey": "Key设置为相同的会推送到一个微信去，如果不相同则各自推送"
  },
  {
    "remark": "用户222222222222",
    "phone": "手机号",
    "password": "密码",
    "province": "xx省",
    "city": "xx市",
    "area": "xx区",
    "address": "最终打卡页面显示的文字，xx省 · xx市 · 某路边",
    "longitude": "经度(精确到小数点后六位)",
    "latitude": "纬度(精确到小数点后六位)",
    "randomLocation": true,
    "desc": "打卡备注，顺便说一下：根据用户数量的增加，只要保持标准json格式也就是现在这个样子，一个用户复制一次花括号加进来就行，这里展示三个用户的情况。不限量但是太多了容易造成崩溃",
    "pushKey": "Key设置为相同的会推送到一个微信去，如果不相同则各自推送"
  },
  {
    "remark": "用户333333333333",
    "phone": "手机号",
    "password": "密码",
    "province": "xx省",
    "city": "xx市",
    "area": "xx区",
    "address": "最终打卡页面显示的文字，xx省 · xx市 · 某路边",
    "longitude": "经度(精确到小数点后六位)",
    "latitude": "纬度(精确到小数点后六位)",
    "randomLocation": true,
    "desc": "打卡备注，顺便说一下：根据用户数量的增加，只要保持标准json格式也就是现在这个样子，一个用户复制一次花括号加进来就行，这里展示三个用户的情况。不限量但是太多了容易造成崩溃",
    "pushKey": "Key设置为相同的会推送到一个微信去，如果不相同则各自推送"
  }
]
```
