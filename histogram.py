import math
from decimal import *

from dataset import DataSet
from bin import Bin

class ClassIntervalType:
  STURGE = 0
  ROOT = 1
  THREESIGMA = 2
  CUSTOM = 3

class Histogram(DataSet):  
  '''# class interval length, L
  # sturge : L = (x_max - x_min) / (1 + 1.44 * n)
  # rule of thumb : L = (x_max - x_min) / sqrt(n)
  '''
  def __init__(self, data, interval_type=ClassIntervalType.STURGE):
    
    f = []
    for d in data:
      f.append(float(d))      
    data = f
    
    DataSet.__init__(self, data)
    self.interval_type = interval_type
    
    if self.interval_type != ClassIntervalType.THREESIGMA:    
      self.class_interval = self.calc_class_interval(interval_type, self.min, self.max, self.n);
      self.construct_bins(self.min, self.max, self.class_interval, False);
    else:
      sigma_span = 6
      min = self.mean - self.stdev * (sigma_span / 2)
      max = self.mean + self.stdev * (sigma_span / 2)
      self.class_interval = self.calc_class_interval(ClassIntervalType.THREESIGMA, min, max, sigma_span)
      self.construct_bins(min, max, self.class_interval, True)
      
    self.fill_bins()
    self.sort_bins()

    total = 0
    for bin in self.bins:
      total = total + bin.count()
    self.bin_contents_count = total
        
  def calc_class_interval(self, class_interval_type, min, max, sigma_span):
    '''
    '''
    interval = None
    if class_interval_type == ClassIntervalType.ROOT:
      interval = (max - min) / (1 + 1.44 * math.Log(n))
    elif class_interval_type == ClassIntervalType.STURGE:
      interval = (max - min) / math.sqrt(self.n)
    elif class_interval_type == ClassIntervalType.THREESIGMA:
      interval = (max - min) / self.n # assumes xMin = xMean - (3 * stdev); xMax = xMean + (3 * stdev)      
    return interval
      
  def construct_bins(self, left_edge, right_edge, interval, exclude_out_of_range_values):
    
    self.left_edge = left_edge
    self.right_edge = right_edge
    self.bin_range = right_edge - left_edge
    self.bin_count = int(self.bin_range / self.class_interval)
    
    self.bins = []
    self.outliers = []
    for i in range(self.bin_count):
      is_last_bin = (i >= self.bin_count - 1)

      self.bins.append(Bin(i, self.left_edge + (i * self.class_interval), self.left_edge + ((i + 1) * self.class_interval), is_last_bin))

  def fill_bins(self):    
    for item in self.data:      
      is_outside = True      
      for bin in self.bins:
        if (bin.add(item) == True):
          is_outside = False
          break      
      if is_outside == True:
        self.outliers.append(item)

  def sort_bins(self):
    for bin in self.bins:
      bin.sort()
  def bin_contrib_perc(self, target_bin):
    total = 0
    the_bin = None
    for bin in self.bins:
      total = total + bin.count()
      if bin == target_bin:
        the_bin = bin
        
    return 100 * the_bin.count() / total
    
  def report(self):
    log = []
    grand_total = 0
    for bin in self.bins:
      grand_total = grand_total + bin.count()
    for bin in self.bins:
      s = str(bin).ljust(35)
      count = int(20 * bin.count() / grand_total) 
      for i in range(count):
        s = s + '*'
      log.append(s)      
    return log