class Card: # class not used yet

  def __init__(self, uid):
    self.uid = uid
    self.name = 'i have no name'
    self.mail = 'no@mail.yet'

  def __del__(self):
    class_name = self.__class__.__name__
    print class_name, "destroyed"

  def iAm(self):
    return "I am %d, mail me at %d" % self.name, self.mail