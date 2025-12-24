import json
import random

# --- 1. THE KNOWLEDGE BASE (What the Bank knows) ---
# Repeat them to simulate volume/variations
documents = [
    "How to freeze your debit card in the app",
    "Reporting a lost or stolen credit card",
    "International wire transfer fees and limits",
    "SWIFT and IBAN codes for incoming transfers",
    "Setting up recurring bill payments",
    "Interest rates for Premium Savings accounts",
    "Overdraft protection and eligibility",
    "How to dispute a transaction on your statement",
    "Updating your billing address and phone number",
    "Biometric login setup (FaceID / TouchID)"
] * 5  # 50 Documents total

# --- 2. THE USER QUERIES (What users are asking) ---

# A. COVERED TOPICS (Should be Green)
covered_queries = [
    "I lost my card, how do I stop it?",
    "freeze my debit card immediately",
    "what is the fee for sending money to France?",
    "where do I find my SWIFT code?",
    "interest rate for savings account",
    "how to change my phone number",
    "app login with face id not working",
    "dispute a charge from amazon",
    "cancel a recurring payment",
    "enable overdraft protection"
] * 4 # 40 Covered Queries

# B. BLIND SPOT 1: CRYPTO (Should be Red)
# The bank has zero docs about Crypto, but users want it.
gap_crypto = [
    "can I buy bitcoin here?",
    "how to transfer ethereum to my wallet",
    "do you support dogecoin?",
    "crypto trading fees",
    "when are you adding cryptocurrency support?",
    "wallet address for receiving btc",
    "invest in crypto directly from app",
    "bitcoin exchange rates"
] * 3 # 24 Crypto Queries

# C. BLIND SPOT 2: DARK MODE (Should be Red)
# Users want a UI feature that doesn't exist.
gap_darkmode = [
    "how to enable dark mode?",
    "app is too bright at night",
    "where is the theme setting?",
    "switch to night mode please",
    "dark theme support android"
] * 4 # 20 Dark Mode Queries

# Combine them all
all_queries = covered_queries + gap_crypto + gap_darkmode
random.shuffle(all_queries) # Shuffle to make it realistic

# --- 3. OUTPUT JSON ---
payload = {
    "documents": documents,
    "queries": all_queries
}

print(json.dumps(payload, indent=2))