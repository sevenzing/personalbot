My personal telegram bot
====

Current avaliavle on @kektest1488bot in testing mode

## Modules
✔ - implemented

✘ - not yet

+ Convenient buy list ✘
    + /add ✔
    + /list ✔
    + Callback on list ✔
    + Update previous 5 lists after changing or adding ✔
    + Nice response messages ✘
    
    ![](media/example_buylist.png)

+ Cleaning reminder ✘
    + /nextcleaning ✔
    + /setbuilding ✔
    + /setreminder ✔
    + /schedule ✔
    + Nice response messages ✘

    ![](media/cleaning_module_example.gif)

+ Default module ✔
    + /start, /help, /cancel ✔

+ Admin module ✘
    + /restart ✘

## How to start
1. Setup `.evn` file 
    + Create `.env` file in root directory: `mv .env.example .env`
    + Fill the file using your telegram token, admin alias, etc

2. Start the bot using docker:

```bash
$ docker-compose up --build -d
```
