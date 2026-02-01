import pytest # (Optional, but we will stick to plain Python for simplicity today)
from day9_refactoring import ask_brain, train_brain

print("--- 🧪 DAY 10: INTEGRATION TEST SUITE ---")

# TEST 1: Does the Brain exist?
# If we try to ask the brain before training, does it crash or give a nice error?
print("\n[TEST 1] Asking Brain (Potentially before training)...")
response = ask_brain(50)
if "ERROR" in response:
    print(f"⚠️  System Check: {response}")
    print("   -> Attempting to Train now...")
    train_brain()
    response = ask_brain(50)
    print(f"   -> Retry Result: {response}")
else:
    print(f"✅ Brain is ready. Prediction: {response}")

# TEST 2: The Logic Check (Sanity Test)
# We know: <10 is Inactive, >85 is Banned.
print("\n[TEST 2] Verifying Logic Rules...")

test_cases = [
    (5, "Inactive"),   # Should be Inactive
    (50, "Active"),    # Should be Active
    (95, "Banned")     # Should be Banned
]

for logins, expected in test_cases:
    prediction = ask_brain(logins)
    if prediction == expected:
        print(f"✅ PASS: {logins} logins -> {prediction}")
    else:
        print(f"❌ FAIL: {logins} logins -> Got {prediction}, Expected {expected}")

# TEST 3: The Crash Test (Edge Cases)
# What happens if we send weird data? (Negative numbers, huge numbers)
print("\n[TEST 3] Edge Cases...")
weird_inputs = [-5, 0, 10000]

for i in weird_inputs:
    try:
        pred = ask_brain(i)
        print(f"⚠️ Input {i} -> Prediction: {pred}")
    except Exception as e:
        print(f"🔥 CRASH on input {i}: {e}")

print("\n--- 🏁 DAY 10 COMPLETE: READY FOR API ---")