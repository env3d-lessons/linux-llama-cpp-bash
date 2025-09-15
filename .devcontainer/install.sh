#!/bin/bash

# smallest qwen model
wget https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q2_k.gguf

bin/llama-server -m qwen2.5-0.5b-instruct-q2_k.gguf

echo ""
echo "✅ DevContainer setup complete!"
echo "You can now start working on your assignment."