# ACMBot
A utility bot for the UWB ACM Discord server. Written in Python using the [discord.py](discord.py) library.

## Commands Reference

`TODO`

## Contributing

Please see the [contribution guidelines described in CONTRIBUTING.](contributing)

## Installation and Running Locally

*If you encounter any problems, please [read the Installation FAQ.](installationFAQ)*

If you wish to make modifications to the codebase, fork this repository first. Then,
clone the repository to your machine.

### Installation

First, ensure that you have Python 3.6 installed with an up-to-date version of `pip`.

Install the Python package requirements using `pip`:

Linux:

```console
sudo apt-get install libffi-dev python3-dev
python3.6 -m pip install -r requirements.txt
```

Windows:

```console
py -3 -m pip install -r requirements.txt
```

Mac:

```console
python3 -m pip install -r requirements.txt
```

### Setup

Create and register a new Discord Bot application [in the Discord Application Portal.](discordapi)

Create a new file called `config.ini` in your local repo's root directory with the following
contents:

```ini
[Configuration]
connection_token=YOUR_TOKEN_GOES_HERE
```

### Running the Bot

Run the bot with the following command (or equivalent):

```command
python3.6 main.py
```

You can invite your bot to a test server using the following invite link (substitute your app's client ID):

`https://discordapp.com/oauth2/authorize?client_id=INSERT_CLIENT_ID_HERE&scope=bot`

The bot should appear to be online, and the name of the registered bot application should be
displayed in the console.

Then, test that the bot is working by typing `;;ping` in a channel with the bot.

[discord.py]: https://github.com/Rapptz/discord.py
[contributing]: .github/CONTRIBUTING
[installationFAQ]: docs/InstallationFAQ.md
[discordapi]: https://discordapp.com/developers/applications/me