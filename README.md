# sunshine

This is my set of tools for managing growbox with Raspberry and Python.

The most interesting part in my opinion is solution for fan speed management.
I failed with dimmer-moniles and ended with set of capacitors connected thru
relays and in parallel, so I can change Capacity turning on and off some
capacitors. I made some tests and chosen handy nominals of capacitors to
have near 10 steps between fully off and bypass. Keep in mind that lowest
speed fan can handle can be lower than the lowest speed it can start.

# Configuration:

Set time of sunrise and lenght of daytime in `conf.ini` 

Set fan speed like this:

```
echo '4' > /opt/fan_speed_day
echo '2' > /opt/fan_speed_night
```
(this can be changed without service restart or reload.
Changes in ini-file will require restart)