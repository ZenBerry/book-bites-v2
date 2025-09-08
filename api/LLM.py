from google import genai

client = genai.Client(api_key="AIzaSyCO4CaWfuolgFco93vdGbYEjqOf9CcqXws")

response = client.models.generate_content(
    model="gemma-3-27b-it",
    contents="Please list 5 authors similar to Tony Robbins. Plain list of 5 names, nothing more, please",

)

print(response.text)

# print("List of models that support generateContent:\n")
# for m in client.models.list():
#     for action in m.supported_actions:
#         if action == "generateContent":
#             print(m.name)

# print("List of models that support embedContent:\n")
# for m in client.models.list():
#     for action in m.supported_actions:
#         if action == "embedContent":
#             print(m.name)