/* this is a README file */
/* nah it's actually my scratch paper l_o_l */

Goal:
    build a server that records some system output and stream it to the client

Technology Stack:
    something that routes an output device to an input device (I'm using VB Audio Cable)
    python sounddevice library
    flask (server)

Overall Design / Architecture:
    set virtual audio cable to route some output to a input device
    use sounddevice to record sound from this device
    the server reads from the recorded audio buffer
        server needs to transform np array to an actual audio stream
    sends it to the client (on request)
    /* the client uses browser to get sound information */

Scratch---------------------------------------------------------------------------------------
alright let's start from a playback app
    listen to an input device
    play it to an output device

There's a problem: the freaking Sounddevice package only work with directsound devices

Yep basic input to output is done.
Next up: forward sound stream to client

according to valuable research, forwarding should happen within the callback function
besides just copying everything from indata to outdata, it can do some other tricks to manipulate the audio data

        side note: the freaking package has almost 0.5 seconds of latency

I need to find out what data structure "indata" in the callback function uses
