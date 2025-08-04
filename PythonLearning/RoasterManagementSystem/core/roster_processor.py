import pandas as pd
import numpy as np
import json
import re
from datetime import datetime
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Bidirectional
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.cluster import KMeans

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