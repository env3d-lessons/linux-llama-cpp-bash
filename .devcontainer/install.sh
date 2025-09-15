#!/bin/bash

echo "export LLAMA_CPP_LIB_PATH=/workspaces/$(basename $(pwd))/bin/" >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/workspaces/'"$(basename $(pwd))"'/bin/:$LD_LIBRARY_PATH' >> ~/.bashrc
export LLAMA_CPP_LIB=/workspaces/$(basename $(pwd))/bin/libllama.so

# smallest qwen model
wget https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q2_k.gguf

nohub bin/llama-server -m qwen2.5-0.5b-instruct-q2_k.gguf & 

echo ""
echo "✅ DevContainer setup complete!"
echo "You can now start working on your assignment."