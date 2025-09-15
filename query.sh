# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Error"
  echo "Usage: $0 <prompt>"
  exit 1
fi

curl -s http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-0.5b-instruct",
    "messages": [{"role": "user", "content": "Write a short poem about data formats"}],
    "stream": true,
    "max_tokens": 256
  }' | grep '{"content' | cut -f 12 -d '"' | tr -d '\n' | sed 's/\\n/\n/g' 