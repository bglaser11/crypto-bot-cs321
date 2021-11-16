# databse connection
from replit import db

# stores the bookmarks for the user in the database

# class Bookmarks
class bookmarks:

  # constructor for the bookmarks to initialize it
  def __init__(self, user):
    self.user = user

  """"
  addBookmark: appends a bookmark to the list
  paramter: currency
  """
  def addBookmark(self, currency):
    keys = db.keys()
    user = str(self.user)

    # checks to see if bookmark list is already present
    if user not in keys:
      print("so i worked")
      db[user] = []
    
    # gets the bookmarks set
    s = db[user]

    # add currency only once to the list
    if currency in s:
      return "can't add as already in bookmarks"
    else:
      s.append(currency)

    # saves the value in db
    db[self.user] = s

    return "currency added successfully"

  """"
  removeBookmark: appends a bookmark to the list
  paramter: currency
  """
  def removeBookmark(self, currency):
    keys = db.keys()
    user = str(self.user)

    # user doesn't have any bookmarks
    if user not in keys:
      return "unable to find currency to remove"

    listOfBookmarks = db[user]

    for curr in listOfBookmarks:
      if curr == currency:
        listOfBookmarks.remove(currency)
        db[user] = listOfBookmarks
        return "successfully removed from bookmarks"
    
    return "unable to find currency to remove"
      
  """"
  getBookmark: returns a list of bookmark
  """
  def getBookmark(self):
    keys = db.keys()
    user = str(self.user)

    # checks to see if bookmark list is already present
    if user in keys:
      return db[user]
    
    return []
