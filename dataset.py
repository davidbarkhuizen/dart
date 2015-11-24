import math

class DataSet:

  def __init__(self, data):
    
    self.n = len(data)
    
    composite = list(zip(data, range(self.n)))
    composite.sort()    
    
    orig_idxs = []
    self.data = []
    for (datum, idx) in composite:      
      orig_idxs.append(idx)
      self.data.append(datum)    
    
    map_rank_to_orig_idx = {}
    for i in range(self.n):
      map_rank_to_orig_idx[i + 1] = orig_idxs[i]
    
    self.min = self.data[0]
    self.max = self.data[self.n - 1]
    
    self.range = self.max - self.min
    
    self.sum = 0
    for x in self.data:
      self.sum = self.sum + x
      
    self.mean = self.sum / self.n
    
    sq_sum = 0;
    for x in self.data:
      sq_sum = sq_sum + ((x - self.mean) * (x - self.mean))
    self.var = sq_sum / (float(self.n) - 1)    
    
    self.stdev = math.sqrt(self.var)
    
  def report(self):
    log = []
    log.append('count = %s' % str(self.n))
    log.append('min = %s, max = %s' % (str(self.min), str(self.max)))
    log.append('mean = %s +- stdev = %s' % (str(self.mean), str(self.stdev)))
    return log