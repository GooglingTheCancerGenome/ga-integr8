#Testing of the Annotator script

from annotator import Annotator


annotator = Annotator()
region = dict()
region['chromosome'] = 'chr1'
region['chromosome2'] = 'chr1'
region['start'] = '1'
region['end'] = '100'

annotator.annotate(region)

