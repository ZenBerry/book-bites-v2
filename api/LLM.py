from google import genai

client = genai.Client(api_key="AIzaSyCO4CaWfuolgFco93vdGbYEjqOf9CcqXws")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Please list 5 books similar to Moral Letters to Lucilius. Plain list of 5 names, nothing more, please",

)

print(response.text)