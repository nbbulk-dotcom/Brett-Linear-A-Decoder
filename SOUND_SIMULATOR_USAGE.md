# Brett Sound Simulator - Linear A (Minoan Script)

## Overview

The Brett Sound Simulator generates audio files that emulate the estimated tone, intonation, and voice inflections for Linear A (Minoan Script, 1800-1450 BCE) using the Brett Method. This tool brings the voices of ancient Crete to life through frequency-based harmonic analysis and Minoan prosody.

## Features

- **Melodic Intonation**: Undulating patterns for trade and votive texts
- **Voice Profiles**: Male (ritual), Female (administrative), Child (communal/votive)
- **Phoneme Accuracy**: IPA-based mappings with Minoan reconstructions
- **Frequency Analysis**: Brett Method harmonic frequencies (220-494 Hz range)
- **WAV Output**: High-quality 44.1 kHz, 16-bit PCM audio files

## Installation

```bash
pip install numpy scipy pandas pydub
```

## Usage

### Basic Commands

```bash
# Process specific inscription
python brett_sound_simulator.py --inscription HT13

# Custom text
python brett_sound_simulator.py --text "ku ro pa i to"

# Different voice
python brett_sound_simulator.py --text "a sa sa ra me" --voice male

# Process all inscriptions
python brett_sound_simulator.py
```

### Examples

#### HT13 - Libation Formula
```bash
python brett_sound_simulator.py --inscription HT13
```
- **Output**: `audio_output/HT13_linear_a.wav`
- **Reading**: "a-sa-sa-ra-me" (deity name/libation)
- **Voice**: Male (120 Hz, ritual tone)

#### HT85 - Commodity Record
```bash
python brett_sound_simulator.py --inscription HT85
```
- **Output**: `audio_output/HT85_linear_a.wav`
- **Reading**: "pa-i-to ku-ro" (to-Phaistos total)
- **Voice**: Female (200 Hz, administrative)

#### KN IV 01 - Knossos Scepter (2024)
```bash
python brett_sound_simulator.py --inscription KN_IV_01
```
- **Output**: `audio_output/KN_IV_01_linear_a.wav`
- **Reading**: "qa-ki-a-ra" (religious ritual)
- **Voice**: Child (280 Hz, votive tone)

## Phoneme Mapping

| Glyph | IPA | Frequency (Hz) | Duration (s) | Stress | Context |
|-------|-----|----------------|--------------|--------|---------|
| a | a | 440.00 | 0.5 | primary | Common syllable |
| da | da | 293.66 | 0.5 | primary | Deity names |
| te | te | 329.63 | 0.4 | secondary | Transactions |
| me | me | 261.63 | 0.5 | primary | Libations |
| ku | ku | 220.00 | 0.5 | primary | Totals |
| ro | ɾo | 246.94 | 0.5 | primary | Place names |
| pa | pa | 277.18 | 0.5 | primary | Commodities |
| i | i | 493.88 | 0.4 | secondary | Prepositions |
| to | to | 311.13 | 0.5 | primary | Destinations |
| sa | sa | 220.00 | 0.4 | secondary | Offerings |

## Voice Profiles

### Male (Ritual/Priestly)
- **Pitch**: 120 Hz
- **Rate**: 150 wpm
- **Context**: Libation formulas, religious texts
- **Example**: HT13 libation formula

### Female (Administrative/Trade)
- **Pitch**: 200 Hz
- **Rate**: 140 wpm
- **Context**: Commodity records, trade documents
- **Example**: HT85 commodity ledger

### Child (Communal/Votive)
- **Pitch**: 280 Hz
- **Rate**: 180 wpm
- **Context**: Votive offerings, communal texts
- **Example**: KN IV 01 scepter inscription

## Intonation

### Melodic Pattern (Default)

1. **Primary Stress**: Undulating (1.0 ± 0.15 amplitude, 4π cycles)
   - Reflects Minoan trade fluidity
2. **Secondary Stress**: Gentle undulation (1.0 ± 0.08 amplitude, 2π cycles)
3. **Unstressed**: Slight reduction (0.95 amplitude)

## Technical Specifications

- **Format**: WAV, 16-bit PCM
- **Sample Rate**: 44,100 Hz
- **Base Frequency**: 261.63 Hz (Minoan C4)
- **Range**: 220-494 Hz
- **File Size**: 1-5 MB per phrase

## Integration

```python
from brett_sound_simulator import LinearASoundSimulator

simulator = LinearASoundSimulator()
audio = simulator.synthesize_phrase("ku ro pa i to", voice_type='female')
simulator.save_wav(audio, 'output.wav')
```

## References

- SigLA Database (Linear A signs)
- GORILA Corpus (inscriptions)
- Younger (2000) - Linear A phonetics
- Ventris-Chadwick (1973) - Linear B parallels
- Brett, N. (2025) - Linear A Decoder v2.2

## License

MIT License

## Contact

- **GitHub**: [@nbbulk-dotcom](https://github.com/nbbulk-dotcom)
- **Email**: nbbulk@gmail.com

---

**Version**: 1.0  
**Last Updated**: October 18, 2025
