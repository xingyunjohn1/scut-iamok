# scut-iamok
Automatically update your daily health state

**Only for whom followed the injection routine blow：**

| Injection Type. | Time | Note                                       |
| -------------- | ---- | ------------------------------------------ |
| Basic vaccination      | 2  | 3-times basic vaccination routine is not supported yet|
| Booster shot   | Any  |  |

**Plz help us support the 3-times basic vaccination routine.**

This project is fork from @hanwckf . Thanks for his great work!

## Requirements

`pip3 install requests urllib bs4 lxml`

## Usage

 1. Download and unzip the project. 
 2. Edit your SCUT SSO `username` and `password` in Line `12` of file `autok.py`. 
 3. Execute `autok.py`.
 4. (Optional) Check the output text, ensure a log is recored like `[yyyy-mm-dd hh:mm:ss]: iamok!`
 5. (Optional) Check your SSO system in WeChat, ensure the first line of the iamok website is corresponded to the log.
 6. Update your crontab setting.
>`crontab -e`
>
>Add a line to the EOF.
>
>`0 9-10 * * * /usr/bin/python3 /your_path/scut-iamok/autok.py >> /tmp/iamok.log 2>&1`

[View in VSCode Online](//github.dev/xingyunjohn1/scut-iamok)
