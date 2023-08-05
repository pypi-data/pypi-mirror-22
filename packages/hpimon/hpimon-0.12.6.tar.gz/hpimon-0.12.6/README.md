# hpimon

This is a realtime monitor of HPI (head position indicator) signals for Elekta MEG systems (TRIUX/Neuromag). It is intended to be used with continuous HPI to detect possible problems during the measurement (e.g. a child withdrawing their head from the helmet). It also monitors the amount of MEG channels that are saturated and thus not contributing any data (due to e.g. large interference signals).

NOTE: still seriously work in progress. If you use this in important measurements, you do so at your own risk.

## Overview

The software relies on the FieldTrip buffer (http://www.fieldtriptoolbox.org/development/realtime/buffer), which is a standard for  streaming of multichannel data into a TCP socket. FieldTrip includes the `neuromag2ft` utility that reads from the Elekta/Neuromag data acquisition into the FieldTrip buffer. hpimon gets data from the FieldTrip buffer and computes the signal-to-noise ratio of HPI signals in realtime.

## Installation

You can run the monitor either on the acquisition workstation (sinuhe), or on another computer. The simplest way is to run on sinuhe.

## Prerequisites

You need to install a Python environment on sinuhe. Anaconda satisfies all requirements and can be installed without root privileges.

Next, unpack FieldTrip into your desired location. After unpacking, you probably need to recompile `neuromag2ft` on sinuhe, which can be done as follows:

```
cd fieldtrip/realtime/src/buffer/src
make clean
make
cd fieldtrip/realtime/src/acquisition/neuromag
make clean
make
```

If compilation succeeds, the neuromag2ft binary should now be available under `fieldtrip/realtime/src/acquisition/neuromag/bin/x86_64-pc-linux-gnu/neuromag2ft`. Check that it runs.

## Initial configuration

Run `python hpimon.py` from a terminal. On the first run, the program will create a new configuration file and abort. Edit the configuration file (`~/.hpimon.cfg`). Edit `server_path` so it points to your `neuromag2ft` binary.

## Running

hpimon needs to be started before you start acquiring data (before you press 'GO' on the acquisition control panel). If you start it while acquiring data, it will start monitoring the next time you press 'GO'.

## Interpreting the output

The software displays dB values for the signal-to-noise ratio of HPI coils, along with corresponding colors. Green means strong signal, yellow means weaker signal (possibly still ok), and red means no HPI signal, or signal too weak. The thresholds and the colors can be adjusted in the configuration file.

If the SNR of a single coil drops down during the measurement, it is possible that the coil has fallen off the subject. There is not much that can be done about this, unless you are ready to take the subject out and digitize the coil locations again. Usually there is some redundancy, i.e. with five coils you can in principle afford to lose two coils and still be able to track the head.

If the SNR of all coils suddenly decreases a lot, this may due to several reasons:

- subject moving further away from the helmet
- a large increase in environmental interference
- continuous HPI accidentally turned off

## Monitoring of saturated channels

The software detects saturated channels by computing standard deviation for each channel using a 50 ms sliding window. If the standard deviation drops below the limits set in the configuration file for any window, the channel is marked as saturated. 

The acceptable limits for the number of saturated channels are set in the configuration file. When the `n_sat_bad` limit is exceeded, the indicator bar is displayed in red color.

## Shutting down the realtime server

It is good to cleanly shut down `neuromag2ft` (by Ctrl-C or SIGTERM signal). Normally hpimon handles this by itself. If it cannot be done (e.g. power failure, or process stopped with SIGKILL), `neuromag2ft` will not have a chance to restore the buffer settings of the data acquisition to their original values, which may possibly cause some trouble later. If in doubt, run `neuromag2ft` manually with the `--fixchunksize` option. Also, restarting the acquisition programs from the maintenance menu will always restore the settings.

## Configuration

The line frequency and HPI frequencies are normally read from the data acquisition config files. You can override them in the hpimon config file, like so:

```
line_freq = 50
hpi_freqs = [293.0, 307.0, 314.0, 321.0, 328.0]
```
`server_opts` are the options passed to `neuromag2ft`. The `chunk_size` option is the size of the data chunk (in samples) that the server requests from the acquisition system. It determines the update frequency of the monitor, e.g. if the chunk is 500 milliseconds, the display will update twice per second. Note that the chunk also affects the raw data display of the acquisition software: the display length must be a multiple of the chunk length. Value of sampling rate / 2 is reasonable, so you get updates twice per second.

If you don't want hpimon to start and stop the server, specify `server_autostart = 0`.

`buffer_poll_interval` refers to the interval for polling the realtime server buffer. Normally should be set smaller than the `chunk_size` option (so that polling happens more often than new data actually arrives).

`win_len` is length of the data used for the computations. It can be longer than `chunk_size`, in which case overlapping chunks are used for the computations. The display is updated whenever new data becomes available (see `chunk_size` above).

## Testing without acquisition 

To test the monitor, you can stream data from a file. This requires `neuromag2ft` version >= 3.0.2. In the config file, specify `server_opts = '--file test_raw.fif'`. Specify also `hpi_freqs` as they are not available via the FieldTrip header. Note that the `--chunksize` option of `neuromag2ft` has no effect when streaming from a file.

## Running on a separate workstation

You need to:

- start the neuromag2ft server yourself on sinuhe (set `server_autostart = 0` in config, so that hpimon will not try to manage it)
- set `hostname = 'sinuhe'` in config (or whatever the hostname of the acquisition computer is in your network)
- open the firewall on sinuhe, or at least tcp port 1972. You can temporarily disable the firewall by issuing the command `/etc/init.d/iptables stop` (be aware of the security implications)

## Command line options

You can enable debug output by starting the software as `hpimon --debug`.

## (Known) issues

The CPU usage seems extremely high, at least according to top. Apparently this is caused by the matrix computations. Not sure if it's a real issue.

The SNR limits are somewhat arbitrary. Effects of different SNR on e.g. MaxFilter should be investigated more carefully.

The frequencies should be read directly from collector via its TCP interface, instead of config files. Not of practical consequence, unless you have a habit of changing HPI frequencies directly via the collector interface.










