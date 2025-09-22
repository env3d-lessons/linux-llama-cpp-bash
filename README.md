# Linux curl with LLM Exercise

Pre-reading: Learn about how to pass arguments to a bash script https://linuxhandbook.com/courses/bash-beginner/bash-arguments/

# Introduction

NOTE: Make sure you wait until all the setup is complete before starting the exercise.

The `query.sh` script is a simple Bash script that currently contains a single
`curl` command. This command is used to send a query to a local AI service that 
functions similarly to ChatGPT. By inspecting the script, you will notice that 
the prompt being sent to the AI service is hardcoded within the script itself. 
When you run the script, the `curl` command returns multiple lines of JSON 
objects, where each line represents a token with its value stored in the 
"content" key. By combining all the values of the "content" key from these JSON 
objects, you can reconstruct the complete response to the input prompt.

```shell
$ ./query.sh 
data: {"choices":[{"finish_reason":null,"index":0,"delta":{"role":"assistant","content":null}}],"created":1757973060,"id":"chatcmpl-Q9FZ3pGOdFQLtbXzymVYAVh2UvV0yBU5","model":"qwen2.5-0.5b-instruct","system_fingerprint":"b6479-b907255f","object":"chat.completion.chunk"}

data: {"choices":[{"finish_reason":null,"index":0,"delta":{"content":"Data"}}],"created":1757973060,"id":"chatcmpl-Q9FZ3pGOdFQLtbXzymVYAVh2UvV0yBU5","model":"qwen2.5-0.5b-instruct","system_fingerprint":"b6479-b907255f","object":"chat.completion.chunk"}

data: {"choices":[{"finish_reason":null,"index":0,"delta":{"content":" formats"}}],"created":1757973060,"id":"chatcmpl-Q9FZ3pGOdFQLtbXzymVYAVh2UvV0yBU5","model":"qwen2.5-0.5b-instruct","system_fingerprint":"b6479-b907255f","object":"chat.completion.chunk"}

...

```

# Exercise

You're goal is to modify query.sh to achieve the following:

  1. Instead of having the prompt integrated into the script itself, change it so the script
  accepts the prompt as a command-line argument

  1. If no prompt is specified, return an error.  Do not perform curl without argument.

  1. Output only to content stdout, not the individual JSON objects.

## Examples

```shell
./query.sh 'Write a short poem about data formats'
Data formats are like the keys to the kingdom,
They hold the secrets of the code,
From JSON to XML, they guide us all,
To make our data, the best that can be.

They format our text, making it easy,
We can read it, understand it, and share,
Whether it's a long tale or a brief,
Or data that needs to be shared.

They format our images too,
When we want to use them in our stories,
Or to make a picture that captures the spirit,
They format it to its best, and we'll see.

They format our videos too,
They can show us a story's tale,
Or to tell a tale we'll be pleased,
And we'll see them to the end.

They format our data, so we can share,
And help us to understand,
Their keys are the keys to the data format,
They help us make it easy to read and share.
```

```shell
$ ./query.sh 
Error: must call with prompt as argument
Usage: ./query.sh <prompt>
```
# Hand-in

Make sure you run `pytest` to check your score.

Once you are satisified with your score, run the following commands to submit your assignment:

1. `git add -A`
2. `git commit -a -m 'submit'`
3. `git push`
