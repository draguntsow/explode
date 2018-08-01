# explode
ShadeProxy project:
ShadeProxy is an experimental proxy with an encryption and extensible set of middlewares.
The main purpose of this project is creation of the universal and extensible way to bypass the DPI systems and possibly protect your data.
Current main idea is to wrap both the https and http (and, maybe, any other protocol) traffic into the common http packages. The trick is in the making the packages unexplorable in automated way.
The server side is built like a WSGI python application which make it fully portable and usable over any HTTP-server which supports WSGI. 
The client side is designed as common local proxy which makes it compatible with any browser or whatever user-agent you use.