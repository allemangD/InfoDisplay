#!/usr/bin/env python

from subprocess import Popen

from pydub import AudioSegment

bell1path = "res/wav/bellhit1.wav"
bell2path = "res/wav/bellhit2.wav"
bell3path = "res/wav/bellhit3.wav"
bell4path = "res/wav/bellhit4.wav"
bell5path = bell4path

g = AudioSegment.from_file(bell1path)
e = AudioSegment.from_file(bell2path)
f = AudioSegment.from_file(bell3path)
b = AudioSegment.from_file(bell4path)
e3 = AudioSegment.from_file(bell5path)

try:
    horn = AudioSegment.from_file("/home/pi/sound/traphorn.wav")
except FileNotFoundError:
    horn = AudioSegment.empty()

phrase1 = [(g, .25), (f, .25), (e, .25), (b, .50)]
phrase2 = [(e, .25), (g, .25), (f, .25), (b, .50)]
phrase3 = [(e, .25), (f, .25), (g, .25), (e, .50)]
phrase4 = [(g, .25), (e, .25), (f, .25), (b, .50)]
phrase5 = [(b, .25), (f, .25), (g, .25), (e, .50)]
rest = [(AudioSegment.empty(), .50)]
strike = [(e3, .75)]
trap_horn = [(horn, 0)]

whole_time = 3000


def chime_length(chime):
    return sum(c[1] for c in chime) * whole_time + len(chime[-1][0])


def play(audio):
    audio.export('/tmp/clock_chime.wav', 'wav')
    Popen(['aplay', '/tmp/clock_chime.wav', '-q'])


def play_phrase(phrase):
    audio = AudioSegment.silent(chime_length(phrase))
    time = 0

    for a, t in phrase:
        audio = audio.overlay(a, int(time))
        time += t * whole_time

    play(audio)


last_chime = None


def play_chime(hour, minute):
    global last_chime
    this_chime = hour, minute
    if last_chime == this_chime:
        return
    last_chime = this_chime

    chime = []

    if hour == 16 and minute == 20:
        chime = trap_horn

    if minute == 15:
        chime = phrase1
    if minute == 30:
        chime = phrase2 + phrase3
    if minute == 45:
        chime = phrase4 + phrase5 + phrase1
    if minute == 0:
        if hour > 12:
            hour -= 12
        if hour == 0:
            hour = 12
        chime = phrase2 + phrase3 + phrase4 + phrase5 + rest + strike * hour

    if not chime:
        return

    play_phrase(chime)


if __name__ == '__main__':
    play_chime(2, 00)
