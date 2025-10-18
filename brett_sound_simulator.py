#!/usr/bin/env python3
"""
Brett Sound Simulator - Linear A (Minoan Script)
=================================================
Generates audio files that emulate the estimated tone, intonation, and voice 
inflections for Linear A using the Brett Method.

Created by: Nicolas of the Family Brett
Date: October 18, 2025
License: MIT
"""

import numpy as np
from scipy.io import wavfile
import pandas as pd
import os
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
import argparse

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available. Install with: pip install pydub")

@dataclass
class VoiceProfile:
    """Voice profile configuration"""
    type: str  # 'male', 'female', 'child'
    pitch: float  # Hz
    rate: int  # Words per minute
    description: str

@dataclass
class PhonemeData:
    """Phoneme data structure"""
    glyph: str
    ipa: str
    pitch: float
    duration: float
    stress: str

class LinearASoundSimulator:
    """Sound simulator for Linear A (Minoan Script)"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.voice_profiles = {
            'male': VoiceProfile('male', 120, 150, 'Ritual/priestly tone'),
            'female': VoiceProfile('female', 200, 140, 'Administrative/trade tone'),
            'child': VoiceProfile('child', 280, 180, 'Communal/votive tone')
        }
        self.base_freq = 261.63  # Minoan-inspired C4
        
    def load_phoneme_map(self, file_path: str) -> Dict[str, PhonemeData]:
        """Load phoneme-to-IPA mapping"""
        if not os.path.exists(file_path):
            return self._create_default_phoneme_map()
        
        df = pd.read_csv(file_path)
        phoneme_map = {}
        for _, row in df.iterrows():
            phoneme_map[row['glyph']] = PhonemeData(
                glyph=row['glyph'],
                ipa=row['ipa'],
                pitch=row['pitch'],
                duration=row['duration'],
                stress=row['stress']
            )
        return phoneme_map
    
    def _create_default_phoneme_map(self) -> Dict[str, PhonemeData]:
        """Create default phoneme mappings for Linear A"""
        default_phonemes = {
            'a': PhonemeData('a', 'a', 440.00, 0.5, 'primary'),
            'da': PhonemeData('da', 'da', 293.66, 0.5, 'primary'),
            'te': PhonemeData('te', 'te', 329.63, 0.4, 'secondary'),
            'me': PhonemeData('me', 'me', 261.63, 0.5, 'primary'),
            'ku': PhonemeData('ku', 'ku', 220.00, 0.5, 'primary'),
            'ro': PhonemeData('ro', 'ɾo', 246.94, 0.5, 'primary'),
            'pa': PhonemeData('pa', 'pa', 277.18, 0.5, 'primary'),
            'i': PhonemeData('i', 'i', 493.88, 0.4, 'secondary'),
            'to': PhonemeData('to', 'to', 311.13, 0.5, 'primary'),
            'sa': PhonemeData('sa', 'sa', 220.00, 0.4, 'secondary')
        }
        return default_phonemes
    
    def generate_tone(self, freq: float, duration: float) -> np.ndarray:
        """Generate sine wave for phoneme"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = np.sin(2 * np.pi * freq * t)
        
        # Apply envelope
        envelope = np.ones_like(tone)
        fade_samples = int(0.01 * self.sample_rate)
        if len(tone) > 2 * fade_samples:
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return tone * envelope
    
    def apply_melodic_intonation(self, audio: np.ndarray, stress: str) -> np.ndarray:
        """Apply melodic undulating intonation for trade/votive texts"""
        samples = len(audio)
        
        if stress == 'primary':
            # Undulating pattern for emphasized syllables
            curve = 1 + 0.15 * np.sin(np.linspace(0, 4 * np.pi, samples))
        elif stress == 'secondary':
            # Gentle undulation for secondary stress
            curve = 1 + 0.08 * np.sin(np.linspace(0, 2 * np.pi, samples))
        else:
            # Slight variation for unstressed
            curve = np.ones(samples) * 0.95
        
        return audio * curve
    
    def synthesize_phrase(self, text: str, voice_type: str = 'child', 
                         phoneme_map: Optional[Dict] = None) -> np.ndarray:
        """Synthesize a phrase into audio"""
        if phoneme_map is None:
            phoneme_map = self._create_default_phoneme_map()
        
        audio_segments = []
        syllables = text.replace('-', ' ').split()
        
        for syllable in syllables:
            if syllable in phoneme_map:
                phoneme = phoneme_map[syllable]
                
                # Generate tone
                tone = self.generate_tone(phoneme.pitch, phoneme.duration)
                
                # Apply melodic intonation
                tone = self.apply_melodic_intonation(tone, phoneme.stress)
                
                # Adjust for voice profile
                voice = self.voice_profiles[voice_type]
                pitch_factor = voice.pitch / 280  # Normalize to child baseline
                tone = self._adjust_pitch(tone, pitch_factor)
                
                audio_segments.append(tone)
                
                # Add brief silence
                silence = np.zeros(int(0.1 * self.sample_rate))
                audio_segments.append(silence)
        
        if audio_segments:
            combined = np.concatenate(audio_segments)
            max_val = np.max(np.abs(combined))
            if max_val > 0:
                combined = combined / max_val * 0.8
            return combined
        return np.array([])
    
    def _adjust_pitch(self, audio: np.ndarray, factor: float) -> np.ndarray:
        """Adjust pitch by resampling"""
        if factor == 1.0:
            return audio
        
        indices = np.arange(0, len(audio), factor)
        indices = indices[indices < len(audio)].astype(int)
        return audio[indices]
    
    def save_wav(self, audio: np.ndarray, output_path: str):
        """Save audio as WAV file"""
        audio_int = (audio * 32767).astype(np.int16)
        wavfile.write(output_path, self.sample_rate, audio_int)
        print(f"Saved audio to: {output_path}")
    
    def process_inscription(self, inscription_id: str, output_dir: str = 'audio_output'):
        """Process a decoded inscription into audio"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Example inscriptions
        inscriptions = {
            'HT13': {
                'text': 'a sa sa ra me',
                'voice': 'male',
                'context': 'Libation formula (Haghia Triada)'
            },
            'HT85': {
                'text': 'pa i to ku ro',
                'voice': 'female',
                'context': 'Commodity record (Haghia Triada)'
            },
            'KN_IV_01': {
                'text': 'qa ki a ra',
                'voice': 'child',
                'context': 'Religious ritual (Knossos scepter, 2024)'
            }
        }
        
        if inscription_id not in inscriptions:
            print(f"Inscription {inscription_id} not found")
            return
        
        insc = inscriptions[inscription_id]
        print(f"Processing {inscription_id}: {insc['text']}")
        print(f"Context: {insc['context']}")
        print(f"Voice: {insc['voice']}")
        
        audio = self.synthesize_phrase(insc['text'], insc['voice'])
        output_path = os.path.join(output_dir, f"{inscription_id}_linear_a.wav")
        self.save_wav(audio, output_path)
        
        return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Brett Sound Simulator for Linear A (Minoan Script)'
    )
    parser.add_argument('--inscription', '-i', help='Inscription ID (HT13, HT85, KN_IV_01)')
    parser.add_argument('--text', '-t', help='Custom text to synthesize')
    parser.add_argument('--voice', '-v', choices=['male', 'female', 'child'], 
                       default='child', help='Voice profile')
    parser.add_argument('--output', '-o', default='audio_output', 
                       help='Output directory')
    parser.add_argument('--phoneme-map', '-p', help='Path to phoneme CSV file')
    
    args = parser.parse_args()
    
    simulator = LinearASoundSimulator()
    
    if args.inscription:
        simulator.process_inscription(args.inscription, args.output)
    elif args.text:
        os.makedirs(args.output, exist_ok=True)
        
        phoneme_map = None
        if args.phoneme_map:
            phoneme_map = simulator.load_phoneme_map(args.phoneme_map)
        
        print(f"Synthesizing: {args.text}")
        print(f"Voice: {args.voice}")
        
        audio = simulator.synthesize_phrase(args.text, args.voice, phoneme_map)
        output_path = os.path.join(args.output, f"custom_linear_a.wav")
        simulator.save_wav(audio, output_path)
    else:
        print("Processing all available inscriptions...")
        for insc_id in ['HT13', 'HT85', 'KN_IV_01']:
            simulator.process_inscription(insc_id, args.output)

if __name__ == "__main__":
    main()
