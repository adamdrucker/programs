#!/bin/bash

# this script exists to automatically detect if my headphones are plugged in, and change the audio profile so that audio streams out of the headphones and not the laptop speakers and/or the headphones at the same time. why, you ask? because Fedora41 implemented some dumb Intel/ALSA bullshit that fucked this simple concept up really bad.

CARD="alsa_card.pci-0000_00_1f.3-platform-skl_hda_dsp_generic"
# CARD=$(pactl list cards | grep Name | awk -F: '{print $2}')

# sink names
HEADPHONES_SINK="HiFi__Headphones__sink"
SPEAKER_SINK="HiFi__Speaker__sink"
SPEAKER_PROFILE="HiFi (HDMI1, HDMI2, HDMI3, Mic1, Mic2, Speaker)"
HEADPHONE_PROFILE="HiFi (HDMI1, HDMI2, HDMI3, Headphones, Mic1, Mic2)"

# current sink list
SINKS=$(pactl list short sinks)

if echo "$SINKS" | grep -q "$HEADPHONES_SINK"; then
  echo "Headphone sink detected — setting headphone profile"
  pactl set-card-profile "$CARD" "$HEADPHONE_PROFILE"
elif echo "$SINKS" | grep -q "$SPEAKER_SINK"; then
  echo "Speaker sink detected — setting speaker profile"
  pactl set-card-profile "$CARD" "$SPEAKER_PROFILE"
else
  echo "Neither sink found — no action taken"
fi
