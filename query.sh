curl -s http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"qwen2.5-0.5b-instruct\",
    \"messages\": [{\"role\": \"user\", \"content\": \"Write me a poem on data formats\"}],
    \"stream\": true,
    \"max_tokens\": 256
  }" 