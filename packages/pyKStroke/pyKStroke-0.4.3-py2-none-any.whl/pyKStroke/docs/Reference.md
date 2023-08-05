# API Reference 
*(work in progress)*

*Italic* style words are methods that should be used only for internal package development.  
I report them here for completeness.

___
/#######################################################################################################################
___
## TABLE OF CONTENTS

## Module
___
[`__init__.py`](#markdown-header-init) . . . . . . . . . . . . . . . . . . . . . . . . . . Module where the main code is.

___

## Module 
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
>>[`vkey_index`](#markdown-header-keyinput-vkey_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return a vkey string from vkey code.                            
>>___
>>[`vkeys_index`](#markdown-header-keyinput-vkeys_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return multiple vkey string from vkey code.                            
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
>>[`vkey_index`](#markdown-header-keyinput-vkey_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return a vkey string from vkey code.                            
>>___
>>[`vkeys_index`](#markdown-header-keyinput-vkeys_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return multiple vkey string from vkey code.                            
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
>>[`vkey_index`](#markdown-header-keyinput-vkey_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return a vkey string from vkey code.                            
>>___
>>[`vkeys_index`](#markdown-header-keyinput-vkeys_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return multiple vkey string from vkey code.                            
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

## Module 
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
>>[`vkey_index`](#markdown-header-keyinput-vkey_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return a vkey string from vkey code.                            
>>___
>>[`vkeys_index`](#markdown-header-keyinput-vkeys_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return multiple vkey string from vkey code.                            
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
>>[`vkey_index`](#markdown-header-keyinput-vkey_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return a vkey string from vkey code.                            
>>___
>>[`vkeys_index`](#markdown-header-keyinput-vkeys_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return multiple vkey string from vkey code.                            
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
>>[`vkey_index`](#markdown-header-keyinput-vkey_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return a vkey string from vkey code.                            
>>___
>>[`vkeys_index`](#markdown-header-keyinput-vkeys_index) . . . . . . . . . . . . . . . . . . . . . . . . . . Return multiple vkey string from vkey code.                            
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

## Module 
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

## Module 
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

## Module 
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

## Module 
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

## Module 
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

## Module 
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
## IN-DEPTH DESCRIPTIONS AND EXAMPLES
___
___

## Modules
___

### init

Module where the main code is. 

Attributes: 

- Windows Virtual Keys table with some additions. Original V-Keys table (https://goo.gl/8lk3G8)   

        DEFAULT_WINDOWS_VKEYS = {   
                "LBUTTON":0x01, # (Left mouse button)
                "RBUTTON":0x02, # (Right mouse button)
                "CANCEL":0x03, # (Control-break processing)
                "MBUTTON":0x04, # (Middle mouse button)
                "XBUTTON1":0x05, # (X1 mouse button)
                "XBUTTON2":0x06, # (X2 mouse button)
                "BACK":0x08, # (BACKSPACE key)
                "TAB":0x09, # (TAB key)
                "CLEAR":0x0C, # (CLEAR key)
                "RETURN":0x0D, # (ENTER key)
                "SHIFT":0x10, # (SHIFT key)
                "CONTROL":0x11, # (CTRL key)
                "CTRL":0x11, # (CTRL key. This is not in the original Windows virtual keys table)
                "MENU":0x12, # (ALT key)
                "ALT":0x12, # (ALT key. This is not in the original Windows virtual keys table)
                "PAUSE":0x13, # (PAUSE key)
                "CAPITAL":0x14, # (CAPS LOCK key)
                "CAPS":0x14, # (CAPS LOCK key. This is not in the original Windows virtual keys table)
                "KANA":0x15, # (IME Kana mode)
                "HANGUL":0x15, # (IME Hangul mode)
                "HANGUEL":0x15, # (IME Hangeul mode)
                "JUNJA":0x17, # (IME Jungja mode)
                "FINAL":0x18, # (IME Final mode)
                "KANJI":0x19, # (IME Kanji mode)
                "HANGJA":0x19, # (IME Hangja mode)
                "ESCAPE":0x1b, # (ESC key)
                "ESC":0x1b, # (ESC key. This is not in the original Windows virtual keys table)
                "CONVERT":0x1C, # (IME convert)
                "NONCONVERT":0x1D, # (IME nonconvert)
                "ACCEPT":0x1E, # (IME accept)
                "MODECHANGE":0x1F, # (IME mode change request)
                "SPACE":0x20, # (SPACEBAR key)
                "PRIOR":0x21, # (PAGE UP key)
                "NEXT":0x22, # (PAGE DOWN key)
                "END":0x23, # (END key)
                "HOME":0x24, # (HOME key)
                "LEFT":0x25, # (LEFT ARROW key)
                "UP":0x26, # (UP ARROW key)
                "RIGHT":0x27, # (RIGHT ARROW key)
                "DOWN":0x28, # (DOWN ARROW key)
                "SELECT":0x29, # (SELECT key)
                "PRINT":0x2A, # (PRINT key)
                "EXECUTE":0x2B, # (EXECUTE key)
                "SNAPSHOT":0x2C, # (PRINT SCREEN key)
                "INSERT":0x2D, # (INS key)
                "INS":0x2D, # (INS key. This is not in the original Windows virtual keys table)
                "DELETE":0x2E, # (DEL key)
                "DEL":0x2E, # (DEL key. This is not in the original Windows virtual keys table)
                "HELP":0x2F, # (HELP key)
                "0":0x30, # (0 key)
                "1":0x31, # (1 key)
                "2":0x32, # (2 key)
                "3":0x33, # (3 key)
                "4":0x34, # (4 key)
                "5":0x35, # (5 key)
                "6":0x36, # (6 key)
                "7":0x37, # (7 key)
                "8":0x38, # (8 key)
                "9":0x39, # (9 key)
                "A":0x41, # (A key)
                "B":0x42, # (B key)
                "C":0x43, # (C key)
                "D":0x44, # (D key)
                "E":0x45, # (E key)
                "F":0x46, # (F key)
                "G":0x47, # (G key)
                "H":0x48, # (H key)
                "I":0x49, # (I key)
                "J":0x4A, # (J key)
                "K":0x4B, # (K key)
                "L":0x4C, # (L key)
                "M":0x4D, # (M key)
                "N":0x4E, # (N key)
                "O":0x4F, # (O key)
                "P":0x50, # (P key)
                "Q":0x51, # (Q key)
                "R":0x52, # (R key)
                "S":0x53, # (S key)
                "T":0x54, # (T key)
                "U":0x55, # (U key)
                "V":0x56, # (V key)
                "W":0x57, # (W key)
                "X":0x58, # (X key)
                "Y":0x59, # (Y key)
                "Z":0x5A, # (Z key)
                "LWIN":0x5B, # (Left Windows key)
                "RWIN":0x5C, # (Right Windows key)
                "APPS":0x5D, # (Applications/Menu key)
                "POWER":0x5E, # (Computer Power key)
                "SLEEP":0x5F, # (Computer Sleep key)
                "NUMPAD0":0x60, # (Numeric keypad 0 key)
                "NUMPAD1":0x61, # (Numeric keypad 1 key)
                "NUMPAD2":0x62, # (Numeric keypad 2 key)
                "NUMPAD3":0x63, # (Numeric keypad 3 key)
                "NUMPAD4":0x64, # (Numeric keypad 4 key)
                "NUMPAD5":0x65, # (Numeric keypad 5 key)
                "NUMPAD6":0x66, # (Numeric keypad 6 key)
                "NUMPAD7":0x67, # (Numeric keypad 7 key)
                "NUMPAD8":0x68, # (Numeric keypad 8 key)
                "NUMPAD9":0x69, # (Numeric keypad 9 key)
                "MULTIPLY":0x6A, # (Numeric keypad Multiply key)
                "ADD":0x6B, # (Numeric keypad Add key)
                "SEPARATOR":0x6C, # (Separator key)
                "SUBTRACT":0x6D, # (Numeric keypad Subtract key)
                "DECIMAL":0x6E, # (Numeric keypad Decimal key)
                "DIVIDE":0x6F, # (Numeric keypad Divide key)
                "F1":0x70, # (F1 key)
                "F2":0x71, # (F2 key)
                "F3":0x72, # (F3 key)
                "F4":0x73, # (F4 key)
                "F5":0x74, # (F5 key)
                "F6":0x75, # (F6 key)
                "F7":0x76, # (F7 key)
                "F8":0x77, # (F8 key)
                "F9":0x78, # (F9 key)
                "F10":0x79, # (F10 key)
                "F11":0x7A, # (F11 key)
                "F12":0x7B, # (F12 key)
                "F13":0x7C, # (F13 key)
                "F14":0x7D, # (F14 key)
                "F15":0x7E, # (F15 key)
                "F16":0x7F, # (F16 key)
                "F17":0x80, # (F17 key)
                "F18":0x81, # (F18 key)
                "F19":0x82, # (F19 key)
                "F20":0x83, # (F20 key)
                "F21":0x84, # (F21 key)
                "F22":0x85, # (F22 key)
                "F23":0x86, # (F23 key)
                "F24":0x87, # (F24 key)
                "NUMLOCK":0x90, # (NUM LOCK key)
                "SCROLL":0x91, # (SCROLL LOCK key)
                "OEM_FJ_JISHO":0x92, # (OEM Fj Jisho)
                "OEM_FJ_MASSHOU":0x93, # (OEM Fj Masshou)
                "OEM_FJ_TOUROKU":0x94, # (OEM Fj Touroku)
                "OEM_FJ_LOYA":0x95, # (OEM Fj Loya)
                "OEM_FJ_ROYA":0x96, # (OEM Fj Roya)
                "LSHIFT":0xA0, # (Left SHIFT key)
                "RSHIFT":0xA1, # (Right SHIFT key)
                "LCONTROL":0xA2, # (Left CONTROL key)
                "LCTRL":0xA2, # (Left CONTROL key. This is not in the original Windows virtual keys table)                            
                "RCONTROL":0xA3, # (Right CONTROL key)
                "RCTRL":0xA3, # (Right CONTROL key. This is not in the original Windows virtual keys table)
                "LMENU":0xA4, # (Left ALT key)
                "LALT":0xA4, # (Left ALT key. This is not in the original Windows virtual keys table)
                "RMENU":0xA5, # (Right ALT key OR ALTGR key)                           
                "RALT":0xA5, # (Right ALT key OR ALTGR key. This is not in the original Windows virtual keys table)
                "BROWSER_BACK":0xA6, # (Browser Back key)
                "BROWSER_FORWARD":0xA7, # (Browser Forward key)
                "BROWSER_REFRESH":0xA8, # (Browser Refresh key)
                "BROWSER_STOP":0xA9, # (Browser Stop key)
                "BROWSER_SEARCH":0xAA, # (Browser Search key)
                "BROWSER_FAVORITES":0xAB, # (Browser Favorites key)
                "BROWSER_HOME":0xAC, # (Browser Start/Home key)
                "VOLUME_MUTE":0xAD, # (Volume Mute key)
                "VOLUME_DOWN":0xAE, # (Volume Down key)
                "VOLUME_UP":0xAF, # (Volume Up key)
                "MEDIA_NEXT_TRACK":0xB0, # (Next Track key)
                "MEDIA_PREV_TRACK":0xB1, # (Previous Track key)
                "MEDIA_STOP":0xB2, # (Stop Media key)
                "MEDIA_PLAY_PAUSE":0xB3, # (Play/Pause Media key)
                "LAUNCH_MAIL":0xB4, # (Start Mail key)
                "LAUNCH_MEDIA_SELECT":0xB5, # (Select Media key)
                "LAUNCH_APP1":0xB6, # (Start Aapplication 1 key)
                "LAUNCH_APP2":0xB7, # (Start Application 2 key)
                "OEM_1":0xBA, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ';:' key)
                "OEM_PLUS":0xBB, # (For any country/region, the '+=' key)
                "OEM_COMMA":0xBC, # (For any country/region, the '<,' key)
                "OEM_MINUS":0xBD, # (For any country/region, the '_-' key)
                "OEM_PERIOD":0xBE, # (For any country/region, the '>.' key)
                "OEM_2":0xBF, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '/?' key)
                "OEM_3":0xC0, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '`~' key)
                "ABNT_C1":0xC1, # (ABNT C1)
                "ABNT_C2":0xC2, # (ABNT C1)
                "OEM_4":0xDB, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '[{' key)
                "OEM_5":0xDC, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '\|' key)
                "OEM_6":0xDD, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ']}' key)
                "OEM_7":0xDE, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ''"' key)
                "OEM_8":0xDF, # (Used for miscellaneous characters; it can vary by keyboard.)
                "OEM_AX":0xE1, # (Ax)
                "OEM_102":0xE2, # (Either the '<>' key or the '\|' key on the RT 102-key keyboard)
                "OEM_ICO_HELP":0xE3, # (OEM Ico Help)
                "OEM_ICO_00":0xE4, # (OEM Ico 00)
                "PROCESSKEY":0xE5, # (IME PROCESS key)
                "OEM_ICO_CLEAR":0xE6, # (OEM Ico Clear)
                "PACKET":0xE7, # (Used to pass Unicode characters as if they were keystrokes. Low word 32-bit Virtual Key value used for non-keyboard input methods)
                "SYSRQ":0xE8, # (SysRq for Linux systems. This is not in the original Windows virtual keys table)
                "OEM_RESET":0xE9, # (OEM Reset)
                "OEM_JUMP":0xEA, # (OEM Jump)
                "OEM_PA1":0xEB, # (OEM Pa1)
                "OEM_PA2":0xEC, # (OEM Pa2)
                "OEM_PA3":0xED, # (OEM Pa3)
                "OEM_WSCTRL":0xEE, # (OEM Ws Control)
                "OEM_CUSEL":0xEF, # (OEM CuSel)
                "OEM_ATTN":0xF0, # (Oem Attn)
                "OEM_FINISH":0xF1, # (OEM Finish)
                "OEM_COPY":0xF2, # (OEM Copy)
                "OEM_AUTO":0xF3, # (Auto)
                "OEM_ENLW":0xF4, # (OEM Enlw)
                "OEM_BACKTAB":0xF5, # (Backtab)
                "ATTN":0xF6, # (Attn key)
                "CRSEL":0xF7, # (CrSel key)
                "EXSEL":0xF8, # (ExSel key)
                "EREOF":0xF9, # (Erase EOF key)
                "PLAY":0xFA, # (Play key)
                "ZOOM":0xFB, # (Zoom key)
                "NONAME":0xFC, # (Noname)
                "PA1":0xFD, # (PA1 key)
                "OEM_CLEAR":0xFE, # (OEM Clear key)
                                }    

- This is a table for the US 101-KEY keyboard. This should be changed for each keyboard layout   

        DEFAULT_SCODE_TO_VKEY = { #Scancodes (Extended key)
        # scancodes | vkeys code
                0x01:(0x1b,None), # (ESC)
                0x02:(0x31,None), # (1)
                0x03:(0x32,None), # (2)
                0x04:(0x33,None), # (3)
                0x05:(0x34,None), # (4)
                0x06:(0x35,None), # (5)
                0x07:(0x36,None), # (6)
                0x08:(0x37,None), # (7)
                0x09:(0x38,None), # (8)
                0x0A:(0x39,None), # (9)
                0x0B:(0x30,None), # (0)
                0x0C:(0xBD,None), # (-)
                0x0D:(0xBB,None), # (=)
                0x0E:(0x08,None), # (BKSP)
                0x0F:(0x09,None), # (TAB)
                0x10:(0x51,0xB1), # (Q, PREV TRACK)
                0x11:(0x57,None), # (W)
                0x12:(0x45,None), # (E)
                0x13:(0x52,None), # (R)
                0x14:(0x54,None), # (T)
                0x15:(0x59,None), # (Y)
                0x16:(0x55,None), # (U)
                0x17:(0x49,None), # (I)
                0x18:(0x4F,None), # (O)
                0x19:(0x50,0xB0), # (P, NEXT TRACK)
                0x1A:(0xDB,None), # ([)
                0x1B:(0xDD,None), # (])
                0x1C:(0x0D,0x0D), # (ENTER, KP ENTER)
                0x1D:(0xA2,0xA3), # (L CTRL, R CTRL)
                0x1E:(0x41,None), # (A)
                0x1F:(0x53,None), # (S) 
                0x20:(0x44,0xAD), # (D, MUTE)
                0x21:(0x46,None), # (F, CALC)
                0x22:(0x47,0xB3), # (G, PLAY/PAUSE)
                0x23:(0x48,None), # (H)
                0x24:(0x4A,0xB2), # (J, STOP)
                0x25:(0x4B,None), # (K)
                0x26:(0x4C,None), # (L)
                0x27:(0xBA,None), # (;)
                0x28:(0xDE,None), # (')
                0x29:(0xC0,None), # (`)
                0x2A:(0xA0,0xA0), # (L SHIFT)
                0x2B:(0xDC,None), # (\)
                0x2C:(0x5A,None), # (Z, EJECT)
                0x2D:(0x58,None), # (X)
                0x2E:(0x43,0xAE), # (C, VOL DOWN)
                0x2F:(0x56,None), # (V)
                0x30:(0x42,0xAF), # (B, VOL UP)
                0x31:(0x4E,None), # (N)
                0x32:(0x4D,0xAC), # (M, WEB HOME)
                0x33:(0xBC,None), # (,)
                0x34:(0xBE,None), # (.)
                0x35:(0xBF,0x6F), # (/, KP /)
                0x36:(0xA1,0xA1), # (R SHIFT)
                0x37:(0x6A,0x2A), # (KP *, PRT SCRN/STAMP)
                0x38:(0xA4,0xA5), # (L ALT, R ALT)
                0x39:(0x20,None), # (SPACE)
                0x3A:(0x14,None), # (CAPS LOCK)
                0x3B:(0x70,0x2F), # (F1, HELP)
                0x3C:(0x71,None), # (F2, MUSIC)
                0x3D:(0x72,None), # (F3)
                0x3E:(0x73,None), # (F4)
                0x3F:(0x74,None), # (F5)
                0x40:(0x75,None), # (F6)
                0x41:(0x76,None), # (F7)
                0x42:(0x77,None), # (F8)
                0x43:(0x78,None), # (F9)
                0x44:(0x79,None), # (F10)
                0x45:(0x13,0x90), # (PAUSE, NUM LOCK)
                0x46:(0x91,None), # (SCR LOCK)
                0x47:(0x67,0x24), # (KP 7, HOME)
                0x48:(0x68,0x26), # (KP 8, U ARROW)
                0x49:(0x69,0x21), # (KP 9, PG UP)
                0x4A:(0x6D,None), # (KP -)
                0x4B:(0x64,0x25), # (KP 4, L ARROW)
                0x4C:(0x65,None), # (KP 5, RULE)
                0x4D:(0x66,0x27), # (KP 6, R ARROW)
                0x4E:(0x6B,None), # (KP +) 
                0x4F:(0x61,0x23), # (KP 1, END)
                0x50:(0x62,0x28), # (KP 2, D ARROW)
                0x51:(0x63,0x22), # (KP 3, PG DOWN)
                0x52:(0x60,0x2D), # (KP 0, INSERT)
                0x53:(0x6E,0x2E), # (KP ., DELETE)
                0x54:(0xE8,None), # (SYSRQ) used only in Linux
                0x56:(0xE2,None), # (INT 1) mean interrupt
                0x57:(0x7A,None), # (F11)
                0x58:(0x7B,None), # (F12)
                0x5B:(0x7C,0x5B), # (F13, L WIN)
                0x5C:(0x7D,0x5C), # (F14, R WIN)
                0x5D:(0x7E,0x5D), # (F15, APPS)
                0x5E:(None,0x5E), # (nothing?, POWER)
                0x5F:(None,0x5F), # (nothing?, SLEEP)
                0x63:(0x7F,None), # (F16, WAKE) idk?
                0x64:(0x80,None), # (F17, PICTURES) idk?
                0x65:(0x81,0xAA), # (F18, WEB SEARCH)
                0x66:(0x82,0xAB), # (F19, WEB FAVORITES)
                0x67:(0x83,0xA8), # (F20, WEB REFRESH)
                0x68:(0x84,0xA9), # (F21, WEB STOP)
                0x69:(0x85,0xA7), # (F22, WEB FORWARD)
                0x6A:(0x86,0xA6), # (F23, WEB BACK)
                0x6B:(0x87,None), # (F24, MY PC) idk?
                0x6C:(0x11,0xB4), # (CTRL, EMAIL)
                0x6D:(0xF9,0xB5), # (EREOF/RECRD, VIDEO/MEDIA SELECT)
                0x6F:(0xF2,None), # (COPY/TEST)
                0x70:(0x15,None), # (KATAKANA) not sure of this
                0x71:(0xF6,None), # (ATTN/SYSRQ)
                0x72:(0xF7,None), # (CRSEL)
                0x74:(0xF8,None), # (EXSEL/SETUP)
                0x75:(0xF4,None), # (ENL/HELP)
                0x76:(0x0C,None), # (CLEAR)
                0x77:(0x15,None), # (FURIGANA)
                0x79:(0x19,None), # (KANJI)
                0x7B:(0x15,None), # (HIRAGANA) not sure of this
                0x21D:(0xA2,None), # (windows ALTGR down)
                                }    

- Is used for the escape key   

        DEFAULT_EXIT_KEY_CODE = DEFAULT_WINDOWS_VKEYS.get("ESCAPE") #ESC key    

- Is used as conversion table for the key (press, release) state   

        DEFAULT_KEY_STATE_STRING = ("UP","DOWN")    

[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksSys

This module is used for detect any pressed key from any program. It imports main code from ___init.py__
Intercept any pressed key that occurs in the system even if this code is running in the background.
You need to use this module if you are trying to do an alike keylogger program.  
All __call__() methods of this module classes return virual key code and event state code as a tuple.
 
[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksApp

This module is used for intercept input keys only if it is in foreground state. It imports main code from ___init.py__
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

Attributes:

- *WINDOWS_VKEY -* Windows Virtual Keys table. Dict key is vkey string, dict value is vkey code.
- *SCODE_TO_VKEY -* Scancodes to Virtual Keys association table. Dict key is scan code number, value is a 2-element tuple of vkey codes (normal, extended).
- *KEY_STATE_STRING -* 2-element tuple of key (press and release) state.     

[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksSys KeyEvent 
*From: ksSys*

Inherits from [**KeyInput**](#markdown-header-kssys-keyinput) class.

Run [`keyInput.__call__()`](#markdown-header-keyinput-call) method in a loop. Return any pressed key from an handler function. 
The handler loop will be executed under the same main thread.

Attributes:

- *WINDOWS_VKEY -* Windows Virtual Keys table. Dict key is vkey string, dict value is vkey code.
- *SCODE_TO_VKEY -* Scancodes to Virtual Keys association table. Dict key is scan code number, value is a 2-element tuple of vkey codes (normal, extended).
- *KEY_STATE_STRING -* 2-element tuple of key (press and release) state.     
- *EXIT_KEY_CODE -* Virtual key code that will be used to stop input keys. Default value is 0x1B (ESC key).

[*return to table of contents*](#markdown-header-table-of-contents)
___

### ksSys KeyThread
*From: ksSys*

Used with build-in *threading* package. Should be used when you need a fast input response, independently from the main process execution.
Run and instance of [`KeyEvent`](#markdown-header-keyevent) class in a separate thread and return any pressed key in asynchronous mode. *(best mode)*
Character 27 (default ESC key) for terminate the code. 

Attributes:

- *WINDOWS_VKEY -* Windows Virtual Keys table. Dict key is vkey string, dict value is vkey code.
- *SCODE_TO_VKEY -* Scancodes to Virtual Keys association table. Dict key is scan code number, value is a 2-element tuple of vkey codes (normal, extended).
- *KEY_STATE_STRING -* 2-element tuple of key (press and release) state.     
- *EXIT_KEY_CODE -* Virtual key code that will be used to stop input keys. Default value is 0x1B (ESC key).

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

## Methods
___

### KeyInput init
*From: ksSys.KeyInput*
*From: ksApp.KeyInput*

Initialize the base instance for the current OS.

Parameters:

- *windowsVKeysTable -* Use custom Virtual key table. Associate with WINDOWS_VKEYS attribute.
- *scancodeToVKeysTable -* Use custom Scancode Virtual key table. Associate with SCODE_TO_VKEY attribute.
- *keyStateString -* Use custom state string. Associate with KEY_STATE_STRING attribute.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyInput call
*From: ksSys.KeyInput*
*From: ksApp.KeyInput*

Return the pressed key character and exit. 
        
[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyInput vkey_index
*From: ksSys.KeyInput*
*From: ksApp.KeyInput*

Return the string representation of the windows virtual keys code. Only the first key occurrence is returned as a one string list.                           

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyInput vkeys_index
*From: ksSys.KeyInput*
*From: ksApp.KeyInput*

Return the string representation of the windows virtual keys code. Multiple keys can be returned into a list of strings.

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
*From: ksApp.KeyEvent*

Initialize itself and the inherited class.

Parameters:

- *exitkeycode -* Use custom exit code. Associated with EXIT_KEY_CODE attribute.
- *windowsVKeysTable -* Use custom Virtual key table. Associate with WINDOWS_VKEYS attribute.
- *scancodeToVKeysTable -* Use custom Scancode Virtual key table. Associate with SCODE_TO_VKEY attribute.
- *keyStateString -* Use custom state string. Associate with KEY_STATE_STRING attribute.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent call
*From: ksSys.KeyEvent*
*From: ksApp.KeyEvent*

Start the key event handler.

Initialize the event handler and put the [*keyEvent.setEvent()*](#markdown-header-keyevent-setevent) method inside it, then starts it.  
The pressed key code is returned as unicode type in the self.keycode variable.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent vkey_index
*From: ksSys.KeyEvent*
*From: ksApp.KeyEvent*

Return the string representation of the windows virtual keys code. Only the first key occurrence is returned as a one string list.                           

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent vkeys_index
*From: ksSys.KeyEvent*
*From: ksApp.KeyEvent*

Return the string representation of the windows virtual keys code. Multiple keys can be returned into a list of strings.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent set_event
*From: ksSys.KeyEvent*
*From: ksApp.KeyEvent*

Override this method if you would to loop inside the handler. Use `self.keycode` inside it for extract the pressed key.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent _test
*From: ksSys.KeyEvent*
*From: ksApp.KeyEvent*

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
- *exitkeycode -* Use custom exit code. Associated with EXIT_KEY_CODE attribute.
- *windowsVKeysTable -* Use custom Virtual key table. Associate with WINDOWS_VKEYS attribute.
- *scancodeToVKeysTable -* Use custom Scancode Virtual key table. Associate with SCODE_TO_VKEY attribute.
- *keyStateString -* Use custom state string. Associate with KEY_STATE_STRING attribute.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyThread call
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Start the thread if it isn't alive and return the thread ID, if it exist returns None instead.

The main thread programm can countinue the execution of its code.

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent vkey_index
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Return the string representation of the windows virtual keys code. Only the first key occurrence is returned as a one string list.                           

[*return to table of contents*](#markdown-header-table-of-contents)
___

### KeyEvent vkeys_index
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Return the string representation of the windows virtual keys code. Multiple keys can be returned into a list of strings.

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

## Properties
___

### KeyThread keycode
*From: ksSys.KeyThread*
*From: ksApp.KeyThread*

Return a tuple of pressed keys. The foremost tuple contain all pressed keys since the last iteration.
The pressed keys are made by a tuple with virual key code and event state code as described below:   

        ((vkey,state), (vkey,state), (vkey,state), (vkey,state), other keys tuples)    
