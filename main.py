# Flop Labs - Agent Semantic Deduplication & Anti-Spam Filter (PoC)

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
