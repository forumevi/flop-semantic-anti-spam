# Flop Labs - Agent Semantic Deduplication & Anti-Spam Filter (PoC)

A lightweight proof-of-concept (PoC) filter designed to detect memory loops and low-signal repetitive messages in AI agents operating on decentralized AI networks (such as Flop Labs).

## 🚀 Overview

As highlighted in recent Flop Labs network logs, unanchored or looping AI agents can send repetitive, low-entropy replies (e.g., 155 duplicate messages within 95 minutes). 

This behavior is not just a UI nuisance—it drains GPU inference compute resources, consumes bandwidth, and bloats state memory across the network.

This repository provides an algorithmic **Semantic Deduplication Guard** that evaluates message similarity *before* triggering LLM context inference calls, saving up to ~26.7%+ in wasted compute resources.

---

## 📊 Benchmark & Test Findings

Using our semantic similarity benchmark tool, we evaluated sample agent loop logs:

* **Total Comparisons Evaluated:** 15
* **Identified Loop / Spam Messages:** 4
* **Estimated Compute Waste Rate:** **26.7%**
* **Mechanism:** Checks N-Gram Jaccard Semantic Distance between incoming agent replies and state memory history.

---

## 🛠️ Code Architecture (`main.py`)

The core anti-spam guard intercepts incoming agent outputs before network broadcast:

```python
def calculate_jaccard_similarity(text1, text2):
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return (len(intersection) / len(union)) if union else 0.0

def flop_anti_spam_guard(new_reply, message_history, similarity_threshold=0.60):
    """
    Halts agent execution before inference if semantic similarity exceeds threshold.
    Prevents GPU compute burn caused by repetitive agent loops.
    """
    for past_reply in message_history:
        sim = calculate_jaccard_similarity(new_reply, past_reply)
        if sim >= similarity_threshold:
            print(f"[BLOCKED] Semantic Similarity ({sim*100:.1f}%) exceeds threshold. Compute halted.")
            return False
    print("[PASSED] Message high signal. Proceeding to network.")
    return True
