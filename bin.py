class Bin:
  
  def __init__(self, index, floor, ceiling, is_last_bin):
    self.index = index
    self.floor = floor
    self.ceiling = ceiling
    self.range = self.floor - self.ceiling
    self.is_last_bin = is_last_bin
    self.members_asc = []    
    
  def count(self):
    return len(self.members_asc)    
    
  def add(self, val):
    
    if self.is_last_bin == True:
      if (self.floor <= val) and (val <= self.ceiling):
        self.members_asc.append(val)
      else:
        return False
    else: # if self.is_last_bin == False
      if (self.floor <= val) and (val < self.ceiling):
        self.members_asc.append(val)
      else:
        return False
        
    return True
    
  def sort(self):
    self.members_asc.sort()
      
  def __unicode__(self):
    s = '[%s, %s' % (str(self.floor), str(self.ceiling))
    if (self.is_last_bin == False):
      s = s + ')'
    else:
      s = s + ']'
    s = s + ': ' + str(self.count())
    return s
    
  def __str__(self):
    s = '[%.4f, %.4f' % (self.floor, self.ceiling)
    if (self.is_last_bin == False):
      s = s + ')'
    else:
      s = s + ']'
    s = s + ': ' + str(self.count())
    return s

