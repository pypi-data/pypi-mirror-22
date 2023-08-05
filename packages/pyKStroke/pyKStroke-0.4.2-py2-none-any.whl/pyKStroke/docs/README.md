##Preamble

To read correctly the markups inside this file and all other files included in the *DOCS* folder
you should use a reader for the *Markdown* syntax (unnecessary if you are reading the online version).

My main passion is to program but do not consider myself an expert programmer so, please don't blame me if some parts of code are crappy.   
**You can help me to make it better! ;)**  
Another point is that, there will probably be alot of grammatical errors, because of my bad english, 
then any person that is able to correct them is welcome.


---

##Description

####Simple keyboard input hook on multiple platforms that returns a character.

I know that there are others Python packages similar to this on the web, but i make this because my *main goal* would be 
to create an **easy-to-use** and **fast-response** keyboard input event hook package that can be adapted to different types of use.   

The main modules are [**ksSys.py**](Reference.md) and [**ksApp.py**](Reference.md).   
The classes directly included in the above modules are the only ones that you can use for input purposes.   
I've tried to use the same interface in both modules classes to achieve an easy interpretation of what they do, 
even if *"under the hood"* is used a different code implementation.
Both returs a tuple with virual key code and event state code.


---

##Supports

Supported operating Systems are:  

- *Macintosh* 9.0 and earlier that support `Carbon` library (*not tested*) or alternatively `Xlib` library;  
- *OS/X* 10.0 and higher that support `Xlib` library;
- *Windows XP* and higer that support `win32` APIs;  
- *Unix* like systems that supports `Xlib` library.  


---

##Requirements

This package use several Third-Party components **not included in the distribution**. 
Use _pip_ manager to install all required platform-specific python dependencies automatically.
If you dislike the use of _pip_, you need to download the required packages manually.
To do this you can download them from the [_PyPI_](https://pypi.python.org/pypi) website. 
 
Below a list of them:  

* For Windows platforms  

    - [pypiwin32-219](https://pypi.python.org/pypi/pypiwin32/219)  
    - [pyHook-1.5.1](https://pypi.python.org/pypi/pyHook/1.5.1)  

* For Unix like platforms 

    - [python-xlib-0.17](https://pypi.python.org/pypi/python-xlib/0.17)

* For Macintosh OS

    - [carbon](https://docs.python.org/2/library/carbon.html) (already included in the Python Standard Library)
   OR
    - MacX (external library)
    - [python-xlib-0.17](https://pypi.python.org/pypi/python-xlib/0.17) 

* For Os/X System

    - XDarwin (external library for OsX =< 10.2)
    - [XQuartz](https://www.xquartz.org/) (external library for OsX >= 10.2)
    - [python-xlib-0.17](https://pypi.python.org/pypi/python-xlib/0.17) 

For subpackages used by modules above, please refers to their website.  


---

##Installation

The easy way is to install the package via _pip_:

>`pip install --upgrade pykstroke`

Whereas i used *distutils* installation policy, so if you've manually downloaded the source distribution run the following command: 

>`python setup.py install` 

in a Windows *command prompt* or in a Unix-like *terminal* systems and you should be ok.
If you wish can add the `--user` parameter to the command and install the source in the user path.  

If you download the *Windows* distribution, simple run it as standard *Windows* installation package. 

For more details on how to install python modules see [here](https://docs.python.org/2/install/).


---

##API Reference

I have set this [GUIDE](Reference.md) for a good reading and understanding of the code.  
For this I have tried to combine the *references* and *examples* style structure in a common manner. 

**It is not yet complete.**


---

##Planned Features

Support for *Android* and *iOS* systems and need a better *OsX* implementation.

If you need to report a bug or would like to see implemented a new feature, 
or simple you need more details on either one, see the [_Issues section_](https://bitbucket.org/Tungsteno/pykstroke/issues). 


---

##License

This source is distributed under [**LGPLv2.1+**](LICENSE) or later.  

The third-party components specified under section [**Requirements**](#markdown-header-requirements) have their license, not necessarily under *LGPL*.  
For them, refer to the corresponding package or their website.  


---

##Credits

Thanks to all people that help me, directly or indirectly, to assemble and test the code of this package.  

All thirt-party packages credits are of their owners.  

This package is created by *Tungsteno*.  
If you need to contact me for more information or to push a *Git patch*, send an email to <contacts00-pykstroke@yahoo.it>.  
Project [_website_](https://bitbucket.org/Tungsteno/pykstroke/wiki/Home)
