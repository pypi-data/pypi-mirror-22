#API Reference 
*(work in progress)*

*Italic* style words are methods that should be used only for internal package development,  
so i report them here for completeness.

___
/#######################################################################################################################
___
##TABLE OF CONTENTS


##Module 
___                                   
[`ksSys.py`](#markdown-header-kssys) . . . . . . . . . . . . . . . . . . . . . . . . . . Main module for intercept any pressed key character in the system.

___
>###Class  
>___
>[`KeyInput`](#markdown-header-kssys-keyinput) . . . . . . . . . . . . . . . . . . . . . . . . . . Base input class. 

>___
>>####Methods       
>>___
>>[`__init__`](#markdown-header-keyinput-init) . . . . . . . . . . . . . . . . . . . . . . . . . . Initialize the base instance for the current OS.
>>___
>>[`__call__`](#markdown-header-keyinput-call) . . . . . . . . . . . . . . . . . . . . . . . . . . Return pressed key from keyboard.                            
>>___
>>[*`_test`*](#markdown-header-keyinput-_test) . . . . . . . . . . . . . . . . . . . . . . . . . . Try if the class implementation work well.

>___
>###Class 
>___
>[`KeyEvent`](#markdown-header-kssys-keyevent) . . . . . . . . . . . . . . . . . . . . . . . . . . Return pressed keys in an handler function.
>___
>>####Methods  
>>___
>>[`__init__`](#markdown-header-keyevent-init) . . . . . . . . . . . . . . . . . . . . . . . . . . Initialize itself and the inherited class.
>>___
>>[`__call__`](#markdown-header-keyevent-call) . . . . . . . . . . . . . . . . . . . . . . . . . . Start the key event handler.
>>___
>>[`set_event`](#markdown-header-keyevent-set_event) . . . . . . . . . . . . . . . . . . . . . . . . . . Main event loop method. Override it.
>>___
>>[*`_test`*](#markdown-header-keyevent-_test) . . . . . . . . . . . . . . . . . . . . . . . . . . Try if the class implementation work well.

>___
>###Class 
>___
>[`KeyThread`](#markdown-header-kssys-keythread) . . . . . . . . . . . . . . . . . . . . . . . . . . Run a separate thread and return pressed keys.

>___
>>####Methods       
>>___
>>[`__init__`](#markdown-header-keythread-init) . . . . . . . . . . . . . . . . . . . . . . . . . . Initialize thread object and its inherited class.
>>___
>>[`__call__`](#markdown-header-keythread-call) . . . . . . . . . . . . . . . . . . . . . . . . . .  Start the event thread method and return thread ID.                           
>>___
>>[*`_test`*](#markdown-header-keythread-_test) . . . . . . . . . . . . . . . . . . . . . . . . . . Try if the class implementation work well.
>>___
>>[`stop`](#markdown-header-keythread-stop) . . . . . . . . . . . . . . . . . . . . . . . . . . Abort thread instance.                            
>>___
>>[`_check_buffer`](#markdown-header-keythread-_check_buffer) . . . . . . . . . . . . . . . . . . . . . . . . . . Check the buffer length for characters.    
>>___
>>[*`_thread_event`*](#markdown-header-keythread-_thread_event) . . . . . . . . . . . . . . . . . . . . . . . . . . Overwrites the *KeyEvent.set_event* method.                           
>>___
>>[*`_runcode`*](#markdown-header-keythread-runcode) . . . . . . . . . . . . . . . . . . . . . . . . . . Main thread event loop method.    

>___
>>####Properties   
>>___
>>[*`keycode`*](#markdown-header-keythread-keycode) . . . . . . . . . . . . . . . . . . . . . . . . . . Property decorator that returns pressed key.

___

##Module 
___
[`ksApp.py`](#markdown-header-ksapp) . . . . . . . . . . . . . . . . . . . . . . . . . . Main module for get input character only if it is in foreground state.

___
>###Class  
>___                                      
>[`KeyInput`](#markdown-header-ksapp-keyinput) . . . . . . . . . . . . . . . . . . . . . . . . . . Base input class.

>___
>>####Methods       
>>___
>>[`__init__`](#markdown-header-keyinput-init) . . . . . . . . . . . . . . . . . . . . . . . . . . Initialize the base instance for the current OS.
>>___
>>[`__call__`](#markdown-header-keyinput-call) . . . . . . . . . . . . . . . . . . . . . . . . . . Return pressed key from keyboard.                          
>>___
>>[*`_test`*](#markdown-header-keyinput-_test) . . . . . . . . . . . . . . . . . . . . . . . . . . Try if the class implementation work well.

>___
>###Class 
>___
>[`KeyEvent`](#markdown-header-kssys-keyevent) . . . . . . . . . . . . . . . . . . . . . . . . . . Return pressed keys in an handler function.

>___
>>####Methods  
>>___
>>[`__init__`](#markdown-header-keyevent-init) . . . . . . . . . . . . . . . . . . . . . . . . . . Initialize itself and the inherited class.
>>___
>>[`__call__`](#markdown-header-keyevent-call) . . . . . . . . . . . . . . . . . . . . . . . . . . Start the key event handler.
>>___
>>[`set_event`](#markdown-header-keyevent-set_event) . . . . . . . . . . . . . . . . . . . . . . . . . . Main event loop method. Override it.
>>___
>>[*`_test`*](#markdown-header-keyevent-_test) . . . . . . . . . . . . . . . . . . . . . . . . . . Try if the class implementation work well.

>___
>###Class 
>___
>[`KeyThread`](#markdown-header-keythread) . . . . . . . . . . . . . . . . . . . . . . . . . . Run a separate thread and return pressed keys. 

>___
>>####Methods       
>>___
>>[`__init__`](#markdown-header-keythread-init) . . . . . . . . . . . . . . . . . . . . . . . . . . Initialize thread object and its inherited class.
>>___
>>[`__call__`](#markdown-header-keythread-call) . . . . . . . . . . . . . . . . . . . . . . . . . .  Start the event thread method and return thread ID.                           
>>___
>>[*`_test`*](#markdown-header-keythread-_test) . . . . . . . . . . . . . . . . . . . . . . . . . . Try if the class implementation work well.
>>___
>>[`stop`](#markdown-header-keythread-stop) . . . . . . . . . . . . . . . . . . . . . . . . . . Abort thread instance.                            
>>___
>>[`_check_buffer`](#markdown-header-keythread-_check_buffer) . . . . . . . . . . . . . . . . . . . . . . . . . . Check the buffer length for characters.    
>>___
>>[*`_thread_event`*](#markdown-header-keythread-_thread_event) . . . . . . . . . . . . . . . . . . . . . . . . . . Overwrites the *KeyEvent.set_event* method.                           
>>___
>>[*`_runcode`*](#markdown-header-keythread-runcode) . . . . . . . . . . . . . . . . . . . . . . . . . . Main thread event loop method.    

>___
>>####Properties   
>>___
>>[*`keycode`*](#markdown-header-keythread-keycode) . . . . . . . . . . . . . . . . . . . . . . . . . . Property decorator that returns pressed key.
                           
___

##Module 
___
[*`ksApplication/AppGetchUnix.py`*](#markdown-header-appgetchunix) . . . . . . . . . . . . . . . . . . . . . . . . . . short description

___
>###Class  
>___                                      
>[*`_GetchUnix`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 

>___
>>####Methods       
>>___
>>[*`__call__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . .                             

___

##Module 
___
[*`ksApplication/AppGetchWindows.py`*](#markdown-header-appgetchwindows) . . . . . . . . . . . . . . . . . . . . . . . . . . short description

___
>###Class  
>___                                      
>[*`_GetchWindows`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 

>___
>>####Methods       
>>___
>>[*`__call__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . .                          

___

##Module 
___
[*`ksSystem/SysGetchWindows.py`*](#markdown-header-sysgetchwindows) . . . . . . . . . . . . . . . . . . . . . . . . . . short description

___
>###Class  
>___                                      
>[*`_GetchWindows`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 

>___
>>####Methods       
>>___
>>[*`__call__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`set_exit`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`_exit_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . .  
>>___
>>[*`key_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`_on_keyboard_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
                          
___

##Module 
___
[*`ksSystem/SysGetchMacCarbon.py`*](#markdown-header-sysgetchmaccarbon) . . . . . . . . . . . . . . . . . . . . . . . . . . short description

___
>###Class  
>___                                      
>[*`_GetchMacCarbon`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 

>___
>>####Methods       
>>___
>>[*`__init__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . .   
>>___
>>[*`__call__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`set_exit`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`key_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
                          
___

##Module 
___
[*`ksSystem/SysGetchOsXCocoa.py`*](#markdown-header-sysgetchosxcocoa) . . . . . . . . . . . . . . . . . . . . . . . . . . short description

___
>###Class  
>___                                      
>[*`_GetchOsXCocoa`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 

>___
>>####Methods       
>>___
>>[*`__init__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`__call__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`_exit_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`_on_keyboard_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`set_exit`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`key_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 

>___
>###Class  
>___                                      
>[*`_AppDelegate`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 

>___
>>####Methods       
>>___
>>[*`applicationDidFinishLaunching_`*]() . . . . . . . . . . . . . . . . . . . . . . . . . .   
>>___
>>[*`__call__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`handler`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 

___

##Module 
___
[*`ksSystem/SysGetchUnix.py`*](#markdown-header-sysgetchunix) . . . . . . . . . . . . . . . . . . . . . . . . . . short description

___
>###Class  
>___                                      
>[*`_GetchUnix`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 

>___
>>####Methods       
>>___
>>[*`__init__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . .  
>>___
>>[*`__call__`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`_exit_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`_on_keyboard_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`set_exit`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
>>[*`key_event`*]() . . . . . . . . . . . . . . . . . . . . . . . . . . 
>>___
                          
___
/#######################################################################################################################
___
##IN-DEPTH DESCRIPTIONS AND EXPAMPLES
___
___

## Modules
___

### ksSys

This module is used for detect any pressed key from any program.
Intercept any pressed key that occurs in the system even if this code is running in the background.
You need to use this module if you are trying to do an alike keylogger program.  
All __call__() methods of this module classes return virual key code and event state code as a tuple.
 
[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksApp

This module is used for intercept input keys only if it is in foreground state.
Detect keys only if its process window is focussed.  
All __call__() methods of this module classes return virual key code and event state code as a tuple.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### SysGetchUnix

[*return to table of contents*](#markdown-header-table-of-contents)
___

### SysGetchOsXCocoa

[*return to table of contents*](#markdown-header-table-of-contents)
___

### SysGetchMacCarbon

[*return to table of contents*](#markdown-header-table-of-contents)
___

### SysGetchWindows

[*return to table of contents*](#markdown-header-table-of-contents)
___

### AppGetchUnix

[*return to table of contents*](#markdown-header-table-of-contents)
___

### AppGetchWindows

[*return to table of contents*](#markdown-header-table-of-contents)
___
___

## Classes
___

### ksSys KeyInput
*From: ksSys*

Base input class.

Should be used if you need as input only a key or character.
Does not echo to the screen.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksSys KeyEvent 
*From: ksSys*

Inherits from [**KeyInput**](#markdown-header-kssys-keyinput) class.

Run [`keyInput.__call__()`](#markdown-header-keyinput-call) method in a loop. Return any pressed key from an handler function. 
The handler loop will be executed under the same main thread.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksSys KeyThread
*From: ksSys*

Used with build-in *threading* package. Should be used when you need a fast input response, independently from the main process execution.
Run and instance of [`KeyEvent`](#markdown-header-keyevent) class in a separate thread and return any pressed key in asynchronous mode. *(best mode)*
Character 27 (default ESC key) for terminate the code. 

[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksApp KeyInput
*From: ksApp*

Base input class.

Should be used if you need as input only a key or character.
Does not echo to the screen.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksApp KeyEvent 
*From: ksSys*

Inherits from [**KeyInput**](#markdown-header-kssys-keyinput) class.

Run [`keyInput.__call__()`](#markdown-header-keyinput-call) method in a loop. Return any pressed key from an handler function. 
The handler loop will be executed under the same main thread.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksApp KeyThread
*From: ksApp*

Used with build-in *threading* package. Should be used when you need a fast input response, independently from the main process execution.
Run and instance of [`KeyYield`](#markdown-header-keyyield) class in a separate thread and return any pressed key in asynchronous mode. *(best mode)*
Character 27 (default ESC key) for terminate the code. 

[*return to table of contents*](#markdown-header-table-of-contents)
___
___

##Methods
___

### KeyInput init
*From: ksSys.KeyInput*
*From: ksApp.KeyInput*

Initialize the base instance for the current OS.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyInput call
*From: ksSys.KeyInput*
*From: ksApp.KeyInput*

Return the pressed key character and exit. 
        
[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyInput _test
*From: ksSys.KeyInput*
*From: ksApp.KeyInput*

Try if the class implementation work well. Print on screen the pressed character and character code. 
The code of this method is as follows:  

        print 'Press a key' 
        code,state = self.__call__()
        print 'you pressed vkey:',self.vkeys_index(code),' with state:',self.KEY_STATE_STRING[state],' and vkey code:',code       
Use this as example for understand how the class work.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent init
*From: ksSys.KeyEvent*
*From: ksApp.KeyInput*

Initialize itself and the inherited class.

Parameters:

- *exitkeycode -* insert an ASCII key number that will be used to stop input keys. Default value is 27 (ESC key)

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent call
*From: ksSys.KeyEvent*
*From: ksApp.KeyInput*

Start the key event handler.

Initialize the event handler and put the [*keyEvent.setEvent()*](#markdown-header-keyevent-setevent) method inside it, then starts it.  
The pressed key code is returned as unicode type in the self.keycode variable.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent set_event
*From: ksSys.KeyEvent*
*From: ksApp.KeyInput*

Override this method if you would to loop inside the handler. Use `self.keycode` inside it for extract the pressed key.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent _test
*From: ksSys.KeyEvent*
*From: ksApp.KeyInput*

Try if the class implementation work well. Print on screen the pressed character and character code.
The code of this method is as follows:  

        print 'Press a key'
        def testEvent():
            code,state = self.keycode
            print 'you pressed vkey:',self.vkeys_index(code),' with state:',self.KEY_STATE_STRING[state],' and vkey code:',code   
        self.set_event=testEvent
        self.__call__()
Use this as example for understand how the class work.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyThread init
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Initialize thread object. 
Check if the system support the build-in threading. 
If thread_id is None create a new thread, check if the given thread id is associated with an existing thread otherwise. 
If this is true join the thread with the class instance.
    
Parameters:

- *thread_id -* the unique thread id number associated with the run threading object.
- *max_buffer -* the maximum characters buffer which serves for transfer characters from the temporary thread to the main thread. 
  This use the *setBuffer()* method. Default value = 1 (character).
- *exitkeycode -* insert an ASCII key number that will be used to stop input keys. Default value is 27 (ESC key).

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyThread call
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Start the thread if it isn't alive and return the thread ID, if it exist returns None instead.

The main thread programm can countinue the execution of its code.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyThread _test
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*   

Try if the class implementation work well. Print on screen the pressed character and character code. 
The code of this method is as follows:  

        print 'Press a key' 
        self.__call__()
        while 1:
            keycode=self.keycode
            if keycode is not None:
                for keyc in keycode:
                    code,state = keyc
                    print 'you pressed vkey:',self.vkeys_index(code),' with state:',self.KEY_STATE_STRING[state],' and vkey code:',code  
Use this as example for understand how the class work.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyThread _check_buffer
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Check the buffer length which serves for transfer characters from the asynchronous thread to the main thread. 

Parameters:

- *max* - The maximum characters buffer. Default value = 1 (character).

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyThread _thread_event
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Core event that overwrites the *KeyEvent.set_event* method. Implemented as Static method.

This method overwrites the KeyEvent.set_event method as key press detection event.
Do not overwrite it unless you know what you're doing. 

Parameters:

- *max* - The maximum characters buffer. Default value = 1 (character).

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyThread _runcode
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

The core of the key thread acquisition code.
Overwrites the threading run() method with the key press detection event.

Do not overwrite it unless you know what you're doing.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyThread stop
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Abort thread instance. *force* parameter set the strenght of abort state (default=0).

Parameters:

- force = 0 - recomended: only verify if the thread is alive and set a stop event in the thread (the thread will close softly).
- force = 1 - not recomended: verify if the thread is alive and if the thread do not join in a few millisecond,
the function send to it and exception that force the abort state (if the thread respond will close softly otherwise,
it will close in the middle of its execution).
- force = 2 - strongly not recomended: verify if the thread is alive and stop it by sending an exception that force the abort
state (it will close in the middle of its execution).
- retry - how many times try to stop the thread and wait it's join.
- wait - waiting time every retry loop in a join state.

[*return to table of contents*](#markdown-header-table-of-contents)
___
___

##Properties
___

### KeyThread keycode
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Return a tuple of pressed keys. The foremost tuple contain all pressed keys since the last iteration.
The pressed keys are made by a tuple with virual key code and event state code as described below:
    ((vkey,state), (vkey,state), (vkey,state), (vkey,state), other keys tuples)
