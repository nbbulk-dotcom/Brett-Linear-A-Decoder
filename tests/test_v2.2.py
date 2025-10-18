"""
Test suite for Linear A Decoder v2.2

Tests cover:
- Sign lookup and phonetic reading
- Confidence calculation
- Harmonic analysis
- Pattern recognition
- Export functionality
- Visualization generation
"""

import pytest
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_linear_a_decoder_v2_2 import (
    EnhancedLinearADecoder,
    LinearASign,
    SignType,
    EmotionalState,
    VocalEmotionalAnalysis,
    PhoneticReading,
    TabletReading
)


@pytest.fixture
def decoder():
    """Create decoder instance for testing."""
    return EnhancedLinearADecoder()


class TestSignLookup:
    """Test sign lookup and phonetic reading."""
    
    def test_verified_sign_lookup(self, decoder):
        """Test lookup of verified sign."""
        reading = decoder.get_phonetic_reading('AB08')
        assert reading.phonetic == 'a'
        assert reading.confidence >= 0.90
        assert reading.sign == 'AB08'
    
    def test_multiple_sign_lookup(self, decoder):
        """Test multiple sign lookups."""
        signs = ['AB01', 'AB04', 'AB08', 'AB13']
        expected = ['da', 'te', 'a', 'me']
        
        for sign_id, expected_phonetic in zip(signs, expected):
            reading = decoder.get_phonetic_reading(sign_id)
            assert reading.phonetic == expected_phonetic
    
    def test_logogram_lookup(self, decoder):
        """Test logogram lookup."""
        reading = decoder.get_phonetic_reading('AB120')
        assert '[WHEAT]' in reading.phonetic
        assert reading.confidence >= 0.85
    
    def test_fraction_lookup(self, decoder):
        """Test fraction marker lookup."""
        reading = decoder.get_phonetic_reading('AB302')
        assert '1/2' in reading.phonetic
        assert reading.confidence >= 0.90
    
    def test_undeciphered_sign(self, decoder):
        """Test undeciphered sign handling."""
        reading = decoder.get_phonetic_reading('AB999')
        assert 'UNDECIPHERED' in reading.phonetic
        assert reading.confidence == 0.0


class TestVocalEmotionalAnalysis:
    """Test vocal and emotional analysis."""
    
    def test_low_frequency_analysis(self, decoder):
        """Test low frequency (male fundamental range)."""
        analysis = decoder.analyze_vocal_emotional(150.0)
        assert analysis.vocal_range == 'male_fundamental'
        assert analysis.emotional_state in [EmotionalState.LOW_EFFORT, EmotionalState.NEUTRAL_CALM]
    
    def test_mid_frequency_analysis(self, decoder):
        """Test mid frequency (female fundamental range)."""
        analysis = decoder.analyze_vocal_emotional(261.63)
        assert analysis.vocal_range in ['female_fundamental', 'child']
        assert analysis.emotional_state == EmotionalState.NEUTRAL_CALM
    
    def test_high_frequency_analysis(self, decoder):
        """Test high frequency (child/falsetto range)."""
        analysis = decoder.analyze_vocal_emotional(440.0)
        assert analysis.vocal_range in ['child', 'falsetto']
        assert analysis.emotional_state in [EmotionalState.ACTIVE_ENGAGED, EmotionalState.ELEVATED_INVOCATION]
    
    def test_intensity_calculation(self, decoder):
        """Test intensity normalization."""
        low_analysis = decoder.analyze_vocal_emotional(100.0)
        high_analysis = decoder.analyze_vocal_emotional(500.0)
        
        assert 0.0 <= low_analysis.intensity_level <= 1.0
        assert 0.0 <= high_analysis.intensity_level <= 1.0
        assert high_analysis.intensity_level > low_analysis.intensity_level


class TestHarmonicAnalysis:
    """Test Brett Method harmonic analysis."""
    
    def test_octave_detection(self, decoder):
        """Test octave relationship detection."""
        frequencies = [220.0, 440.0, 880.0]
        harmonics = decoder._harmonic_analysis(frequencies)
        
        assert len(harmonics['octaves']) >= 2
        for octave in harmonics['octaves']:
            assert 1.9 <= octave['ratio'] <= 2.1
    
    def test_fifth_detection(self, decoder):
        """Test perfect fifth detection."""
        frequencies = [293.66, 440.0]  # D to A (perfect fifth)
        harmonics = decoder._harmonic_analysis(frequencies)
        
        assert len(harmonics['fifths']) >= 1
        for fifth in harmonics['fifths']:
            assert 1.4 <= fifth['ratio'] <= 1.6
    
    def test_no_harmonics(self, decoder):
        """Test frequencies with no harmonic relationships."""
        frequencies = [100.0, 111.0, 123.0]
        harmonics = decoder._harmonic_analysis(frequencies)
        
        assert len(harmonics['octaves']) == 0
        assert len(harmonics['fifths']) == 0
    
    def test_complex_harmonic_set(self, decoder):
        """Test complex set with multiple harmonics."""
        frequencies = [220.0, 293.66, 329.63, 440.0, 523.25]
        harmonics = decoder._harmonic_analysis(frequencies)
        
        total_harmonics = (len(harmonics['octaves']) + 
                          len(harmonics['fifths']) + 
                          len(harmonics['fourths']))
        assert total_harmonics >= 3


class TestConfidenceCalculation:
    """Test multi-factor confidence calculation."""
    
    def test_high_confidence_calculation(self, decoder):
        """Test high confidence scenario."""
        conf = decoder.calculate_multi_factor_confidence(
            phonetic_conf=0.92,
            contextual_strength='strong',
            harmonic_consistency='consistent',
            pattern_occurrences=89
        )
        
        assert conf['total_confidence'] >= 0.80
        assert conf['phonetic'] == 0.92
        assert conf['contextual'] == 0.95
        assert conf['harmonic'] == 0.90
    
    def test_moderate_confidence_calculation(self, decoder):
        """Test moderate confidence scenario."""
        conf = decoder.calculate_multi_factor_confidence(
            phonetic_conf=0.75,
            contextual_strength='moderate',
            harmonic_consistency='partial',
            pattern_occurrences=25
        )
        
        assert 0.60 <= conf['total_confidence'] < 0.80
        assert conf['contextual'] == 0.75
        assert conf['harmonic'] == 0.70
    
    def test_low_confidence_calculation(self, decoder):
        """Test low confidence scenario."""
        conf = decoder.calculate_multi_factor_confidence(
            phonetic_conf=0.50,
            contextual_strength='weak',
            harmonic_consistency='minimal',
            pattern_occurrences=5
        )
        
        assert conf['total_confidence'] < 0.70
        assert conf['contextual'] == 0.50
        assert conf['harmonic'] == 0.50


class TestPatternRecognition:
    """Test pattern and formula recognition."""
    
    def test_libation_formula_recognition(self, decoder):
        """Test recognition of a-sa-sa-ra-me libation formula."""
        phonetics = ['a', 'sa', 'sa', 'ra', 'me']
        patterns = decoder.recognize_patterns(phonetics)
        
        formula_matches = [p for p in patterns if p['type'] == 'formula_match']
        assert len(formula_matches) > 0
        
        libation = [p for p in formula_matches if 'libation' in p['name'].lower()]
        assert len(libation) > 0
    
    def test_total_formula_recognition(self, decoder):
        """Test recognition of ku-ro total formula."""
        phonetics = ['ku', 'ro']
        patterns = decoder.recognize_patterns(phonetics)
        
        formula_matches = [p for p in patterns if p['type'] == 'formula_match']
        total_formula = [p for p in formula_matches if 'total' in p['name'].lower()]
        assert len(total_formula) > 0
    
    def test_semantic_field_recognition(self, decoder):
        """Test semantic field recognition."""
        phonetics = ['[WHEAT]', '[WINE]', '1/2']
        patterns = decoder.recognize_patterns(phonetics)
        
        assert len(patterns) > 0


class TestTabletReading:
    """Test complete tablet reading process."""
    
    def test_ht13_reading(self, decoder):
        """Test reading of HT13 (libation formula)."""
        reading = decoder.read_tablet('HT13')
        
        assert reading.tablet_id == 'HT13'
        assert len(reading.phonetic_reading) == 5
        assert reading.confidence_metrics['total_confidence'] >= 0.80
        assert 'a-sa-sa-ra-me' in reading.interpretation or 'a sa sa ra me' in reading.interpretation
    
    def test_ht85_reading(self, decoder):
        """Test reading of HT85 (large commodity record)."""
        reading = decoder.read_tablet('HT85')
        
        assert reading.tablet_id == 'HT85'
        assert len(reading.phonetic_reading) > 5
        assert reading.confidence_metrics['total_confidence'] >= 0.70
        assert len(reading.semantic_hypotheses) > 0
    
    def test_invalid_tablet(self, decoder):
        """Test handling of invalid tablet ID."""
        with pytest.raises(ValueError):
            decoder.read_tablet('INVALID_TABLET')
    
    def test_reading_components(self, decoder):
        """Test that reading contains all required components."""
        reading = decoder.read_tablet('HT13')
        
        assert hasattr(reading, 'phonetic_reading')
        assert hasattr(reading, 'syllabic_analysis')
        assert hasattr(reading, 'vocal_emotional_profile')
        assert hasattr(reading, 'semantic_hypotheses')
        assert hasattr(reading, 'confidence_metrics')
        assert hasattr(reading, 'interpretation')


class TestSyllabicAnalysis:
    """Test syllabic structure analysis."""
    
    def test_cv_structure_detection(self, decoder):
        """Test CV structure detection."""
        phonetics = ['pa', 'sa', 'ra']
        analysis = decoder.analyze_syllabic_structure(phonetics)
        
        for syl in analysis:
            assert syl.phonetic_structure == 'CV'
    
    def test_vowel_structure_detection(self, decoder):
        """Test vowel-only structure detection."""
        phonetics = ['a', 'i', 'e']
        analysis = decoder.analyze_syllabic_structure(phonetics)
        
        for syl in analysis:
            assert syl.phonetic_structure == 'V'
    
    def test_word_boundary_detection(self, decoder):
        """Test word boundary likelihood."""
        phonetics = ['pa', '[WHEAT]', 'ku', 'ro']
        analysis = decoder.analyze_syllabic_structure(phonetics)
        
        wheat_analysis = analysis[1]
        assert wheat_analysis.word_boundary_likelihood >= 0.80


class TestExportFunctionality:
    """Test export and report generation."""
    
    def test_json_export(self, decoder):
        """Test JSON export functionality."""
        reading = decoder.read_tablet('HT13')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            decoder.export_readings(filepath, [reading])
            
            assert os.path.exists(filepath)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert 'HT13' in data
            assert 'phonetic' in data['HT13']
            assert 'confidence' in data['HT13']
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_markdown_report(self, decoder):
        """Test Markdown report generation."""
        report = decoder.generate_report('HT13', 'md')
        
        assert '# Linear A Tablet HT13' in report
        assert 'Phonetic Reading' in report
        assert 'Confidence Metrics' in report
        assert 'Interpretation' in report


class TestVisualization:
    """Test visualization generation."""
    
    def test_emotional_plot_creation(self, decoder):
        """Test emotional plot creation."""
        reading = decoder.read_tablet('HT13')
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            filepath = f.name
        
        try:
            decoder.emotional_plot(reading.vocal_emotional_profile, filepath)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_harmonic_plot_creation(self, decoder):
        """Test harmonic plot creation."""
        frequencies = [220.0, 293.66, 440.0]
        harmonics = decoder._harmonic_analysis(frequencies)
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            filepath = f.name
        
        try:
            decoder.harmonic_plot(harmonics, filepath)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)


class TestDataIntegrity:
    """Test data file integrity and consistency."""
    
    def test_sign_database_loaded(self, decoder):
        """Test that sign database is loaded."""
        assert len(decoder.verified_signs) > 0
        assert 'AB08' in decoder.verified_signs
        assert 'AB120' in decoder.verified_signs
    
    def test_tablet_corpus_loaded(self, decoder):
        """Test that tablet corpus is loaded."""
        assert len(decoder.tablet_corpus) > 0
        assert 'HT13' in decoder.tablet_corpus
        assert 'HT85' in decoder.tablet_corpus
    
    def test_formulas_loaded(self, decoder):
        """Test that formulas are loaded."""
        assert len(decoder.formulas) > 0
        
        formula_names = [f['name'] for f in decoder.formulas]
        assert 'libation_formula' in formula_names
        assert 'total_formula' in formula_names
    
    def test_sign_frequency_validity(self, decoder):
        """Test that all sign frequencies are valid."""
        for sign_id, sign in decoder.verified_signs.items():
            assert sign.frequency > 0
            assert sign.frequency <= 2000  # Reasonable upper bound


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
