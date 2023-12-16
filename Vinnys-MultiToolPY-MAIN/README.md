# Vinny's MultiTool -
## By Vinny

# About
<strong>Vinny's Multi Tool-PY</strong> is a multi-threaded Discord Self Bot and it is used for many features such as the token joiner and MassDM

<li>The joiner gets captcha all the time even if the tokens are good</li>
<li>Mass DM is detected</li>
<li>Documentation is not updated after the initial release of Vinny's Multitool</li>

# Features
<li>Proxyless/HTTP Proxy Support</li>
<li>Token Joiner</li>
<li>Token Bio Changer</li>
<li>Token Username Changer</li>
<li>Token Format Changer [Email:Pass:Token] => [Token]</li>
<li>MassDM</li>
<li>Single DM Spam</li>
<li>Server Joiner(Captcha support)</li>
<li>Server Leaver</li>
<li>Member Scrapper</li>
<li>Reaction adder</li>
<li>Username Scrapper(Soon)</li>
<li>Easy to use and setup</li>
<li>Server spammer(Has MassMention)</li>
<li>Token Checker</li>
<li>This can send multiple messages and this can ping the user aswell which is pretty cool if you ask me</li>
<li>Auto Update, This will automatically install all the newest updates so you dont have to download them manually 😃</li>

## Config
| Name                                      | Type | Description                                                                                                                            |
|-------------------------------------------|------|----------------------------------------------------------------------------------------------------------------------------------------|
| <code>removeDeadTokens</code>             | bool | After checking MultiTool will remove all non-working tokens from input/tokens.txt                                                      |
| <code>captcha_api</code>                  | str  | The url of the captcha api you are gonna use to bypass captcha on join, capmonster.cloud and anti-captcha.com are currently supported. |
| <code>captcha_key</code>                  | str  | Your api key for captcha_api.                                                                                                          |
| <code>useDelays</code>                    | bool | If you want to use delays to avoid being rate limited and detected.                                                                    |
| <code>save_failed_logs</code>             | bool | Saves failed logs to logs/logtype.txt                                                                                                  |
| <code>bypass_membership_screening</code>  | bool | Set this to true if you want to bypass membership screening upon joining server. Setting this to true is recommended.                  |
| <code>bypass_reaction_verification</code> | bool | Set this to true if your target server has a reaction verification.                                                                    |
| <code>proxyless</code>                    | bool | If you want to use the tool without proxies.                                                                                           |
| <code>proxyProtocol</code>                | str  | Your proxy protocol, by default its http                                                                                               |
| <code>sendMultitpleMessages</code>        | bool | Set this to true if you want to send multiple messages to the target user                                                              |
| <code>friendBeforeDM</code>               | bool | Set this to true if you want to send a friend request to the target user before dm.                                                    |
| <code>request_timeout</code>              | int  | Timeout for all requests in seconds. Increase if slow connection or proxies.                                                           |
| <code>online_before_dm</code>             | bool | Websockets the token before dm, makes it online which is more realistic.                                                               |
| <code>use_captcha_solver</code>           | bool | Set this to true if you want to use MultiTool's custom captcha-solver for solving the captcha on joiner.                               |

## Example Configuration
```json
{
    "proxy": {
        "protocol": "http",
        "proxyless": true
    },
    "captcha": {
        "api": "anti-captcha.com",
        "key": "YOUR CAPTCHA KEY"
    },
    "joiner": {
        "useDelays": false,
        "delay": 10,
        "bypassMembershipScreening": true,
        "bypassReactionVerification": false
    },
    "removeDeadTokens": true,
    "preferedThreads": 100000,
    "saveFailedLogs": true,
    "requestTimeout": 35,
    "traceback": false
}
```
## How to use?
Install all the requirements
<pre><code>pip install -r requirements.txt
</code></pre>
Fill in the config.json file and message.json file<br/>
And run the VinnysMultitool.exe Application
<pre><code> VinnysMultitool.exe
</code></pre>

## Thank You!
