# owo.py

A wrapper that was written inside of Python that allows for you to upload images to the owo.whats-th.is and shorten URLs through uwu.whats-th.is. Allows for both methods through Async and Non-Async. (Suppports py2)

# Instructions

1. Gain a API key in order to be actually able to use the service.
2. Run the command `pip install owo`.
3. Check the usage below to find some basic examples of how to use the script.

### Mobile Devices

For use on Android devices using [Termux](https://termux.com/), the Termux:API package is required to use the background monitor.
You will need to install using your device's app store AND by running `$ apt install termux-tools termux-api`


**It is also REQUIRED to do the following after installing, or it will not work!**

```bash
$ owo-fix
```

The background monitor watches for new files in a directory (usually a screenshots folder) and uploads those new files.

The program accepts several command-line flags.

```
$ owo-bg --help
usage: bg.py [-h] [-p PATH] -k KEY [-u URL] [-tts]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to check file updates
  -k KEY, --key KEY     API Key
  -u URL, --url URL     Base vanity url to use
  -tts                  Confirm message over tts | Mobile only
```

The base url can be any of the owo.whats-th.is vanity urls.

**Example Use**

`$ owo-bg -p "/storage/Pictures/Screenshots" -k "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" -u "https://i.am-a.ninja/"`

This starts a background task monitoring `/storage/Pictures/Screenshots/` for new files, uploads those files and returns the link, using the vanity url [https://i.am-a.ninja/](https://i.am-a.ninja/)


# Usage

Basic usage of the script is like so.

**Image Uploading**

```python
import owo
owo.upload_files(API_KEY, "file.png", "file.py")
```

returns something like..

```python
{"file.png": "url", "file.py": "url"}
```

**URL Shortening**

```python
import owo
owo.shorten_urls(API_KEY, "url1","url2")
```

returns something like..

```python
["shortened url 1","shortened url 2"]
```


For more powerful/better examples please check /examples/.

# Contribute

1. Fork repo.
2. Edit code.
3. Make a PR.
4. Submit said PR.

# License

A copy of the MIT license can be found in `LICENSE.md`.


