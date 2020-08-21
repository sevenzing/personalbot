My personal telegram bot
====

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
    + /nextcleaning ✘
    + /setbuilding ✔
    + /setreminder ✘
    + Nice response messages ✘

## How to start
1. Setup `.evn` file:
```
BOT_TOKEN=111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```
2. Start the bot using docker:

```bash
$ docker-compose up --build -d
```
