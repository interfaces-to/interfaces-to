# translate the input into spanish
cat input.txt | into --system="translate to spanish" | jq -r '.content' > output.txt

# then share it in general
cat output.txt | into --tools=Slack --system="post to general in slack"