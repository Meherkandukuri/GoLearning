import sys
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import tkinter.font as tkfont
import os
from datetime import datetime, time
from collections import defaultdict, deque
import colorsys
import re
import random
import math
import json
from pathlib import Path
import numpy as np
from difflib import SequenceMatcher
import statistics
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Bidirectional
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.cluster import KMeans
import psutil
import matplotlib.pyplot as plt
from tkinter import ttk
import time as tm

# Check for ttkbootstrap
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    try:
        error_root = tk.Tk()
        error_root.withdraw()
        messagebox.showerror(
            "Missing Dependency",
            "The 'ttkbootstrap' module is required but not installed.\n\n"
            "Please install it using the command:\n"
            "pip install ttkbootstrap"
        )
        error_root.destroy()
    except:
        print("Error: The 'ttkbootstrap' module is required but not installed.")
        print("Please install it using: pip install ttkbootstrap")
    sys.exit(1)

class DataDetectionBot:
    def __init__(self):
        self.column_identifiers = {
            'EMP ID': ['emp', 'id', 'employee', 'staff'],
            'Name': ['name', 'employee name', 'staff'],
            'date': ['date', 'day', 'd-', 'shift date'],
            'shift': ['shift', 'timing', 'schedule', 'pattern'],
            'department': ['dept', 'department', 'team'],
            'position': ['position', 'role', 'designation']
        }
        self.date_formats = [
            "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d", "%d-%b-%y", 
            "%d %B %Y", "%d-%m-%y", "%m-%d-%y", "%y-%m-%d"
        ]

    def detect_columns(self, df):
        detected = {}
        for col in df.columns:
            col_lower = str(col).lower()
            for field, identifiers in self.column_identifiers.items():
                if any(id in col_lower for id in identifiers):
                    detected[field] = col
                    break
        return detected

class ShiftPatternBot:
    def __init__(self):
        self.shift_keywords = {
            'M': ['morning', 'am', 'morn', '0600', '0700', '0800'],
            'A': ['afternoon', 'pm', 'aft', '1200', '1300', '1400'],
            'N': ['night', 'evening', '2000', '2100', '2200'],
            'OFF': ['off', 'rest', 'leave', 'holiday']
        }

    def extract_shift_patterns(self, df, date_columns):
        patterns = {}
        for _, row in df.iterrows():
            pattern = []
            for col in date_columns:
                cell_value = str(row[col]).upper()
                shift_type = '?'
                for key, keywords in self.shift_keywords.items():
                    if any(kw in cell_value for kw in keywords):
                        shift_type = key
                        break
                pattern.append(shift_type)
            patterns[row.name] = '-'.join(pattern)
        return patterns

class DataCleanupBot:
    def clean_data(self, df, column_map):
        # Standardize column names
        df = df.rename(columns={v:k for k,v in column_map.items() if v in df.columns})
        
        # Clean employee IDs
        if 'EMP ID' in df.columns:
            df['EMP ID'] = df['EMP ID'].astype(str).str.strip().str.upper()
            
        # Clean dates
        date_cols = [col for col in df.columns if any(char in str(col) for char in ["/", "-"])]
        for col in date_cols:
            df[col] = df[col].astype(str).str.strip()
            
        return df

class MixedDataImporter:
    def __init__(self):
        self.detection_bot = DataDetectionBot()
        self.pattern_bot = ShiftPatternBot()
        self.cleanup_bot = DataCleanupBot()

    def import_mixed_data(self, file_path):
        try:
            # Read file with multiple attempts
            df = self._read_file(file_path)
            
            # Detect and standardize columns
            detected = self.detection_bot.detect_columns(df)
            
            # Clean and transform data
            df = self.cleanup_bot.clean_data(df, detected)
            
            # Extract shift patterns
            date_cols = [col for col in df.columns if any(char in str(col) for char in ["/", "-"])]
            patterns = self.pattern_bot.extract_shift_patterns(df, date_cols)
            df['Detected Pattern'] = df.index.map(patterns)
            
            return df
            
        except Exception as e:
            raise ValueError(f"Import failed: {str(e)}")

    def _read_file(self, file_path):
        # Try multiple reading strategies
        try:
            return pd.read_excel(file_path, engine='openpyxl')
        except:
            try:
                return pd.read_csv(file_path)
            except:
                try:
                    return pd.read_excel(file_path, engine='xlrd')
                except Exception as e:
                    raise ValueError(f"Could not read file: {str(e)}")

class StarryBackground:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.stars = []
        self.create_stars()
        
    def create_stars(self):
        # Create stars with varying sizes and brightness
        for _ in range(150):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.uniform(0.5, 2)
            brightness = random.uniform(0.3, 1.0)
            twinkle_speed = random.uniform(0.005, 0.02)
            
            star = {
                'x': x, 'y': y, 'size': size, 
                'brightness': brightness, 'twinkle_speed': twinkle_speed,
                'current_brightness': brightness, 'increasing': False
            }
            
            # Create the star on canvas
            star_id = self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=self.get_star_color(brightness),
                outline=""
            )
            star['id'] = star_id
            self.stars.append(star)
    
    def get_star_color(self, brightness):
        # Create star color based on brightness
        r = g = b = int(255 * brightness)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def update(self):
        # Update stars (twinkle effect)
        for star in self.stars:
            # Update brightness
            if star['increasing']:
                star['current_brightness'] += star['twinkle_speed']
                if star['current_brightness'] >= star['brightness']:
                    star['current_brightness'] = star['brightness']
                    star['increasing'] = False
            else:
                star['current_brightness'] -= star['twinkle_speed']
                if star['current_brightness'] <= star['brightness'] * 0.5:
                    star['current_brightness'] = star['brightness'] * 0.5
                    star['increasing'] = True
            
            # Update star color
            color = self.get_star_color(star['current_brightness'])
            self.canvas.itemconfig(star['id'], fill=color)
        
        # Schedule next update
        self.canvas.after(50, self.update)

class RosterProcessor:
    def __init__(self):
        self.df_original = None
        self.df_processed = None
        self.OFF_KEYWORDS = ['WOFF', 'W/OFF', 'RD', 'OFF', 'REST', 'RDO', 'LEAVE']
        self.SHIFT_TYPES = {
            "M": ["0600-1400", "0700-1500", "0800-1600", "0900-1700"],
            "A": ["1200-2000", "1300-2100", "1400-2200", "1500-2300"],
            "N": ["1800-0200", "1900-0300", "2000-0400", "2100-0500", "2200-0600"]
        }
        self.PATTERN_CODES = [
            "CX-1E2N2E2RD", "CX-2E2N1E2RD", "PAX-GEN-2RD", "PAX-A-2RD", "EBT-3A2N2RD", "EY-1N4E2RD",
            "EY-31700N2RD", "EY-1E117001E1N1E2RD", "EY-217003E2RD", "EY-317002E2RD", "EY-2E217001E2RD",
            "UL/VN-2G2M1RD1G1RD", "PAX-3M2N2RD", "Regular Morning", "Regular Afternoon", "Regular Night",
            "PAX-EM", "PAX-M", "PAX-A", "PAX-E", "PAX-N", "SEC-MORN", "SEC-2MAN", "SEC-GEN", "SEC-GEN2", 
            "CRP-GEN", "APR-M", "APR-N", "APR-1600-0000", "APR-1A3E1N2RD", "APR-AFT", "APR-1M3E1RD", 
            "APR-2E1N2E2RD", "APR-2E1RD3E1RD", "APR-2M2A1E1N2RD", "APR-2M2A1N1E2RD", "APR-2M2A2E2RD",
            "APR-2M2A2N2RD", "APR-2M2E2N2RD", "APR-2M3E2RD", "APR-3G1M2G1RD", "APR-3M2E2RD", "APR-E", 
            "Pax-Gen", "PAX-1M4E2RD", "PAX-2M1A2N2RD", "PAX-2M2E1N2RD", "PAX-2M3N2RD", "PAX-2A3E2RD", 
            "EK-2M1A2E2RD", "PAX-2M3E2RD", "PAX-E-EY", "PAX-2E3N2RD", "ALL MORNINGS", "3 MORNING 3 AFTERNOON", 
            "pcc-gen", "EK-2M3E2RD", "2M2E1N2RD", "EK-3M1E1N2RD", "EK-3M1N1E2RD", "EK-3M2E2RD", "IX-EM", 
            "IX1300-2100", "IX1300-2200", "ALL NIGHTS", "2A3N2RD", "EY-1700-0230", "EBT-1m5a1rd", 
            "DD-2E1N1E1RD1E1RD", "UL-1G2M1G2M1RD", "UL-2M1G1M2G1RD", "UL-1G1M2G2M1RD", "XY-1EM1M2EM1M1EM1RD", 
            "1EM1M1EM1M2EM1RD", "SEC-3G2A1RD", "3A1E1N2RD", "3A2E2RD", "EY-1200-2000-", "MHB-1A1E1A2N2RD", 
            "MHB-1M1A1E2N2RD", "MHB-2M2A2M1RD", "MHB-3M3G1RD", "MHB-2G3E2RD", "MHB-3M1G2M1RD", "MHB-1A2M1E1N2RD",
            "MHB-1A4N2RD", "MHB-2A2E1N2RD", "EK-5M1A1RD", "EY-1E117001E2N2RD", "SQ-4M2E1RD", "SQ-5M1E1RD",
            "SV-2G2M1G1M1RD", "SV-1G4M1G1RD", "SV-5M1G1RD"
        ]
        self.pattern_mapping = {}  # Dictionary to store learned patterns
        self.pattern_confidence = defaultdict(int)  # Track pattern recognition confidence
        self.unknown_patterns = set()  # Track unrecognized patterns
        self.pattern_statistics = defaultdict(int)  # Track pattern usage statistics
        self.sequence_matcher = SequenceMatcher()
        self.pattern_model = self.build_pattern_model()
        self.load_patterns()  # Load patterns when initializing
        self.load_trained_model()  # Load AI model if available
        
        # Predefined patterns for sequence matching
        self.predefined_patterns = {
            "Regular Morning": ["M", "M", "M", "M", "M", "M", "RD"],
            "Regular Afternoon": ["A", "A", "A", "A", "A", "A", "RD"],
            "Regular Night": ["N", "N", "N", "N", "N", "N", "RD"],
            "5-2 Rotation": ["M", "M", "M", "M", "M", "RD", "RD"],
            "4-3 Rotation": ["M", "M", "M", "M", "RD", "RD", "RD"],
            "Mixed Rotation": ["M", "A", "N", "RD", "M", "A", "N"],
            "Nights Rotation": ["N", "N", "N", "N", "RD", "RD", "RD"]
        }
        
    def build_pattern_model(self):
        """Create a more robust LSTM neural network for pattern recognition"""
        model = Sequential([
            Embedding(input_dim=1000, output_dim=64, input_length=42),
            Bidirectional(LSTM(128, return_sequences=True)),
            Bidirectional(LSTM(64)),
            Dense(256, activation='relu'),
            Dense(128, activation='relu'),
            Dense(len(self.PATTERN_CODES), activation='softmax')
        ])
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
        
    def load_trained_model(self):
        """Load pre-trained model weights if available"""
        model_path = Path("pattern_model.weights.h5")
        if model_path.exists():
            try:
                self.pattern_model.load_weights(str(model_path))
                print("Loaded pre-trained pattern recognition model")
            except:
                print("Could not load model weights")
                
    def save_trained_model(self):
        """Save model weights for future use"""
        self.pattern_model.save_weights("pattern_model.weights.h5")
        
    def pattern_to_sequence(self, pattern_str):
        """Convert pattern string to numerical sequence"""
        mapping = {"M": 1, "A": 2, "N": 3, "RD": 4, "?": 5}
        sequence = []
        for char in pattern_str.split('-'):
            sequence.append(mapping.get(char, 5))  # Default to unknown
        return sequence
        
    def train_model(self, X_train, y_train):
        """Train the neural network model"""
        # Pad sequences to fixed length
        X_padded = pad_sequences(X_train, maxlen=42, padding='post')
        
        # Convert labels to indices
        label_to_index = {code: idx for idx, code in enumerate(self.PATTERN_CODES)}
        y_indices = [label_to_index[code] for code in y_train]
        
        # Skip training if no data
        if len(X_train) == 0:
            print("No training data available")
            return
        
        # Train the model - removed minimum sample requirement
        self.pattern_model.fit(
            X_padded, 
            np.array(y_indices),
            epochs=30,
            batch_size=min(32, len(X_train)),  # Dynamic batch size
            validation_split=min(0.2, 1 - 1/len(X_train)) if len(X_train) > 1 else 0
        )
        self.save_trained_model()
        
    def predict_pattern(self, pattern_str):
        """Use AI model to predict pattern code"""
        sequence = self.pattern_to_sequence(pattern_str)
        padded_seq = pad_sequences([sequence], maxlen=42, padding='post')
        predictions = self.pattern_model.predict(padded_seq, verbose=0)[0]
        top_idx = np.argmax(predictions)
        return self.PATTERN_CODES[top_idx], predictions[top_idx]
        
    def load_patterns(self):
        """Load learned patterns from JSON file"""
        pattern_file = Path("learned_patterns.json")
        if pattern_file.exists():
            try:
                with open(pattern_file, 'r') as f:
                    self.pattern_mapping = json.load(f)
            except Exception as e:
                print(f"Error loading patterns: {e}")
                self.pattern_mapping = {}
                
    def save_patterns(self):
        """Save learned patterns to JSON file"""
        pattern_file = Path("learned_patterns.json")
        try:
            with open(pattern_file, 'w') as f:
                json.dump(self.pattern_mapping, f)
        except Exception as e:
            print(f"Error saving patterns: {e}")
            
    def get_shift_type(self, shift_str):
        """Determine shift type based on actual timing"""
        shift_str = shift_str.upper().strip()
        
        # Check for OFF days first
        if any(off in shift_str for off in self.OFF_KEYWORDS):
            return "RD"
        
        # Check for exact timing patterns
        for shift_type, timings in self.SHIFT_TYPES.items():
            for timing in timings:
                if timing in shift_str:
                    return shift_type
        
        # Try to parse time ranges
        time_match = re.search(r'(\d{1,4})\s*[-:]\s*(\d{1,4})', shift_str)
        if time_match:
            try:
                start_str, end_str = time_match.groups()
                
                # Normalize times to 4-digit format
                start_time = start_str.zfill(4)
                end_time = end_str.zfill(4)
                
                # Convert to minutes since midnight
                start_minutes = int(start_time[:2]) * 60 + int(start_time[2:4])
                end_minutes = int(end_time[:2]) * 60 + int(end_time[2:4])
                
                # Handle overnight shifts
                if end_minutes < start_minutes:
                    end_minutes += 24 * 60  # Add 24 hours
                
                # Determine shift type based on start time
                if 300 <= start_minutes < 720:  # 5:00 AM to 12:00 PM
                    return "M"
                elif 720 <= start_minutes < 1020:  # 12:00 PM to 5:00 PM
                    return "A"
                elif start_minutes >= 1020 or start_minutes < 300:  # 5:00 PM to 5:00 AM
                    return "N"
            except:
                pass
        
        return "?"  # Unknown shift type
        
    def get_shift_pattern(self, row):
        """Convert a row's shifts into a pattern string with features"""
        shift_columns = [col for col in row.index if any(char in str(col) for char in ["/", "-"])]
        pattern = []
        shift_counts = defaultdict(int)
        shift_sequence = []
        
        for col in shift_columns:
            shift = str(row[col]).strip()
            if not shift:  # Skip empty shifts
                continue
                
            shift_type = self.get_shift_type(shift)
            pattern.append(shift_type)
            shift_sequence.append(shift_type)
            shift_counts[shift_type] += 1
                
        return "-".join(pattern), shift_counts, shift_sequence
        
    def learn_pattern(self, pattern_str, pattern_code):
        """Store and reinforce learned pattern"""
        if pattern_str in self.pattern_mapping:
            # Reinforce existing pattern
            self.pattern_confidence[pattern_code] += 5
        else:
            # New pattern learning
            self.pattern_mapping[pattern_str] = pattern_code
            self.pattern_confidence[pattern_code] = 10
            
        # Save after each learning
        self.save_patterns()
        
    def record_pattern_usage(self, pattern_code):
        """Track pattern usage statistics"""
        self.pattern_statistics[pattern_code] += 1
        
    def get_unknown_patterns(self):
        """Get unrecognized patterns"""
        return list(self.unknown_patterns)
        
    def _edit_distance(self, s1, s2):
        """Calculate edit distance between two strings (Levenshtein distance)"""
        if len(s1) < len(s2):
            return self._edit_distance(s2, s1)
        
        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
        
    def semantic_similarity(self, pattern1, pattern2):
        """Calculate semantic similarity between patterns"""
        # Sequence alignment similarity
        self.sequence_matcher.set_seqs(pattern1, pattern2)
        alignment_score = self.sequence_matcher.ratio()
        
        # Edit distance
        edit_distance = self._edit_distance(pattern1, pattern2)
        max_len = max(len(pattern1), len(pattern2))
        normalized_edit = 1 - (edit_distance / max_len) if max_len > 0 else 0
        
        # Contextual similarity
        context_sim = self.contextual_similarity(pattern1, pattern2)
        
        # Weighted combination
        return 0.5 * alignment_score + 0.3 * normalized_edit + 0.2 * context_sim
        
    def contextual_similarity(self, pattern1, pattern2):
        """Compare patterns based on contextual features"""
        features1 = self.get_pattern_features(pattern1)
        features2 = self.get_pattern_features(pattern2)
        
        if not features1 or not features2:
            return 0
            
        # Calculate feature similarity
        feature_sim = 0
        for key in features1:
            if key in features2:
                if isinstance(features1[key], (int, float)):
                    # Normalize numerical differences
                    max_val = max(features1[key], features2[key]) or 1
                    diff = abs(features1[key] - features2[key])
                    feature_sim += 1 - (diff / max_val)
                else:
                    # For categorical features
                    feature_sim += 1 if features1[key] == features2[key] else 0
                    
        return feature_sim / len(features1) if features1 else 0
        
    def get_pattern_features(self, pattern_str):
        """Extract features from pattern string"""
        parts = pattern_str.split('-')
        return {
            'length': len(parts),
            'rd_count': parts.count("RD"),
            'm_count': parts.count("M"),
            'a_count': parts.count("A"),
            'n_count': parts.count("N"),
            'first': parts[0] if parts else "",
            'last': parts[-1] if parts else "",
            'transitions': self.count_transitions(parts)
        }
        
    def count_transitions(self, pattern):
        """Count shift type transitions in pattern"""
        transitions = 0
        for i in range(1, len(pattern)):
            if pattern[i] != pattern[i-1]:
                transitions += 1
        return transitions
        
    def has_weekend_rd(self, row):
        """Detect if RD falls on weekend"""
        date_cols = [col for col in row.index if any(char in str(col) for char in ["/", "-"])]
        weekend_rd = False
        
        for i, col in enumerate(date_cols):
            if "RD" in str(row[col]).upper():
                try:
                    # Extract day of week from column header
                    if isinstance(col, str):
                        dt = datetime.strptime(col, "%d-%m-%Y")
                        if dt.weekday() >= 5:  # Saturday or Sunday
                            weekend_rd = True
                except:
                    continue
        return weekend_rd
        
    def cluster_patterns(self, patterns):
        """Cluster patterns using K-Means"""
        # Convert patterns to feature vectors
        features = []
        for pattern in patterns:
            feat = self.get_pattern_features(pattern)
            features.append([
                feat['length'],
                feat['rd_count'],
                feat['m_count'],
                feat['a_count'],
                feat['n_count'],
                feat['transitions']
            ])
            
        if not features:
            return {}
            
        # Perform clustering
        n_clusters = min(5, len(patterns))
        if n_clusters < 2:
            return {}
            
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(features)
        
        # Group patterns by cluster
        clustered = defaultdict(list)
        for i, pattern in enumerate(patterns):
            clustered[clusters[i]].append(pattern)
            
        return clustered
        
    def detect_repeating_pattern(self, sequence):
        """Detect repeating patterns in a sequence"""
        max_pattern_length = min(14, len(sequence))  # Look for patterns up to 14 days
        best_pattern = None
        best_score = 0
        
        # Try different pattern lengths
        for pattern_length in range(3, max_pattern_length + 1):
            # Check if sequence is multiple of pattern length
            if len(sequence) % pattern_length != 0:
                continue
                
            pattern = sequence[:pattern_length]
            repetitions = len(sequence) // pattern_length
            match = True
            
            # Verify pattern repeats throughout
            for i in range(1, repetitions):
                start = i * pattern_length
                end = start + pattern_length
                if sequence[start:end] != pattern:
                    match = False
                    break
                    
            if match:
                # Calculate confidence based on pattern length and repetitions
                score = pattern_length * repetitions
                if score > best_score:
                    best_score = score
                    best_pattern = pattern
                    
        return best_pattern
        
    def match_predefined_patterns(self, sequence):
        """Match sequence against predefined common patterns"""
        # First try exact matches
        for pattern_name, pattern_seq in self.predefined_patterns.items():
            if self.sequence_matches(sequence, pattern_seq):
                return pattern_name, 1.0
                
        # Then try partial matches
        best_match = None
        best_score = 0
        
        for pattern_name, pattern_seq in self.predefined_patterns.items():
            score = self.sequence_similarity(sequence, pattern_seq)
            if score > best_score and score > 0.7:
                best_score = score
                best_match = pattern_name
                
        if best_match:
            return best_match, best_score
            
        return None, 0.0
        
    def sequence_matches(self, seq1, seq2):
        """Check if two sequences match exactly with possible repetition"""
        if len(seq1) % len(seq2) != 0:
            return False
            
        repetitions = len(seq1) // len(seq2)
        for i in range(repetitions):
            start = i * len(seq2)
            end = start + len(seq2)
            if seq1[start:end] != seq2:
                return False
                
        return True
        
    def sequence_similarity(self, seq1, seq2):
        """Calculate similarity between two sequences"""
        # Find the longer sequence
        longer = seq1 if len(seq1) > len(seq2) else seq2
        shorter = seq1 if len(seq1) <= len(seq2) else seq2
        
        # Create a moving window over the longer sequence
        max_similarity = 0
        for i in range(0, len(longer) - len(shorter) + 1):
            window = longer[i:i+len(shorter)]
            matches = sum(1 if a == b else 0 for a, b in zip(window, shorter))
            similarity = matches / len(shorter)
            if similarity > max_similarity:
                max_similarity = similarity
                
        return max_similarity

    def detect_best_match(self, pattern_str, sequence):
        """AI-enhanced pattern matching with sequence analysis"""
        # 1. Check learned patterns first (exact match)
        if pattern_str in self.pattern_mapping:
            code = self.pattern_mapping[pattern_str]
            return code, 1.0  # 100% confidence
            
        # 2. Match against predefined patterns
        predefined_match, confidence = self.match_predefined_patterns(sequence)
        if predefined_match and confidence > 0.9:
            return predefined_match, confidence
            
        # 3. Try neural network prediction
        try:
            nn_pred, nn_confidence = self.predict_pattern(pattern_str)
            if nn_confidence > 0.8:
                return nn_pred, nn_confidence
        except Exception as e:
            print(f"AI prediction failed: {e}")
            
        # 4. Semantic similarity matching with your pattern codes
        best_match = None
        best_score = 0
        best_similarity = 0.0
        
        for code in self.PATTERN_CODES:
            similarity = self.semantic_similarity(pattern_str, code)
                
            # Weight by confidence and length match
            score = similarity * 100 + self.pattern_confidence.get(code, 0)
            if len(pattern_str) == len(code):
                score += 20  # Bonus for exact length match
                
            if score > best_score:
                best_score = score
                best_match = code
                best_similarity = similarity
        
        if best_match and best_similarity > 0.7:
            return best_match, best_similarity
            
        # 5. Check for repeating patterns (last resort)
        repeating_pattern = self.detect_repeating_pattern(sequence)
        if repeating_pattern:
            pattern_name = "Rep-" + "-".join(repeating_pattern)
            return pattern_name, 1.0
            
        return None, 0.0

    def format_date_headers(self, df):
        new_columns = []
        date_formats = [
            "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d", "%d-%b-%y", "%d %B %Y",
            "%d-%m-%y", "%m-%d-%y", "%y-%m-%d", "%d/%m/%y", "%m/%d/%y"
        ]
        
        for col in df.columns:
            if isinstance(col, str):
                col = col.strip()
                converted = False
                for fmt in date_formats:
                    try:
                        dt = datetime.strptime(col, fmt)
                        new_columns.append(dt.strftime("%d-%m-%Y"))
                        converted = True
                        break
                    except ValueError:
                        continue
                if not converted:
                    if isinstance(col, datetime):
                        new_columns.append(col.strftime("%d-%m-%Y"))
                    else:
                        new_columns.append(col)
            elif isinstance(col, datetime):
                new_columns.append(col.strftime("%d-%m-%Y"))
            else:
                new_columns.append(col)
        df.columns = new_columns
        return df

    def detect_roster_begin(self, row, date_cols):
        for i, val in enumerate(row[date_cols]):
            if pd.isna(val):
                continue
                
            val_str = str(val).upper().strip()
            if any(off in val_str for off in self.OFF_KEYWORDS):
                for j in range(i + 1, len(date_cols)):
                    next_shift = str(row[date_cols[j]]).upper().strip()
                    if not any(off in next_shift for off in self.OFF_KEYWORDS):
                        return date_cols[j]
                return date_cols[0]
        return date_cols[0]

    def generate_roster_begin(self):
        if self.df_original is None:
            raise ValueError("No file loaded")

        date_cols = [col for col in self.df_original.columns if any(char in str(col) for char in ["/", "-"])]
        if not date_cols:
            date_cols = self.df_original.columns[2:9]
            
        self.df_processed = self.df_original.copy()
        self.df_processed = self.format_date_headers(self.df_processed)
        date_cols = [col for col in self.df_processed.columns if any(char in str(col) for char in ["/", "-"])]
        
        self.df_processed['Roster Begin Date'] = self.df_processed.apply(
            lambda row: self.detect_roster_begin(row, date_cols), axis=1)
        self.df_processed['Pattern Code'] = ""
        
        new_order = [col for col in self.df_processed.columns 
                     if col not in ['Roster Begin Date', 'Pattern Code']] + \
                   ['Roster Begin Date', 'Pattern Code']
        self.df_processed = self.df_processed[new_order]
        return self.df_processed

    def validate_data(self):
        """Validate roster data and return issues"""
        issues = []
        if self.df_processed is not None:
            missing_ids = self.df_processed['EMP ID'].isna().sum()
            if missing_ids > 0:
                issues.append(f"Missing Employee IDs: {missing_ids}")
            
            empty_patterns = self.df_processed['Pattern Code'].isna().sum()
            if empty_patterns > 0:
                issues.append(f"Empty Pattern Codes: {empty_patterns}")
                
        return issues

class NSKRosterApp:
    def __init__(self, root):
        self.root = root
        self.current_theme = "darkly"
        self.available_themes = ["darkly", "superhero", "vapor", "cyborg", "solar", "morph", "quartz", "pulse", "flatly", "litera", "matrix"]
        self.style = ttk.Style(theme=self.current_theme)
        
        self.update_theme_colors()
        
        # Create canvas for background animation
        self.canvas = tk.Canvas(root, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Create main container above the canvas
        self.main_container = ttk.Frame(self.canvas, style='Black.TFrame')
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.processor = RosterProcessor()
        self.importer = MixedDataImporter()
        self.selected_rows = set()
        self.checkbox_vars = {}
        
        self.setup_ui()
        self.setup_pattern_learning_ui()
        self.setup_ai_tools()
        self.setup_autocomplete()
        self.shift_colors = {}
        self.configured_tags = set()
        self.column_widths = {}
        
        # Create starry background animation
        self.starry_bg = StarryBackground(self.canvas, root.winfo_width(), root.winfo_height())
        self.root.update()
        self.starry_bg.update()
        
        # Bind to window resize
        self.root.bind("<Configure>", self.on_resize)
        
        # Configure black frame style
        self.style.configure('Black.TFrame', background='black')
        
        # Handle window closing
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """Save patterns and close the application"""
        self.processor.save_patterns()
        self.processor.save_trained_model()
        if messagebox.askokcancel("Quit", "Do you want to quit NSK's Roster Analyzer?"):
            self.root.destroy()
            
    def on_resize(self, event):
        if event.widget == self.root:
            self.starry_bg.width = event.width
            self.starry_bg.height = event.height
            
    def update_theme_colors(self):
        self.bg_color = self.style.colors.dark
        self.fg_color = self.style.colors.light
        self.select_color = self.style.colors.primary
        
    def change_theme(self, theme_name):
        try:
            self.current_theme = theme_name
            self.style.theme_use(theme_name)
            self.update_theme_colors()
            self.update_treeview_style()
            self.status_var.set(f"Theme changed to: {theme_name}")
            
            # Special styling for Matrix theme
            if theme_name == "matrix":
                self.style.configure("Treeview", 
                                    background='black', 
                                    foreground='#00ff00',
                                    fieldbackground='black',
                                    rowheight=28)
                self.style.configure("Treeview.Heading", 
                                    background='#003300',
                                    foreground='#00ff00',
                                    font=("Courier", 10, "bold"))
                self.style.map("Treeview", 
                              background=[("selected", "#005500")])
                self.clock_label.configure(foreground="#00ff00")
            else:
                self.update_treeview_style()
                self.clock_label.configure(foreground="white")
                
        except Exception as e:
            messagebox.showerror("Theme Error", f"Failed to change theme: {str(e)}")
        
    def update_treeview_style(self):
        self.style.configure("Treeview", 
                             background='black', 
                             foreground='white',
                             fieldbackground='black',
                             rowheight=28)
        self.style.configure("Treeview.Heading", 
                             background='#004466',
                             foreground='white',
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview", 
                      background=[("selected", "#006699")])
        
    def update_clock(self):
        """Update the digital clock"""
        current_time = tm.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
        
    def setup_ui(self):
        self.root.title("NSK's Roster Analyzer Pro")
        self.root.geometry("1400x800")
        
        header_frame = ttk.Frame(self.main_container, padding=15, style='Black.TFrame')
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_canvas = tk.Canvas(
            header_frame, 
            bg='#001a33', 
            highlightthickness=0,
            height=60,
            width=500
        )
        title_canvas.pack(side="left", fill="x", expand=True)
        
        title_canvas.create_rectangle(
            0, 0, 500, 60, 
            fill='#001a33', 
            outline='', 
            tags="bg"
        )
        
        title_canvas.create_text(
            15, 25,
            text="NSK'S ROSTER ANALYZER",
            font=("Segoe UI", 18, "bold"),
            fill="#00ccff",
            anchor="w",
            tags="title"
        )
        
        subtitle = ttk.Label(
            header_frame,
            text="Professional Shift Management Suite with AI",
            font=("Segoe UI", 10, "italic"),
            bootstyle="secondary"
        )
        subtitle.pack(side="left", padx=10, anchor="s")
        
        theme_frame = ttk.Frame(header_frame, style='Black.TFrame')
        theme_frame.pack(side="right", padx=(20, 0))
        
        ttk.Label(theme_frame, text="Theme:", font=("Segoe UI", 10), bootstyle="inverse").pack(side="left", padx=(0, 5))
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=self.available_themes,
            state="readonly",
            width=12,
            bootstyle="primary"
        )
        theme_combo.pack(side="left")
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.change_theme(self.theme_var.get()))
        
        # Create digital clock label
        self.clock_label = ttk.Label(
            header_frame, 
            font=("Courier", 14),
            background='black',
            foreground='white'
        )
        self.clock_label.pack(side="right", padx=10)
        
        btn_frame = ttk.Frame(self.main_container, style='Black.TFrame')
        btn_frame.pack(fill="x", pady=(0, 15))
        
        primary_frame = ttk.Frame(btn_frame, style='Black.TFrame')
        primary_frame.pack(side="left", fill="x", expand=True)
        
        primary_actions = [
            ("📂 Import File", self.browse_file, "primary", "Import roster data from Excel/CSV"),
            ("⚙️ Generate Roster", self.generate_roster, "success", "Generate roster begin dates"),
            ("💾 Export Data", self.export_to_excel, "warning", "Export processed data to Excel"),
            ("🔍 Validate Data", self.validate_data, "info", "Check data integrity")
        ]
        
        for text, command, style, tooltip in primary_actions:
            btn = ttk.Button(
                primary_frame, 
                text=text, 
                command=command, 
                bootstyle=style,
                width=20
            )
            btn.pack(side="left", padx=5)
            self.create_tooltip(btn, tooltip)
        
        secondary_frame = ttk.Frame(btn_frame, style='Black.TFrame')
        secondary_frame.pack(side="right")
        
        # ADDED AUTO DETECT BUTTON HERE
        secondary_actions = [
            ("🔍 Auto Detect", self.auto_detect_all, "info", "Automatically detect shift patterns"),
            ("➕ Add Pattern", self.add_pattern_code, "secondary", "Add new pattern code"),
            ("🧠 Pattern Manager", self.show_pattern_manager, "info", "Manage learned patterns"),
            ("✓ Select All", self.select_all_rows, "secondary", "Select all rows"),
            ("✗ Clear All", self.deselect_all_rows, "secondary", "Deselect all rows")
        ]
        
        for text, command, style, tooltip in secondary_actions:
            btn = ttk.Button(
                secondary_frame, 
                text=text, 
                command=command, 
                bootstyle=style,
                width=15
            )
            btn.pack(side="left", padx=2)
            self.create_tooltip(btn, tooltip)
        
        search_frame = ttk.Frame(self.main_container, style='Black.TFrame')
        search_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:", font=("Segoe UI", 10), bootstyle="inverse").pack(side="left", padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30,
            bootstyle="primary"
        )
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.bind("<KeyRelease>", self.search_data)
        
        ttk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            bootstyle="secondary",
            width=8
        ).pack(side="left")
        
        table_frame = ttk.LabelFrame(
            self.main_container, 
            text="📋 Roster Data", 
            bootstyle="primary",
            padding=15
        )
        table_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.tree = ttk.Treeview(
            table_frame,
            show="headings",
            bootstyle="primary",
            selectmode="extended",
            columns=()
        )
        
        vsb = ttk.Scrollbar(
            table_frame, 
            orient="vertical", 
            command=self.tree.yview,
            bootstyle="primary-round"
        )
        hsb = ttk.Scrollbar(
            table_frame, 
            orient="horizontal", 
            command=self.tree.xview,
            bootstyle="primary-round"
        )
        
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        self.update_treeview_style()
        
        status_frame = ttk.Frame(self.main_container, style='Black.TFrame')
        status_frame.pack(fill="x", pady=(5, 0))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - NSK's Roster Analyzer Pro")
        
        status_label = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            bootstyle="inverse",
            anchor="w",
            font=("Segoe UI", 9)
        )
        status_label.pack(side="left", fill="x", expand=True, padx=10)
        
        self.progress = ttk.Progressbar(
            status_frame,
            mode="indeterminate",
            bootstyle="primary-striped"
        )
        
        self.record_count_var = tk.StringVar()
        self.record_count_var.set("Records: 0")
        
        record_label = ttk.Label(
            status_frame,
            textvariable=self.record_count_var,
            bootstyle="inverse",
            font=("Segoe UI", 9)
        )
        record_label.pack(side="right", padx=10)
        
        ttk.Separator(status_frame, orient="vertical").pack(side="left", fill="y", padx=5)
        
        self.learning_icon = ttk.Label(
            status_frame,
            text="🧠",
            font=("Segoe UI", 10),
            bootstyle="inverse"
        )
        self.learning_icon.pack(side="left", padx=(5, 0))
        
        self.learning_status = ttk.Label(
            status_frame, 
            text="0 patterns learned",
            bootstyle="inverse",
            font=("Segoe UI", 9)
        )
        self.learning_status.pack(side="left", padx=(0, 10))
        
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Control-d>", self.copy_from_above)
        self.tree.bind("<Button-1>", self.on_treeview_click)
        self.tree.bind("<Return>", self.on_enter_key)
        self.tree.bind("<ButtonRelease-1>", self.on_column_resize)
        self.tree.bind("<<TreeviewSelect>>", self.highlight_selected_row)
        
        self.last_clicked_column = None
        self.last_clicked_row = None
        self.pattern_manager_open = False
        self.copied_pattern = None
        
        # Start the clock
        self.update_clock()
        
    def auto_detect_all(self):
        """Enhanced auto-detection with sequence analysis"""
        if self.processor.df_processed is None:
            messagebox.showwarning("No Data", "Please generate roster data first")
            return
            
        self.progress.pack(side="right", padx=10)
        self.progress.start()
        self.status_var.set("Auto-detecting patterns...")
        
        try:
            # Process each row
            for idx, row in self.processor.df_processed.iterrows():
                pattern_str, _, sequence = self.processor.get_shift_pattern(row)
                
                # Enhanced pattern detection
                best_match, confidence = self.processor.detect_best_match(pattern_str, sequence)
                
                if best_match and confidence > 0.5:
                    self.processor.df_processed.at[idx, 'Pattern Code'] = best_match
                    self.processor.record_pattern_usage(best_match)
                    
                    # Learn with confidence based on similarity
                    if confidence > 0.8:
                        self.processor.learn_pattern(pattern_str, best_match)
                else:
                    # Track unknown patterns
                    self.processor.unknown_patterns.add(pattern_str)
            
            # Update learning status
            learned = len(self.processor.pattern_mapping)
            unknown = len(self.processor.unknown_patterns)
            self.learning_status.config(
                text=f"Learned: {learned} patterns | Unknown: {unknown} patterns"
            )
            self.learning_status_var.set(f"Learned: {learned} patterns | Unknown: {unknown} patterns")
            
            self.update_table(self.processor.df_processed)
            self.status_var.set(f"Auto-detected patterns. {learned} patterns learned")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to auto-detect patterns: {str(e)}")
            self.status_var.set("Auto-detect failed")
        finally:
            self.progress.stop()
            self.progress.pack_forget()
        
    def select_all_rows(self):
        """Select all rows in the table"""
        for item in self.tree.get_children():
            self.tree.set(item, "Select", "☑")
            self.selected_rows.add(item)
        
    def deselect_all_rows(self):
        """Deselect all rows in the table"""
        for item in self.tree.get_children():
            self.tree.set(item, "Select", "☐")
            self.selected_rows.discard(item)
        
    def update_table(self, df):
        if df is None:
            return
            
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Remove any existing serial number column to prevent duplication
        if '#' in df.columns:
            df = df.drop(columns=['#'])
            
        # Add fresh serial numbers
        df = df.copy()
        df.insert(0, "#", range(1, len(df)+1))
        
        # Add checkbox column
        df.insert(0, "Select", "☐")
        
        # Configure treeview columns
        self.tree["columns"] = list(df.columns)
        
        # Configure checkbox column
        self.tree.column("Select", width=50, anchor="center")
        self.tree.heading("Select", text="✓")
        
        # Configure other columns
        for col in df.columns[1:]:  # Skip checkbox column
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=100, anchor='center')
        
        # Add data with checkboxes
        for idx, (_, row) in enumerate(df.iterrows()):
            values = [row[col] for col in df.columns]
            self.tree.insert("", "end", values=values, tags=(f"row{idx}",))
            self.tree.tag_configure(f"row{idx}", background='black' if idx % 2 else '#111111')

    def on_column_resize(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "separator":
            for i, col in enumerate(self.tree["columns"]):
                width = self.tree.column(col, width=True)
                self.column_widths[col] = width
                
    def highlight_selected_row(self, event):
        for item in self.tree.selection():
            self.tree.item(item, tags=("selected_row",))
            
    def setup_pattern_learning_ui(self):
        """Create pattern learning panel"""
        self.learning_frame = ttk.LabelFrame(
            self.main_container, 
            text="🔍 Pattern Learning", 
            bootstyle="info",
            padding=10
        )
        self.learning_frame.pack(fill="x", pady=5, padx=10)
        
        ttk.Label(
            self.learning_frame, 
            text="Learning Engine:",
            font=("Segoe UI", 9, "bold"),
            bootstyle="inverse"
        ).pack(side="left", padx=(0, 5))
        
        self.learning_status_var = tk.StringVar()
        self.learning_status_var.set("Ready to learn")
        
        learning_label = ttk.Label(
            self.learning_frame, 
            textvariable=self.learning_status_var,
            font=("Segoe UI", 9),
            bootstyle="info"
        )
        learning_label.pack(side="left", fill="x", expand=True)
        
        btn_frame = ttk.Frame(self.learning_frame)
        btn_frame.pack(side="right")
        
        ttk.Button(
            btn_frame, 
            text="Validate Patterns", 
            command=self.validate_patterns,
            bootstyle="info-outline",
            width=15
        ).pack(side="left", padx=2)
        
    def setup_ai_tools(self):
        """Add AI-powered tools to the UI"""
        ai_frame = ttk.LabelFrame(
            self.main_container, 
            text="🤖 AI Pattern Tools", 
            bootstyle="success",
            padding=10
        )
        ai_frame.pack(fill="x", pady=5, padx=10)
        
        ttk.Button(
            ai_frame, 
            text="Train Model",
            command=self.train_ai_model,
            bootstyle="success-outline",
            width=15
        ).pack(side="left", padx=5)
        
        ttk.Button(
            ai_frame, 
            text="Cluster Unknowns",
            command=self.cluster_unknown_patterns,
            bootstyle="info-outline",
            width=15
        ).pack(side="left", padx=5)
        
        ttk.Button(
            ai_frame, 
            text="Generate Insights",
            command=self.generate_insights,
            bootstyle="warning-outline",
            width=15
        ).pack(side="left", padx=5)
        
        self.ai_status = ttk.Label(
            ai_frame, 
            text="AI: Ready",
            font=("Segoe UI", 9),
            bootstyle="info"
        )
        self.ai_status.pack(side="left", padx=10, fill="x", expand=True)
        
    def train_ai_model(self):
        """Train the neural network model"""
        if self.processor.df_processed is None:
            messagebox.showwarning("No Data", "Please generate roster data first")
            return
            
        self.progress.pack(side="right", padx=10)
        self.progress.start()
        self.ai_status.config(text="AI: Training model...")
        
        try:
            X_train = []
            y_train = []
            
            for _, row in self.processor.df_processed.iterrows():
                pattern_str, _, _ = self.processor.get_shift_pattern(row)
                pattern_code = row.get("Pattern Code", "")
                
                if pattern_code and pattern_code in self.processor.PATTERN_CODES:
                    X_train.append(self.processor.pattern_to_sequence(pattern_str))
                    y_train.append(pattern_code)
            
            if len(X_train) > 0:
                self.processor.train_model(X_train, y_train)
                self.ai_status.config(text="AI: Model trained successfully")
                messagebox.showinfo("Training Complete", 
                                   f"Model trained with {len(X_train)} samples")
            else:
                messagebox.showwarning("Insufficient Data", 
                                      "Labeled patterns are required for training")
                self.ai_status.config(text="AI: Training failed - insufficient data")
            
        except Exception as e:
            messagebox.showerror("Training Error", f"Failed to train model: {str(e)}")
            self.ai_status.config(text=f"AI: Error - {str(e)}")
        finally:
            self.progress.stop()
            self.progress.pack_forget()
    
    def cluster_unknown_patterns(self):
        """Cluster unknown patterns for analysis"""
        if not self.processor.unknown_patterns:
            messagebox.showinfo("No Unknowns", "No unknown patterns to cluster")
            return
            
        self.progress.pack(side="right", padx=10)
        self.progress.start()
        self.ai_status.config(text="AI: Clustering patterns...")
        
        try:
            clusters = self.processor.cluster_patterns(list(self.processor.unknown_patterns))
            
            if clusters:
                cluster_text = "Pattern Clusters:\n\n"
                for cluster_id, patterns in clusters.items():
                    cluster_text += f"Cluster {cluster_id+1}:\n"
                    cluster_text += "\n".join(f" - {pattern}" for pattern in patterns[:5])
                    if len(patterns) > 5:
                        cluster_text += f"\n - ...and {len(patterns)-5} more"
                    cluster_text += "\n\n"
                
                cluster_window = tk.Toplevel(self.root)
                cluster_window.title("Pattern Clusters")
                cluster_window.geometry("600x400")
                
                text_frame = ttk.Frame(cluster_window)
                text_frame.pack(fill="both", expand=True, padx=10, pady=10)
                
                text_area = tk.Text(
                    text_frame,
                    wrap="word",
                    bg="black",
                    fg="white",
                    font=("Consolas", 10)
                )
                text_area.pack(fill="both", expand=True, padx=5, pady=5)
                text_area.insert("1.0", cluster_text)
                text_area.config(state="disabled")
                
                self.ai_status.config(text=f"AI: Found {len(clusters)} clusters")
            else:
                messagebox.showinfo("Clustering Result", "No significant clusters found")
                self.ai_status.config(text="AI: No clusters found")
                
        except Exception as e:
            messagebox.showerror("Clustering Error", f"Failed to cluster patterns: {str(e)}")
            self.ai_status.config(text=f"AI: Error - {str(e)}")
        finally:
            self.progress.stop()
            self.progress.pack_forget()
    
    def generate_insights(self):
        """Generate insights about shift patterns"""
        if self.processor.df_processed is None or "Pattern Code" not in self.processor.df_processed.columns:
            messagebox.showwarning("No Data", "Please generate roster data with pattern codes first")
            return
            
        self.progress.pack(side="right", padx=10)
        self.progress.start()
        self.ai_status.config(text="AI: Analyzing patterns...")
        
        try:
            pattern_counts = self.processor.df_processed["Pattern Code"].value_counts()
            
            top_patterns = pattern_counts.head(5)
            
            shift_dist = {"M": 0, "A": 0, "N": 0, "RD": 0}
            for _, row in self.processor.df_processed.iterrows():
                pattern_str, shift_counts, _ = self.processor.get_shift_pattern(row)
                for shift, count in shift_counts.items():
                    if shift in shift_dist:
                        shift_dist[shift] += count
            
            insights = "Shift Pattern Insights:\n\n"
            insights += f"Total Employees: {len(self.processor.df_processed)}\n"
            insights += f"Unique Patterns: {len(pattern_counts)}\n\n"
            
            insights += "Top 5 Patterns:\n"
            for pattern, count in top_patterns.items():
                insights += f" - {pattern}: {count} employees\n"
            
            insights += "\nShift Type Distribution:\n"
            total_shifts = sum(shift_dist.values())
            for shift, count in shift_dist.items():
                percentage = (count / total_shifts) * 100 if total_shifts else 0
                insights += f" - {shift}: {count} shifts ({percentage:.1f}%)\n"
            
            insights_window = tk.Toplevel(self.root)
            insights_window.title("Pattern Insights")
            insights_window.geometry("500x400")
            
            text_frame = ttk.Frame(insights_window)
            text_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            text_area = tk.Text(
                text_frame,
                wrap="word",
                bg="black",
                fg="white",
                font=("Segoe UI", 10)
            )
            text_area.pack(fill="both", expand=True, padx=5, pady=5)
            text_area.insert("1.0", insights)
            text_area.config(state="disabled")
            
            self.ai_status.config(text="AI: Insights generated")
            
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to generate insights: {str(e)}")
            self.ai_status.config(text=f"AI: Error - {str(e)}")
        finally:
            self.progress.stop()
            self.progress.pack_forget()
    
    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(
                tooltip,
                text=text,
                background='black',
                foreground='white',
                relief="solid",
                borderwidth=1,
                font=("Segoe UI", 9)
            )
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
                
            tooltip.after(3000, hide_tooltip)
            widget.tooltip = tooltip
            
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
        
    def setup_autocomplete(self):
        self.autocomplete_window = None
        self.autocomplete_listbox = None
        self.current_edit = None
        self.selected_index = 0
        
    def search_data(self, event=None):
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.update_table(self.processor.df_processed if self.processor.df_processed is not None else self.processor.df_original)
            return
            
        if self.processor.df_processed is not None:
            df = self.processor.df_processed
        elif self.processor.df_original is not None:
            df = self.processor.df_original
        else:
            return
            
        filtered_df = df[df.astype(str).apply(lambda x: x.str.lower().str.contains(search_term, na=False)).any(axis=1)]
        self.update_table(filtered_df)
        
    def clear_search(self):
        self.search_var.set("")
        self.update_table(self.processor.df_processed if self.processor.df_processed is not None else self.processor.df_original)
        
    def show_context_menu(self, event):
        context_menu = tk.Menu(self.root, tearoff=0, bg='black', fg='white')
        context_menu.add_command(label="Copy Cell", command=self.copy_cell)
        context_menu.add_command(label="Copy Row", command=self.copy_row)
        context_menu.add_command(label="Copy Pattern Code", command=self.copy_pattern_code)
        context_menu.add_command(label="Paste Pattern Code", command=self.paste_pattern_code)
        context_menu.add_separator()
        context_menu.add_command(label="Edit Cell", command=lambda: self.on_double_click(event))
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
            
    def copy_cell(self):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)['values']
            if values:
                self.root.clipboard_clear()
                self.root.clipboard_append(str(values[0]))
                self.status_var.set("Cell copied to clipboard")
                
    def copy_row(self):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)['values']
            row_text = '\t'.join(str(val) for val in values)
            self.root.clipboard_clear()
            self.root.clipboard_append(row_text)
            self.status_var.set("Row copied to clipboard")
            
    def copy_pattern_code(self):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            pattern_col = len(self.tree["columns"]) - 1  # Last column is pattern code
            pattern_code = self.tree.item(item)['values'][pattern_col]
            self.copied_pattern = pattern_code
            self.status_var.set(f"Copied pattern code: {pattern_code}")
            
    def paste_pattern_code(self):
        if not self.copied_pattern:
            self.status_var.set("No pattern code copied")
            return
            
        selected_items = self.tree.selection()
        if not selected_items:
            self.status_var.set("No rows selected")
            return
            
        pattern_col = len(self.tree["columns"]) - 1  # Last column is pattern code
        
        for item in selected_items:
            # Update treeview
            values = list(self.tree.item(item)['values'])
            values[pattern_col] = self.copied_pattern
            self.tree.item(item, values=values)
            
            # Update dataframe
            if self.processor.df_processed is not None:
                index = int(self.tree.index(item))
                col_name = self.tree["columns"][pattern_col]
                self.processor.df_processed.at[index, col_name] = self.copied_pattern
                
        self.status_var.set(f"Pasted pattern code to {len(selected_items)} rows")
        self.update_table(self.processor.df_processed)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Roster File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.progress.pack(side="right", padx=10)
            self.progress.start()
            
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, dtype={'EMP ID': str})
                else:
                    df = pd.read_excel(file_path, dtype={'EMP ID': str})
                
                df = self.processor.format_date_headers(df)
                self.processor.df_original = df
                self.update_table(df)
                self.status_var.set(f"Loaded: {os.path.basename(file_path)} - {len(df)} records")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
                self.status_var.set("Error loading file")
            finally:
                self.progress.stop()
                self.progress.pack_forget()
    
    def generate_roster(self):
        if self.processor.df_original is None:
            messagebox.showwarning("No Data", "Please load a file first")
            return
            
        self.progress.pack(side="right", padx=10)
        self.progress.start()
        
        try:
            df = self.processor.generate_roster_begin()
            self.update_table(df)
            self.status_var.set("Roster dates generated with Pattern Code column")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error generating roster")
        finally:
            self.progress.stop()
            self.progress.pack_forget()
    
    def validate_data(self):
        if self.processor.df_processed is None:
            messagebox.showwarning("No Data", "Please generate roster data first")
            return
            
        issues = self.processor.validate_data()
        
        if issues:
            issue_text = "\n".join(issues)
            messagebox.showwarning("Data Validation", f"Issues found:\n\n{issue_text}")
        else:
            messagebox.showinfo("Data Validation", "✅ All data looks good!")
            
        self.status_var.set(f"Validation complete - {len(issues)} issues found")
    
    def validate_patterns(self):
        """Validate all pattern codes in the dataset"""
        if self.processor.df_processed is None:
            messagebox.showwarning("No Data", "Please generate roster data first")
            return
            
        invalid_codes = []
        valid_count = 0
        
        for idx, row in self.processor.df_processed.iterrows():
            pattern_code = str(row.get("Pattern Code", "")).strip()
            if pattern_code and pattern_code not in self.processor.PATTERN_CODES:
                invalid_codes.append((row.get("EMP ID", ""), pattern_code))
            elif pattern_code:
                valid_count += 1
                
        if invalid_codes:
            invalid_count = len(invalid_codes)
            message = f"Found {invalid_count} invalid pattern codes\n"
            message += f"Valid patterns: {valid_count}\n\n"
            message += "Open Pattern Manager to review?"
            if messagebox.askyesno("Validation Results", message):
                self.show_pattern_manager()
        else:
            messagebox.showinfo("Validation Complete", "All pattern codes are valid!")
        
        self.status_var.set(f"Pattern validation: {valid_count} valid, {len(invalid_codes)} invalid")
    
    def highlight_shifts(self, df):
        if df is None:
            return
            
        for idx, item in enumerate(self.tree.get_children()):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.item(item, tags=(tag,))
        
        shift_columns = [col for col in df.columns if any(char in str(col) for char in ["/", "-"])]
        
        # Process each row
        for idx, (_, row) in enumerate(df.iterrows()):
            if idx >= len(self.tree.get_children()):
                continue
                
            item = self.tree.get_children()[idx]
            current_tags = list(self.tree.item(item, "tags"))
            
            # Process each shift column
            for col in shift_columns:
                if col not in df.columns:
                    continue
                    
                shift = str(row[col]).strip()
                if not shift:
                    continue
                    
                # Create a tag for this specific shift
                shift_type = self.processor.get_shift_type(shift)
                tag_name = f"shift_{shift_type}"
                color = self.generate_color(shift_type, col)
                
                # Configure the tag if not already done
                if tag_name not in self.configured_tags:
                    self.tree.tag_configure(tag_name, background=color)
                    self.configured_tags.add(tag_name)
                
                # Add the tag to the current tags
                if tag_name not in current_tags:
                    current_tags.append(tag_name)
            
            # Update item tags
            self.tree.item(item, tags=current_tags)
    
    def generate_color(self, shift_type, column_name):
        key = f"{column_name}_{shift_type}"
        
        if key in self.shift_colors:
            return self.shift_colors[key]
            
        # Special colors for common shift types
        color_map = {
            "M": "#FF9900",  # Orange for mornings
            "A": "#00CC66",  # Green for afternoons
            "N": "#3366FF",  # Blue for nights
            "RD": "#CC66CC"  # Purple for rest days
        }
        
        # Use predefined color if available
        if shift_type in color_map:
            self.shift_colors[key] = color_map[shift_type]
            return color_map[shift_type]
                
        # Generate random color for other shifts
        hue = (len(self.shift_colors) * 0.618) % 1.0
        saturation = 0.7
        value = 0.85 if self.current_theme in ["darkly", "cyborg", "solar"] else 0.7
        
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        
        color = f"#{r:02x}{g:02x}{b:02x}"
        self.shift_colors[key] = color
        return color
        
    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            # Allow editing of any column except the first (checkbox)
            if column != "#1":
                self.edit_cell(item, column)
                
                # Add pattern to learning if new
                if self.processor.df_processed is not None:
                    index = int(self.tree.index(item))
                    col_name = self.tree["columns"][int(column[1:])-1]
                    if col_name == "Pattern Code":
                        pattern_code = self.tree.set(item, column)
                        if pattern_code and pattern_code not in self.processor.PATTERN_CODES:
                            self.ask_to_learn_pattern(index, pattern_code)
    
    def ask_to_learn_pattern(self, index, pattern_code):
        """Prompt user to save a new pattern"""
        row = self.processor.df_processed.iloc[index]
        pattern_str, _, _ = self.processor.get_shift_pattern(row)
        
        response = messagebox.askyesno(
            "New Pattern Detected",
            f"Learn new pattern?\n\nPattern: {pattern_str}\nCode: {pattern_code}",
            parent=self.root
        )
        
        if response:
            self.processor.PATTERN_CODES.append(pattern_code)
            self.processor.learn_pattern(pattern_str, pattern_code)
            self.status_var.set(f"Learned new pattern: {pattern_code}")
            
            # Update learning status
            learned = len(self.processor.pattern_mapping)
            self.learning_status_var.set(f"Learned: {learned} patterns")
            self.learning_status.config(text=f"Learned: {learned} patterns")

    def on_treeview_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            self.last_clicked_column = self.tree.identify_column(event.x)
            self.last_clicked_row = self.tree.identify_row(event.y)
            
            # Handle checkbox toggle
            if self.last_clicked_column == "#1":  # First column is checkbox
                current_val = self.tree.set(self.last_clicked_row, "Select")
                if current_val == "☐":
                    self.tree.set(self.last_clicked_row, "Select", "☑")
                    self.selected_rows.add(self.last_clicked_row)
                else:
                    self.tree.set(self.last_clicked_row, "Select", "☐")
                    self.selected_rows.discard(self.last_clicked_row)
                    
    def on_enter_key(self, event):
        if self.last_clicked_row and self.last_clicked_column:
            if self.last_clicked_column != "#1":  # Skip checkbox column
                next_item = self.tree.next(self.last_clicked_row)
                if next_item:
                    self.tree.selection_set(next_item)
                    self.tree.focus(next_item)
                    self.tree.see(next_item)
                    self.last_clicked_row = next_item
                    self.edit_cell(next_item, self.last_clicked_column)
                    
    def copy_from_above(self, event):
        if self.last_clicked_row and self.last_clicked_column:
            prev_item = self.tree.prev(self.last_clicked_row)
            if prev_item:
                value_above = self.tree.set(prev_item, self.last_clicked_column)
                
                selected_items = self.tree.selection()
                for item in selected_items:
                    self.tree.set(item, self.last_clicked_column, value_above)
                    
                    if self.processor.df_processed is not None:
                        index = int(self.tree.index(item))
                        col_name = self.tree["columns"][int(self.last_clicked_column[1:])-1]
                        self.processor.df_processed.at[index, col_name] = value_above
                        
                self.status_var.set("Copied from above")
                self.update_table(self.processor.df_processed)
                
    def edit_cell(self, item, column):
        x, y, width, height = self.tree.bbox(item, column)
        current_value = self.tree.set(item, column)
        
        entry = ttk.Entry(
            self.tree, 
            font=("Segoe UI", 10),
            bootstyle="primary"
        )
        entry.place(x=x, y=y, width=width, height=height, anchor="nw")
        entry.insert(0, current_value)
        entry.select_range(0, tk.END)
        entry.focus()
        
        entry.bind("<Return>", lambda e: self.save_cell(item, column, entry))
        entry.bind("<Tab>", lambda e: self.save_cell(item, column, entry))
        entry.bind("<Escape>", lambda e: self.cancel_edit(entry))
        entry.bind("<KeyRelease>", lambda e: self.update_autocomplete(entry))
        entry.bind("<Up>", lambda e: self.handle_entry_up(e))
        entry.bind("<Down>", lambda e: self.handle_entry_down(e))
        
        self.current_edit = (item, column, entry)
        self.selected_index = 0
        
        # Auto-detect only for pattern code column
        col_index = int(column[1:]) - 1
        if self.tree["columns"][col_index] == "Pattern Code":
            self.auto_detect_pattern(item, column, entry)
    
    def auto_detect_pattern(self, item, column, entry):
        if self.processor.df_processed is None:
            return
            
        index = int(self.tree.index(item))
        row = self.processor.df_processed.iloc[index]
        
        # Get the shift pattern string and sequence
        pattern_str, _, sequence = self.processor.get_shift_pattern(row)
        
        # Enhanced pattern detection
        best_match, confidence = self.processor.detect_best_match(pattern_str, sequence)
        
        if best_match and confidence > 0.5:
            entry.delete(0, tk.END)
            entry.insert(0, best_match)
            self.status_var.set(f"Auto-detected pattern: {best_match} (confidence: {confidence*100:.1f}%)")
    
    def handle_entry_up(self, event):
        if self.autocomplete_listbox and self.autocomplete_listbox.winfo_exists():
            if self.selected_index > 0:
                self.selected_index -= 1
                self.autocomplete_listbox.selection_clear(0, tk.END)
                self.autocomplete_listbox.selection_set(self.selected_index)
                self.autocomplete_listbox.see(self.selected_index)
        return "break"
    
    def handle_entry_down(self, event):
        if self.autocomplete_listbox and self.autocomplete_listbox.winfo_exists():
            max_index = self.autocomplete_listbox.size() - 1
            if self.selected_index < max_index:
                self.selected_index += 1
                self.autocomplete_listbox.selection_clear(0, tk.END)
                self.autocomplete_listbox.selection_set(self.selected_index)
                self.autocomplete_listbox.see(self.selected_index)
        return "break"
    
    def cancel_edit(self, entry):
        self.hide_autocomplete()
        if entry.winfo_exists():
            entry.destroy()
        self.current_edit = None
    
    def update_autocomplete(self, entry):
        self.root.after(100, self._delayed_autocomplete, entry)
    
    def _delayed_autocomplete(self, entry):
        if not entry.winfo_exists():
            return
            
        text = entry.get().upper()
        if not text:
            self.hide_autocomplete()
            return
            
        col_index = int(self.current_edit[1][1:]) - 1
        col_name = self.tree["columns"][col_index]
        
        # Only show autocomplete for pattern code column
        if col_name == "Pattern Code":
            primary_matches = [code for code in self.processor.PATTERN_CODES if code.upper().startswith(text)]
            secondary_matches = [code for code in self.processor.PATTERN_CODES 
                               if text in code.upper() and not code.upper().startswith(text)]
            
            matches = primary_matches + secondary_matches
            
            if matches:
                if self.autocomplete_window and self.autocomplete_window.winfo_exists():
                    self.autocomplete_listbox.delete(0, tk.END)
                    for match in matches[:8]:
                        self.autocomplete_listbox.insert(tk.END, match)
                    self.selected_index = 0
                    self.autocomplete_listbox.selection_set(0)
                    self.autocomplete_listbox.see(0)
                else:
                    self.show_autocomplete(entry, matches)
            else:
                self.hide_autocomplete()
        else:
            self.hide_autocomplete()
    
    def show_autocomplete(self, entry, matches):
        if not entry.winfo_exists():
            return
            
        if self.autocomplete_window:
            self.autocomplete_window.destroy()
            
        x = entry.winfo_rootx()
        y = entry.winfo_rooty() + entry.winfo_height()
        
        self.autocomplete_window = tk.Toplevel(self.root)
        self.autocomplete_window.wm_overrideredirect(True)
        self.autocomplete_window.wm_geometry(f"+{x}+{y}")
        self.autocomplete_window.configure(bg='black')
        
        max_items = 8
        matches = matches[:max_items]
        
        self.autocomplete_listbox = tk.Listbox(
            self.autocomplete_window,
            height=min(len(matches), max_items),
            width=max(len(match) for match in matches) + 2,
            selectbackground='#006699',
            selectforeground='white',
            bg='black',
            fg='white',
            font=("Segoe UI", 10),
            bd=1,
            highlightthickness=0,
            relief="solid",
            activestyle="none",
            exportselection=False
        )
        self.autocomplete_listbox.pack()
        
        for match in matches:
            self.autocomplete_listbox.insert(tk.END, match)
        
        self.selected_index = 0
        self.autocomplete_listbox.selection_set(0)
        self.autocomplete_listbox.see(0)
        
        self.autocomplete_listbox.bind("<Button-1>", self.on_autocomplete_click)
        self.autocomplete_listbox.bind("<Double-Button-1>", self.on_autocomplete_double_click)
        self.autocomplete_listbox.bind("<Return>", self.select_autocomplete)
        
        entry.focus()
    
    def on_autocomplete_click(self, event):
        self.selected_index = self.autocomplete_listbox.nearest(event.y)
        self.autocomplete_listbox.selection_clear(0, tk.END)
        self.autocomplete_listbox.selection_set(self.selected_index)
        
        if self.current_edit:
            _, _, entry = self.current_edit
            if entry.winfo_exists():
                entry.focus()
    
    def on_autocomplete_double_click(self, event):
        self.select_autocomplete()
    
    def hide_autocomplete(self):
        if self.autocomplete_window:
            self.autocomplete_window.destroy()
            self.autocomplete_window = None
            self.autocomplete_listbox = None
    
    def select_autocomplete(self, event=None):
        if self.autocomplete_listbox and self.current_edit:
            # Get the current selection from the listbox
            selection = self.autocomplete_listbox.curselection()
            if selection:
                selected_index = selection[0]
                selection_text = self.autocomplete_listbox.get(selected_index)
                item, column, entry = self.current_edit
                
                if not entry.winfo_exists():
                    self.hide_autocomplete()
                    return
                
                entry.delete(0, tk.END)
                entry.insert(0, selection_text)
                self.tree.set(item, column, selection_text)
                
                if self.processor.df_processed is not None:
                    index = int(self.tree.index(item))
                    col_name = self.tree["columns"][int(column[1:])-1]
                    self.processor.df_processed.at[index, col_name] = selection_text
                    
                    # LEARN PATTERN: Map shift pattern to this code
                    if col_name == "Pattern Code":
                        row = self.processor.df_processed.iloc[index]
                        pattern_str, _, _ = self.processor.get_shift_pattern(row)
                        self.processor.learn_pattern(pattern_str, selection_text)
                        self.processor.record_pattern_usage(selection_text)
                
                self.hide_autocomplete()
                entry.destroy()
                self.current_edit = None
                
                next_item = self.tree.next(item)
                if next_item:
                    self.tree.see(next_item)
                    self.root.after(100, lambda: self.edit_cell(next_item, column))
                self.update_table(self.processor.df_processed)

    def save_cell(self, item, column, entry):
        if not entry.winfo_exists():
            return
        
        if self.autocomplete_listbox and self.autocomplete_listbox.winfo_exists():
            self.select_autocomplete()
            return
            
        new_value = entry.get()
        self.tree.set(item, column, new_value)
        
        if self.processor.df_processed is not None:
            index = int(self.tree.index(item))
            col_name = self.tree["columns"][int(column[1:])-1]
            self.processor.df_processed.at[index, col_name] = new_value
            
            # LEARN PATTERN if this is a pattern code column
            if col_name == "Pattern Code":
                row = self.processor.df_processed.iloc[index]
                pattern_str, _, _ = self.processor.get_shift_pattern(row)
                self.processor.learn_pattern(pattern_str, new_value)
                self.processor.record_pattern_usage(new_value)
        
        self.hide_autocomplete()
        entry.destroy()
        self.current_edit = None
        
        # Move to next cell in same row
        col_index = int(column[1:])
        if col_index < len(self.tree["columns"]):
            next_col = f"#{col_index + 1}"
            self.root.after(100, lambda: self.edit_cell(item, next_col))
        else:
            # Move to next row if at end of row
            next_item = self.tree.next(item)
            if next_item:
                self.tree.see(next_item)
                self.root.after(100, lambda: self.edit_cell(next_item, "#2"))
                
        self.update_table(self.processor.df_processed)
    
    def export_to_excel(self):
        if self.processor.df_processed is None:
            messagebox.showwarning("No Data", "Please generate roster data first")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Roster Data",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )
        
        if file_path:
            self.progress.pack(side="right", padx=10)
            self.progress.start()
            
            try:
                # Remove serial number column before exporting
                export_df = self.processor.df_processed.drop(columns=["#"], errors="ignore")
                export_df = self.processor.format_date_headers(export_df)
                
                if file_path.endswith('.csv'):
                    export_df.to_csv(file_path, index=False)
                else:
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        export_df.to_excel(writer, index=False, sheet_name="Roster Data")
                        effective_df = export_df[['EMP ID', 'Roster Begin Date', 'Pattern Code']].copy()
                        effective_df.to_excel(writer, index=False, sheet_name="Effective Dates")
                
                self.status_var.set(f"Exported to {os.path.basename(file_path)}")
                messagebox.showinfo("Export Success", f"File exported successfully to:\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export file:\n{str(e)}")
                self.status_var.set("Export failed")
            finally:
                self.progress.stop()
                self.progress.pack_forget()
    
    def add_pattern_code(self):
        new_code = simpledialog.askstring(
            "Add Pattern Code", 
            "Enter new pattern code:",
            parent=self.root
        )
        if new_code and new_code.strip():
            new_code = new_code.strip()
            if new_code not in self.processor.PATTERN_CODES:
                self.processor.PATTERN_CODES.append(new_code)
                self.processor.PATTERN_CODES.sort()
                self.status_var.set(f"Added new pattern code: {new_code}")
                messagebox.showinfo("Success", f"Added new pattern code: {new_code}")
            else:
                messagebox.showwarning("Duplicate", "Pattern code already exists!")
    
    def show_pattern_manager(self):
        if self.pattern_manager_open:
            return
            
        self.pattern_manager_open = True
        manager = tk.Toplevel(self.root)
        manager.title("Pattern Learning Manager")
        manager.geometry("800x600")
        manager.transient(self.root)
        manager.grab_set()
        
        # Header
        header = ttk.Frame(manager, padding=10)
        header.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(
            header,
            text="Pattern Learning Center",
            font=("Segoe UI", 14, "bold"),
            bootstyle="primary"
        ).pack(side="left")
        
        ttk.Button(
            header,
            text="Refresh",
            command=lambda: self.update_pattern_manager(manager),
            bootstyle="success",
            width=10
        ).pack(side="right", padx=5)
        
        # Stats frame
        stats_frame = ttk.Frame(manager, padding=10)
        stats_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        stats_data = [
            ("Learned Patterns", len(self.processor.pattern_mapping)),
            ("Unknown Patterns", len(self.processor.unknown_patterns)),
            ("Most Used Pattern", max(self.processor.pattern_statistics, 
                                   key=self.processor.pattern_statistics.get, 
                                   default="N/A"))
        ]
        
        for text, value in stats_data:
            frame = ttk.Frame(stats_frame)
            frame.pack(side="left", padx=10, fill="x", expand=True)
            
            ttk.Label(
                frame,
                text=text,
                font=("Segoe UI", 9),
                bootstyle="secondary"
            ).pack(anchor="w")
            
            ttk.Label(
                frame,
                text=str(value),
                font=("Segoe UI", 10, "bold"),
                bootstyle="primary"
            ).pack(anchor="w", pady=(2, 0))
        
        # Pattern lists
        notebook = ttk.Notebook(manager)
        notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Known patterns tab
        known_frame = ttk.Frame(notebook, padding=10)
        notebook.add(known_frame, text=f"Learned Patterns ({len(self.processor.pattern_mapping)})")
        
        known_columns = ("Pattern String", "Mapped Code", "Confidence")
        self.known_tree = ttk.Treeview(
            known_frame,
            columns=known_columns,
            show="headings",
            height=10,
            bootstyle="primary"
        )
        
        for col in known_columns:
            self.known_tree.heading(col, text=col)
            self.known_tree.column(col, width=150)
        
        vsb = ttk.Scrollbar(known_frame, orient="vertical", command=self.known_tree.yview)
        self.known_tree.configure(yscrollcommand=vsb.set)
        
        self.known_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
        # Unknown patterns tab
        unknown_frame = ttk.Frame(notebook, padding=10)
        notebook.add(unknown_frame, text=f"Unknown Patterns ({len(self.processor.unknown_patterns)})")
        
        self.unknown_list = tk.Listbox(
            unknown_frame,
            font=("Consolas", 10),
            bg="black",
            fg="white",
            selectbackground="#006699",
            selectforeground="white",
            height=15
        )
        self.unknown_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Fill data
        self.update_pattern_manager(manager)
        
        # Bind closing event
        manager.protocol("WM_DELETE_WINDOW", lambda: self.close_pattern_manager(manager))
    
    def update_pattern_manager(self, manager):
        # Update known patterns
        for item in self.known_tree.get_children():
            self.known_tree.delete(item)
            
        for pattern, code in self.processor.pattern_mapping.items():
            confidence = self.processor.pattern_confidence.get(code, 0)
            self.known_tree.insert("", "end", values=(pattern, code, confidence))
        
        # Update unknown patterns
        self.unknown_list.delete(0, tk.END)
        for pattern in self.processor.get_unknown_patterns():
            self.unknown_list.insert(tk.END, pattern)
    
    def close_pattern_manager(self, manager):
        self.pattern_manager_open = False
        manager.destroy()

if __name__ == "__main__":
    try:
        root = ttk.Window(title="NSK's Roster Analyzer Pro", themename="darkly")
        root.resizable(True, True)
        root.minsize(1000, 600)
        root.geometry("1400x800")
        root.configure(background='black')
        
        app = NSKRosterApp(root)
        root.mainloop()
        
    except Exception as e:
        import traceback
        error_msg = f"Application failed to start:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        
        try:
            error_root = tk.Tk()
            error_root.withdraw()
            messagebox.showerror("Startup Error", error_msg)
            error_root.destroy()
        except:
            print(error_msg)