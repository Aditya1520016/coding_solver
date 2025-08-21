"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"

from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-4o-mini",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text)
