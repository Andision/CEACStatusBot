# CEACStatusBot🤖

自动从[CEAC](https://ceac.state.gov/CEACStatTracker/Status.aspx?App=NIV)查询您的美国签证申请状态，并在状态更新时立即通知您！

感谢 [Andision](https://github.com/Andision)的 [CEACStatusBot](https://github.com/Andision/CEACStatusBot), 这个分支更新了当前的依赖并重构了代码，以便在状态发生变化时通知用户。

## 使用


您可以将其部署到您自己的机器上，但强烈建议使用Github Actions。


###  环境变量


- LOCATION: 您申请签证的使领馆的地点。要查找使领馆对应的名称，请参考[此表](LOCATION.md)。请直接使用使馆位置名，如`CHINA, BEIJING`。


- NUMBER: 您在CEAC网站中的Application ID or Case Number(例如`AA0020AKAX` 或 `2012118 345 0001`)。具体信息请查看[CEAC](https://ceac.state.gov/CEACStatTracker/Status.aspx?App=NIV)网站的说明。**注意**: 请先在[CEAC](https://ceac.state.gov/CEACStatTracker/Status.aspx?App=NIV)网站确认你能够正确获取你的签证状态。这一项目的目的是简化从[CEAC](https://ceac.state.gov/CEACStatTracker/Status.aspx?App=NIV)网站获取签证信息的过程，并不能比人工方式获得更多的信息。

- PASSPORT_NUMBER: 护照号码

- SURNAME: 姓的前5个英文字母

- TIMEZONE: 可选，设置你所在的时区，以避免在睡眠时间收到打扰。例如: `Asia/Shanghai` 或 `America/New_York`。**注意**: 这里使用的是IANA时区数据库的时区表示法，并不是简单的地理位置的组合。例如，如果你希望使用北京时间，你的时区应该是`Asia/Shanghai`而**不是** ~~`Asia/Beijing`~~

- ACTIVE_HOURS: 可选，设置接收通知的活跃时间段，以避免在睡眠时间收到打扰。使用24小时格式。例如: `08:00-22:00`

- GH_TOKEN: 要访问之前的状态，您需要设置一个具有`repo`权限的Github令牌。您可以在Github -> 设置 -> 开发者设置 -> 个人访问令牌中创建一个新的令牌。

#### 邮件通知

如果你想收到邮件通知，需要设置如下环境变量：

- FROM: 发送通知的电子邮件地址。**注意**: 本项目并不提供任何电子邮件服务，需要使用你提供的第三方电子邮件服务通过SMTP协议发送电子邮件，因此需要你提供用于发送通知的电子邮件地址。*一个小技巧是，如果你希望如果你希望通过邮件提醒自己签证状态，你可以在此处填写和收取通知相同的电子邮件地址，即可以使用同一个邮箱收发邮件，换句话说你可以自己给自己发邮件。*

- TO: 接收通知的电子邮件地址。您可以发送到多个电子邮件地址，用“|”分割多个电子邮件地址(“|”这个符号通常在退格键Backspace的下方，回车Enter的上方，你通常需要使用上档Shift键打出这个符号)，不用且不可添加任何空格。下面是几个例子: 
  - 发送到一个邮箱: `your_mail@email.com`
  - 发送到多个邮箱: `first@email.com|second@email.com|third@email.com`

- PASSWORD: 在`FROM`填写的邮箱的密码。**注意**: 对于一些电子邮箱(如QQ邮箱)，你应该在这里使用“授权码”而不是邮箱的密码，因为这个项目使用SMTP协议发送电子邮件。有关详细信息，请查看邮箱服务提供商的SMTP使用方法。

- SMTP: 可选，设置SMTP服务器 (e.g. `smtp.example.com`, `smtp.example.com:587`)

#### Telegram机器人通知

如果你想通过Telegram Bot发送通知，需要设置如下环境变量。

Telegram Bot [创建教程](https://www.cytron.io/tutorial/how-to-create-a-telegram-bot-get-the-api-key-and-chat-id)

- TG_BOT_TOKEN: Bot 密钥

- TG_CHAT_ID: 聊天 ID，获取方法见教程

#### Bark 通知

安装并打开 [Bark](https://github.com/Finb/Bark)，从 App 显示的推送地址中复制设备密钥（例如 `https://api.day.app/YOUR_DEVICE_KEY/...` 中的 `YOUR_DEVICE_KEY` 部分）。

- BARK_DEVICE_KEY: Bark 设备密钥

- BARK_SERVER: 可选，自建 Bark 服务地址；默认使用 `https://api.day.app`

- BARK_GROUP: 可选，通知分组；默认为 `CEACStatusBot`

- BARK_SOUND: 可选，Bark 通知声音名称

### 在 Github Actions 的使用方法


1. folk这个仓库


2. 在`Github -> Settings -> Secrets and variables -> Actions -> New repository secret`中设置环境变量。
![image](docs/github.new.secret.png)


3. 查看 `Github Actions` 中的 `workflows` 是否正常运行，并检查邮箱、Telegram 或 Bark 是否收到通知。

### 本地使用

对于本地使用，可以在项目根目录创建一个 `.env` 文件来存储你的环境变量 (例如 `LOCATION=...`, `NUMBER=...`)，脚本会自动加载它们。或者拷贝模版文件 `.env.example` 并重命名为 `.env`来使用。
然后使用 uv 构建环境：

```bash
pip install uv # 如果你没有安装 uv
uv sync
uv run trigger.py
```


## 待办事项

- [x] 向多个邮箱发送邮件。

- [x] 增加更多第三方通知服务。

- [ ] 更人性化的界面。


## 特别感谢

### 开发者

[h4x3rotab](https://github.com/h4x3rotab) : Telegram bot, 适配新版CEAC接口

### 相关项目

这个repo中的部分代码引用了下面的项目。谢谢你们的工作。

- [ceac_tracker](https://github.com/lixin-wei/ceac_tracker)

- [CEACStatTracker](https://github.com/yuzeming/CEACStatTracker)
