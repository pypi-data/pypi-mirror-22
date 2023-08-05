Howler Monkey
=============
A slack messaging authentication and interfacing system for the DTG
-------------------------------------------------------------------
Intended to allow for automated messaging to our DTG slack group at a controlled endpoint.

Authentication is provided by only allowing connections over local unix domain sockets on a puppy VM. As such any user that can gain access to the host in order to connect must have sufficient monkeysphere auth and thus be a member of the DTG or at least equivalently privileged. Unauthenticated access by minor services can also be mediated by co-locating them on the same host.
