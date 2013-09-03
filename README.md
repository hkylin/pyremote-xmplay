PyRemote - XMPlay
=================

This project it's meant to control the [XMPlay media player](http://support.xmplay.com/) in windows, in a remotely way, with Python 3.
The music is stored in the family desktop, and, well, they like windows.

Talking technically, the XMPlay Player, is very lightweitgh and customizable, and runs in background without overloading the system.
The python script that runs in this pc, called "server.py", talks with XMPlay through a windows protocol named Dynamic Data Exchange.
I would have prefered another protocol, but XMPlay uses that, so, well. Yes, I also could send virtual keystrokes, but again, is very system dependant,
and DDE works well. To use DDE with python, I uses the [pywin32 library](http://sourceforge.net/projects/pywin32/files/pywin32/).
Well, the server and client talks through TCP, using sockets. I believe that this projects was an subconscient excuse to learn how to use sockets with python. 

The client it's multiplatform. I run linux in my laptop, so this is good.

In the future I think i could add a gui with PyQT, but for now, the console is ok.

Thanks for reading!

Greetings from Argentina!
