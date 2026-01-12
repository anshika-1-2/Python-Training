#classes and objects
class Dog:
    species = "Canines"  

    def __init__(self, name, age):
        self.name = name  
        self.age = age  

dog1 = Dog("Rockie", 6)  
dog2 = Dog("Bo", 3)  

print(dog1.name, dog1.age, dog1.species)  
print(dog2.name, dog2.age, dog2.species)  
print(Dog.species)  

#example2


class Playlist:
  def __init__(self, name):
    self.name = name
    self.songs = []

  def add_song(self, song):
    self.songs.append(song)
    print(f"Added: {song}")

  def remove_song(self, song):
    if song in self.songs:
      self.songs.remove(song)
      print(f"Removed: {song}")

  def show_songs(self):
    print(f"Playlist '{self.name}':")
    for song in self.songs:
      print(f"- {song}")

my_playlist = Playlist("Favorites")
my_playlist.add_song("Tay Tay")
my_playlist.add_song("Weeknd")
my_playlist.show_songs()