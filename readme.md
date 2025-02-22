# Dependencies
## 1.1. ChromeDriver (necessary for selenium)

Go to https://developer.chrome.com/docs/chromedriver/downloads and find a compatible ChromeDriver.

    Download compatible chromedriver-xxxxx.zip
    Unzip it
    Place the chromedriver binary in PATH env var

## 1.2. Python 3.X 

Go to https://www.python.org/about/gettingstarted/ and follow those easy steps

## 1.3. make

# How to run bot
## 1. Create config file
```
cp telegram_bot/bot.conf.sample telegram_bot/bot.conf
```
## 2. Update [config file](./telegram_bot/bot.conf)

## 3. Run bot
```
cd telegram_bot
make
```

## 4. Talk with @hackUDCbot in Telegram