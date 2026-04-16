#!/usr/bin/env python3
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Utility script to generate Ed25519 keypairs for ResilientDB.

This is a standalone utility script for manual key generation.
For automated key generation, use the MCP server's generateKeys tool instead.
"""
import sys
from collections import namedtuple

try:
    from cryptoconditions import crypto as _cc_crypto
except ImportError:
    print("Error: Could not import cryptoconditions.")
    print("Install it with: pip install cryptoconditions")
    sys.exit(1)

CryptoKeypair = namedtuple("CryptoKeypair", ("private_key", "public_key"))


def generate_keypair() -> CryptoKeypair:
    """Generate an Ed25519 keypair (base58-encoded, ResilientDB format)."""
    priv, pub = (k.decode() for k in _cc_crypto.ed25519_generate_key_pair())
    return CryptoKeypair(private_key=priv, public_key=pub)


# Generate keypairs
signer = generate_keypair()
recipient = generate_keypair()

print("=" * 70)
print("ResilientDB Key Generator")
print("=" * 70)
print()
print("Signer Keypair:")
print(f"  Public Key:  {signer.public_key}")
print(f"  Private Key: {signer.private_key}")
print()
print("Recipient Keypair:")
print(f"  Public Key:  {recipient.public_key}")
print(f"  Private Key: {recipient.private_key}")
print()
print("=" * 70)
print("Ready-to-use curl command:")
print("=" * 70)
print()
print(f"""curl -X POST http://localhost:8000/graphql \\
  -H "Content-Type: application/json" \\
  -d '{{
    "query": "mutation Test($data: PrepareAsset!) {{ postTransaction(data: $data) {{ id }} }}",
    "variables": {{
      "data": {{
        "operation": "CREATE",
        "amount": 100,
        "signerPublicKey": "{signer.public_key}",
        "signerPrivateKey": "{signer.private_key}",
        "recipientPublicKey": "{recipient.public_key}",
        "asset": {{
          "data": {{
            "name": "Test Asset",
            "description": "My first test asset"
          }}
        }}
      }}
    }}
  }}' | python3 -m json.tool""")
print()
print("=" * 70)
print("Copy and paste the curl command above to create a transaction!")
print("=" * 70)
