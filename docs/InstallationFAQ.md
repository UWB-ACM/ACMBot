# Installation and Running Locally FAQ and Commonly Encountered Issues

### AioHTTP

#### Problem

When I run `python3 main.py` I get this error.

`TypeError: Inheritance a class <class 'aiohttp.http_writer.URL'> from URL is forbidden`

#### Solution

Update your requirements.txt with the latest version from this repo with the latest contents. The file should contain:

```
yarl<1.2
git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]
```

Run your `python3 -m pip install -r requirements.txt` (or equivalent) command again, then `python3 main.py`.

### Mac SSL Cannot Connect

#### Problem

On Mac, with Python 3.6, I cannot get my bot to connect online, and the error log complains about some SSL issue.

#### Solution

You need to install certificates. Navigate to `Applications/Python 3.6`, and double click the `Install Certificates.command` file. Give it a few seconds. Once the terminal window stops doing stuff, you can close it. Retry running the bot with `python3 main.py`.

### Pip Install Doesn't Work

#### Problem

When I run `py -3 -m pip install -r requirements.txt`, the installation fails for some reason.

#### Solution

Ensure that you have git installed, since the requirements installation process makes use of git.


### `python3` is not recognized as an internal or external command... (Windows)

On windows, you need to use `py` isntead of `python3`. Ensure that you have Python installed, and re-open your command window
to ensure that your `%PATH%` has been updated.
