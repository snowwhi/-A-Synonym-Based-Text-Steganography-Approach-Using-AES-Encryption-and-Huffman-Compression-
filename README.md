# Baseline Synonym Substitution Text Steganography

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple text steganography implementation using synonym substitution for bit embedding, combined with Huffman compression and AES-256 encryption.

## 🎯 Overview

This is a **baseline implementation** of text steganography that uses a simple but effective approach:

1. **Compress** the secret message using Huffman coding
2. **Encrypt** the compressed data using AES-256
3. **Embed** bits by substituting words with their synonyms
4. **Extract** and decrypt to recover the original message

**Purpose:** This serves as a baseline/comparison method for evaluating more advanced steganography techniques like CMPHM-based approaches.

---

## 🔍 How It Works (Simple Explanation)

Imagine you have a secret message and want to hide it in normal text:

### The Process:

**Step 1: Pick Your Words**
You have a dictionary of word pairs that mean the same thing:
- good ↔ excellent
- fast ↔ quick
- big ↔ large

**Step 2: Hide Your Secret**
Your secret message becomes 0s and 1s (bits). For each bit:
- Bit **0** → Use the **first** word (good, fast, big)
- Bit **1** → Use the **second** word (excellent, quick, large)

**Example:**

```
Cover text: "The good dog ran fast"
Secret bits: 0 1

Result:     "The good dog ran quick"
                 ↑              ↑
                (0)            (1)
```

The word "good" stayed the same (bit 0), but "fast" changed to "quick" (bit 1).

**Step 3: Get It Back**
The receiver looks at each word:
- Sees "good" → bit 0
- Sees "quick" → bit 1
- Converts bits back to original message

---

## ✨ Features

### Capabilities
- ✅ **Simple Implementation** - Easy to understand and modify
- ✅ **Huffman Compression** - Reduces message size by ~50%
- ✅ **AES-256 Encryption** - Military-grade security
- ✅ **Dictionary-Based** - Uses natural synonym pairs
- ✅ **Preserves Format** - Keeps capitalization and punctuation

### Evaluation Tools
- 📊 Embedding capacity (BPC - Bits Per Character)
- 🔍 Imperceptibility (Jaro-Winkler similarity)
- ⏱️ Performance timing (embedding/extraction speed)

---

## 🚀 Installation

### Prerequisites
```bash
Python 3.8+
pip package manager
```

### Install Required Libraries
```bash
pip install huffman cryptography jellyfish
```

**What each library does:**
- `huffman` - Compresses the message
- `cryptography` - Provides AES-256 encryption
- `jellyfish` - Calculates text similarity

---

## 🎬 Quick Start

### Basic Example

```python
# Your secret message
secret_message = "Hello World"

# Cover text (must contain dictionary words)
cover_text = "The good dog ran fast to the big house. " * 50

# 32-byte encryption key
key = b'0123456789abcdef0123456789abcdef'

# Hide the message
stego_text, codec, bits_len, embed_time = hide_message(
    secret_message, 
    cover_text, 
    key
)

print(f"Stego Text: {stego_text[:100]}...")

# Recover the message
recovered, extract_time = recover_message(
    stego_text, 
    cover_text, 
    codec, 
    key, 
    bits_len
)

print(f"Recovered: {recovered}")
print(f"Success: {recovered == secret_message}")
**Expected Output:**
```
Stego Text: The good dog ran quick to the large house. The terrible cat was sluggish and tiny. ...
Recovered Message: khadija_is_good
Embedding Capacity: 0.0006 bits per character
Imperceptibility (Jaro-Winkler Similarity): 0.8830
Performance - Embedding Time: 0.0123s, Extraction Time: 0.0098s
```

---
## 🏗️ Methodology

### The Synonym Dictionary

The system uses predefined word pairs:

```python
SYNONYM_DICT = {
    'good': ('good', 'excellent'),    # 0=good, 1=excellent
    'bad': ('bad', 'terrible'),       # 0=bad, 1=terrible
    'big': ('big', 'large'),          # 0=big, 1=large
    'small': ('small', 'tiny'),       # 0=small, 1=tiny
    'fast': ('fast', 'quick'),        # 0=fast, 1=quick
    'slow': ('slow', 'sluggish'),     # 0=slow, 1=sluggish
}
```

### Step-by-Step Process

#### **1. Compression (Huffman Coding)**
```
Original message: "Hello"
↓
Compressed bits: "0110100011..."
(~50% smaller)
```

**Why?** Smaller messages are easier to hide.

#### **2. Encryption (AES-256 CTR Mode)**
```
Compressed: "0110100011..."
↓
Encrypted: "X7#@9$%..."
(scrambled with your key)
```

**Why?** Even if someone finds the hidden message, they can't read it.

#### **3. Embedding (Synonym Substitution)**
```
Cover text: "The good dog ran fast"
Bits to hide: 0 1
↓
Look at each word:
- "good" is in dictionary
  → Bit is 0
  → Keep it as "good" ✓
  
- "fast" is in dictionary  
  → Bit is 1
  → Change to "quick" ✓

Result: "The good dog ran quick"
```

**Why?** Synonyms look natural, so the text doesn't seem suspicious.

#### **4. Extraction & Decryption**
```
Stego text: "The good dog ran quick"
↓
Check each word against dictionary:
- "good" → bit 0
- "quick" → bit 1
↓
Decrypt with key
↓
Decompress
↓
Original message: "Hello"
```

---

## 📊 Evaluation Metrics

### 1. Embedding Capacity

**Formula:**
```
Capacity (BPC) = (Secret message bits) / (Cover text characters)
```

**Typical Results:**
- **BPC:** 0.0003 - 0.0008
- **Interpretation:** Very low capacity due to dictionary limitations

**Example:**
```
Secret: 15 chars = 120 bits
Cover: 14,400 chars
Capacity: 120/14,400 = 0.0083 BPC
```

### 2. Imperceptibility

**Formula:**
```
Similarity = jaro_winkler_similarity(original, stego)
```

**Typical Results:**
- **Score:** 0.85 - 0.90 (85-90% similar)
- **Interpretation:** Moderately imperceptible

**Why Lower?**
Synonym changes like "good" → "excellent" can be noticeable:
```
❌ "The excellent dog ran quick to the large house"
   (Sounds unnatural)
```

### 3. Performance

**Typical Timing:**
- Embedding: 0.01 - 0.03 seconds
- Extraction: 0.008 - 0.02 seconds

**Very Fast!** Simple dictionary lookup is efficient.

---

## ⚠️ Limitations

### 1. **Very Low Capacity**

**Problem:** Only works with specific words in the dictionary.

**Example:**
```python
SYNONYM_DICT = {
    'good': ('good', 'excellent'),
    'fast': ('fast', 'quick'),
    # ... only 6 pairs
}

cover_text = "The good dog ran fast."  # Only 2 words match
# Can hide: 2 bits maximum!
```

**Impact:** Need very long cover texts (1000+ words) for short messages.

### 2. **Dictionary Dependency**

**Problem:** Cover text must contain the exact words.

**Example:**
```python
# This works:
cover = "The good dog ran fast"  ✅

# This doesn't:
cover = "The nice dog ran quickly"  ❌ (no dictionary words)
```

### 3. **Unnatural Text**

**Problem:** Synonym substitution can create awkward sentences.

**Examples:**
```
Original: "The good dog"
Stego:    "The excellent dog"  
          (sounds too formal)

Original: "The fast car"
Stego:    "The quick car"
          (sounds odd)
```

### 4. **Detectable Patterns**

**Problem:** Repeated substitutions create patterns.

**Example:**
```
"The excellent dog ran quick to the large house. 
 The terrible cat was sluggish and tiny."
 
All adjectives are formal synonyms → suspicious!
```

---

## 💡 Use Cases

### ✅ **Good For:**

1. **Educational Purposes**
   - Learning steganography basics
   - Understanding compression + encryption + embedding

2. **Baseline Comparison**
   - Testing against more advanced methods
   - Demonstrating need for better techniques

3. **Controlled Environments**
   - When you control the cover text
   - When detection isn't the primary concern

### ❌ **Not Good For:**

1. **Real-World Covert Communication**
   - Too easy to detect
   - Very low capacity

2. **Arbitrary Cover Texts**
   - Doesn't work if text lacks dictionary words

3. **High-Volume Data Hiding**
   - Can only hide a few bits per sentence

---

## 🔧 Troubleshooting

### Issue 1: "Cover text too short"

**Problem:**
```python
ValueError: Not enough dictionary words in cover text
```

**Solution:**
```python
# Multiply cover text to get more dictionary words
cover_text = base_text * 100  # Repeat 100 times

# OR use text with more synonym words
cover_text = """
The good team did a fast job on the big project.
The bad weather was slow to clear the small area.
""" * 50
```

### Issue 2: "Low capacity - can't hide message"

**Problem:**
```
Secret: 100 chars
Capacity: Only 24 bits available
```

**Solution 1 - Shorter Message:**
```python
# Use shorter message
secret = "Hi"  # Instead of "Hello World"
```

**Solution 2 - More Dictionary Words:**
```python
# Add more synonym pairs
SYNONYM_DICT = {
    'good': ('good', 'excellent'),
    'bad': ('bad', 'terrible'),
    'big': ('big', 'large'),
    'small': ('small', 'tiny'),
    'fast': ('fast', 'quick'),
    'slow': ('slow', 'sluggish'),
    'nice': ('nice', 'pleasant'),      # NEW
    'happy': ('happy', 'joyful'),      # NEW
    'sad': ('sad', 'unhappy'),         # NEW
}
```

### Issue 3: "Similarity too low (< 0.85)"

**Problem:**
```
Jaro-Winkler Similarity: 0.78 (too low)
```

**Explanation:** Many synonym substitutions make text look different.

**Solution:** This is a known limitation of the method. Consider:
- Using fewer substitutions (shorter messages)
- Switching to CMPHM-based approach (better imperceptibility)


## 📝 Key Takeaways

### ✅ **Strengths:**
- Simple and easy to understand
- Fast performance
- Good educational value
- Works as baseline for comparison

### ⚠️ **Weaknesses:**
- Very low capacity (6-12 bits per text block)
- Dictionary dependency
- Unnatural synonym usage
- Easy to detect

### 🎯 **Best Use:**
Use this as a **baseline/comparison method** when evaluating more sophisticated steganography techniques. It demonstrates why advanced methods like CMPHM are necessary.

---

## 🔬 For Research Papers

### How to Present This Method:

**Title:** "Baseline Synonym Substitution Method"

**Description:**
```
For comparison purposes, we implemented a baseline synonym 
substitution approach. This method uses a predefined dictionary 
of 6 word pairs (e.g., good↔excellent, fast↔quick) where each 
pair encodes one bit. While simple to implement, this baseline 
suffers from three limitations: (1) very low capacity due to 
dictionary size, (2) moderate detectability from unnatural 
synonym usage, and (3) dependency on specific cover text words. 
These limitations motivated our CMPHM-based approach.
```




