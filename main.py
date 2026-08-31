# Flop Labs - Agent Semantic Deduplication & Anti-Spam Filter (PoC)

import math

def calculate_similarity(text1, text2):
    """İki ajan yanıtı arasındaki kelime benzerliğini (Jaccard Index) ölçer."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if union else 0.0

def flop_anti_spam_guard(new_reply, previous_replies, similarity_threshold=0.75):
    """
    Ajan yanıtı ağa (Inference) gönderilmeden önce bellek kontrolü yapar.
    Benzerlik eşiği geçilirse yanıt engellenir ve GPU compute gücü korunur.
    """
    for prev in previous_replies:
        sim = calculate_similarity(new_reply, prev)
        if sim >= similarity_threshold:
            print(f"[BLOCKED] High Similarity Detected ({sim*100:.1f}%). Compute execution halted to prevent loop.")
            return False  # Mesajı engelle
    
    print("[PASSED] Signal is high. Proceeding to network output.")
    return True  # Mesaj onaylandı

# Test Senaryosu
history = ["Makes sense. Where do you see this heading?"]
incoming_bot_reply = "Makes sense. Where do you see this heading?"

flop_anti_spam_guard(incoming_bot_reply, history)
