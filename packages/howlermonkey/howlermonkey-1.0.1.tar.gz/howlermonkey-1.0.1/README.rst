Howler Monkey
=============
A slack messaging authentication and interfacing system for the DTG
-------------------------------------------------------------------
Intended to allow for automated messaging to our DTG slack group at a controlled endpoint.

Authentication is provided by only allowing connections over local unix domain sockets on a puppy VM. As such any user that can gain access to the host in order to connect must have sufficient monkeysphere auth and thus be a member of the DTG or at least equivalently privileged. Unauthenticated access by minor services can also be mediated by co-locating them on the same host.

Design
======
Server
------
* Python process
* Loads config from file:
  * Slack Address (includes token)
  * Unix socket address
* Accepts JSON payloads over unix socket (via standard handler, poss UnixStreamServer)
* Sends messages to slack via requests (steal code from dtg-lunch-notify)
* Checks response codes?
* Sends JSON back over socket detailing if there were any errors?
* Runs as a daemon (with files for systemd?)

Client
------
* Python Library
* Provides either a single call interface or object interface
  * Single call of style message(text, channel=None, username=None, icon\_url=None, icon\_emoji=None)
  * Or object which lets you store all the varargs params at init and then just call send(text)
  * Steal more code from dtg-lunch-notify
