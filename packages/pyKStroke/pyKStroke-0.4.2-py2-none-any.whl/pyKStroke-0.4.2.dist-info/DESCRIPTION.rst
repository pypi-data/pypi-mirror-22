Simple keyboard input hook on multiple platforms that returns a character.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I know that there are others Python packages similar to this on the web, but i make this because my *main goal* would be
to create an **easy-to-use** and **fast-response** keyboard input event hook package that can be adapted to different types of use.

| The main modules are `**ksSys.py** <Reference.md>`__ and `**ksApp.py** <Reference.md>`__.
| The classes directly included in the above modules are the only ones that you can use for input purposes.
| I've tried to use the same interface in both modules classes to achieve an easy interpretation of what they do,
  even if *"under the hood"* is used a different code implementation.
  Both returs a tuple with virual key code and event state code.


