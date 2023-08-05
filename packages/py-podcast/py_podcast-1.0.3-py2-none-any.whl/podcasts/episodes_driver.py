from episode_worker import EpisodeWorker
from models.series import Series
from models.episode import Episode
from storers.json_storer import JsonStorer
import csv
import os

class EpisodesDriver(object):
  """
  Drives the acquisition of episodes
  based on series that exist in csv's
  stored in `directory`
  """

  def __init__(self, directory, storer, num_threads=20):
    """Constructor"""
    self.directory   = directory
    self.storer      = storer
    self.num_threads = num_threads

  def eps_from_series(self):
    """
    Workhorse function that handles grabbing
    series data from csvs and
    """
    # Grab the CSV files
    csvs = []
    for _, _, filenames in os.walk('./{}'.format(self.directory)):
      csvs.extend(filenames)

    # Build series set
    series_set = set()
    for c in csvs:
      file_name = './{}/{}'.format(self.directory, c)
      reader = csv.DictReader(open(file_name, 'rb'))
      for line in reader:
        series_set.add(Series.from_line(line))

    # Series list to be handled by threads
    series = [s for s in series_set]

    # Threads dispatched
    threads = []
    for i in xrange(0, self.num_threads):
      t = EpisodeWorker(self.storer, series, i)
      threads.append(t)
      t.start()

    # Get them threads together
    for t in threads:
      t.join()
