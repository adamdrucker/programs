#!/bin/bash

# need to find the current profile, then need to 

CARD="alsa_card.pci-0000_00_1f.3-platform-skl_hda_dsp_generic"
HEADPHONES_PROFILE="HiFi (HDMI1, HDMI2, HDMI3, Headphones, Mic1, Mic2)"
SPEAKER_PROFILE="HiFi (HDMI1, HDMI2, HDMI3, Mic1, Mic2, Speaker)"

#CURRENT_PROFILE=$(pactl list cards | grep "Active Profile")

get_jack_state() {
  amixer -c 0 cget numid=15 | grep -o 'values=on\|values=off' | cut -d= -f2
}

alsactl monitor | while read -r line; do
  [[ "$line" != *"Headphone Jack"* ]] && continue

  JACK_STATE=$(get_jack_state)

  if [[ "$JACK_STATE" == "on" && "$CURRENT" != "headphones" ]]; then
    echo "Headphones plugged in — switching to headphone profile"
    pactl set-card-profile "$CARD" "$HEADPHONES_PROFILE"
    CURRENT="headphones"
  elif [[ "$JACK_STATE" == "off" && "$CURRENT" != "speakers" ]]; then
    echo "Headphones unplugged — switching to speaker profile"
    pactl set-card-profile "$CARD" "$SPEAKER_PROFILE"
    CURRENT="speakers"
  fi
done


#if [[ "$CURRENT_PROFILE" == "HiFi" && "$CURRENT_PROFILE" != *Speaker* ]]; then
#  echo "Switching to Speaker profile"
#  pactl set-card-profile "$CARD" "HiFi (HDMI1, HDMI2, HDMI3, Mic1, Mic2, Speaker)"
#else
#  echo "Switching to Headphones profile"
#  pactl set-card-profile "$CARD" "HiFi (HDMI1, HDMI2, HDMI3, Headphones, Mic1, Mic2)"
#fi

