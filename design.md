App is a collection of Screens
Screen has a Root Component (View) and some State (Model)

Screen Lifecycle:

```
{Load/Resume}
   `--> {Activate}                                                   (transition)
           `--> {Async Update} --> {Render} --> [Keypress] - <Classify> --> {Suspend}
                        ^                                     |  |
                        |                             (async) |  |
                        |`-----------{Register}--------------'   | (continue)
                        |                                        |
                         `--------------------------------------'
```

There are 3 different types of signals that can be emitted from the `Keypress` step.

1.  `continue` (default)
    This signal indicates that the Keypress handler has successfully handled the event and no
    further processing is required.  If no key is consumed, this signal is emitted by default.
2.  `async`
    This signal indicates that the Keypress has triggered some asynchronous work.  That work
    will be `Register`ed, see the section on `Async Update`
3.  `transition`
    This signal indicates that the screen should suspend and transition to a new target screen

Input Handling:
```
                                Keypress            Result
                                   |                   ^
.--- Application ------------------|-------------------|----------------------------.
|                                  v                   |                            |
|                             on_keypress()       .----+---------------.            |
|                                  |        (yes) |    |               |            |
|                              <handled?> --------+    |               |            |
|                                  |              | after_keypress()   |            |
|                                  |  (no)        |    ^               |            |
|  .--- Active Screen -------------|--------------|----|---------------|---------.  |
|  |                               |              |    |               |         |  |
|  |                               v              |    |  (no)         |         |  |
|  |                          on_keypress()       |    |         (yes) |         |  |
|  |                               |        (yes) |  <handled?> -------+         |  |
|  |                           <handled?> --------+    |               |         |  |
|  |                               |              | after_keypress()   |         |  |
|  |                               |  (no)        |    ^               |         |  |
|  |  .--- Focused Component ------|--------------|----|---------------|------.  |  |
|  |  |    (recursive)             |              |    |               |      |  |  |
|  |  |                            v              |    |  (no)         |      |  |  |
|  |  |                       on_keypress()       |    |         (yes) |      |  |  |
|  |  |                            |        (yes) |  <handled?> -------'      |  |  |
|  |  |                        <handled?> --------'    |                      |  |  |
|  |  |                            |                after_keypress()          |  |  |
|  |  |                            |  (no)             ^                      |  |  |
|  |  |                            |                   |                      |  |  |
|  |  |                             `------------------'                      |  |  |
|  |  |                                                                       |  |  |
|  |   `----------------------------------------------------------------------'  |  |
|  |                                                                             |  |
|   `----------------------------------------------------------------------------'  |
|                                                                                   |
 `----------------------------------------------------------------------------------'
```
