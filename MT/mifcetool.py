#!/usr/bin/python

import asyncio
import os
import time
from firmware_content_extractor import extract_async

url = input("\nEnter the ROM URL(.zip): ")
filename = input("\nEnter the name of the filename to extract (e.g., boot.img): ")

storage_path = os.path.expanduser("~/storage")
if os.path.exists(storage_path):
    output_dir = os.path.join(storage_path, "fcetool_files")
    os.makedirs(output_dir, exist_ok=True)
else:
    output_dir = os.path.expanduser("~")

start_time = time.perf_counter()

result = asyncio.run(extract_async(url, filename, output_dir))

elapsed = time.perf_counter() - start_time

if result.get("success"):
    print(f"\n[OK] output: {filename} ({elapsed:.2f}s)\n")
else:
    print(f"\n[FAIL] {result.get('error')} ({elapsed:.2f}s)\n")
