from Zlibrary import Zlibrary

# Create Zlibrary object and login
Z = Zlibrary(email="zenberry.music@gmail.com", password="zlibPass8")

results = Z.search(message='The Great Gatsby', extensions='epub')

# info = Z.getBookInfo(bookid= results[0]["id"])

print(results['books'][0])


# # Get most popular books
# most_popular = Z.getMostPopular()

# # Downloading a book
# filename, filecontent = Z.downloadBook(most_popular["books"][0])

# # Writting file content to a file
# with open(filename, "wb") as bookfile:
#     bookfile.write(filecontent)