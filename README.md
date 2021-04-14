# Little Amber
This is Little Amber, a bot I created to help manage the links in Amber's server.

## List of available commands:
* `!help` - gives a list of commands available and how to use them
* `!uptime` - returns how long the bot has been online for. Great for debugging

## Usage
If (~~for some inexplicable reason~~) you'd like fork this bot and use it for yourself, great! Just know...
* You'll have to make a folder name `config` and inside that folder create a json file named `config.json`.
* In there, it should look something like this:
```json
{
    "token": "<token-string>",
    "prefix": "<preferred prefix>",
    "client_id": <integer representation of the bot's id>,
    "me": <integer representation of the programmer's id>
}
```

And you're good to go!