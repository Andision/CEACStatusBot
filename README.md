# CEACStatusBot🤖

[查看中文文档](README.Chinese.md)
 
automatically check your U.S. visa application status in [CEAC](https://ceac.state.gov/CEACStatTracker/Status.aspx?App=NIV) and notice you instantly!

## Usage

You can deploy it to your own machine, but it is highly recomanded to use Github Actions. 

### Environment Variables

- LOCATION: the location code where you applied for your visa. To find the corresponding code for the embassy, please refer to [this table](LOCATION.md).

- NUMBER: your Application ID or Case Number help icon (e.g., AA0020AKAX or 2012118 345 0001) 

- FROM: the email address you use to send the notification.

- TO: the email address you want the notification sent to. You can send to more than one email, split the email address with "|" and without space. Here is an example: `first@email.com|second@email.com|third@email.com`

- PASSWORD: the password of the `FROM` email. Notice: for some email, such as QQ Mail, you should use "authorization code" instead of your password here, because this repo use SMTP to send email. Check the SMTP usage of your Mailbox Service Provider for more details.

- TIMEZONE: optional, set your timezone to avoid disturbing during sleep. :-) Some example: `Asia/Shanghai` `America/New_York`

### Github Actions

1. folk this repo

2. set your Environment Variables in `Github -> Settings -> Secrets and variables -> Actions -> New repository secret`
![image](docs/github.new.secret.png)

3. check your workflow in Actions and your Mailbox

## TODO

- [x] Send Email to multiple emails.
- [ ] Add more third-party notification services.
- [ ] More human-friendly interface.

## Special Thanks

Part of the code in this repo refers to the following project. Thank you for your pretty work.

- [ceac_tracker](https://github.com/lixin-wei/ceac_tracker)
- [CEACStatTracker](https://github.com/yuzeming/CEACStatTracker)