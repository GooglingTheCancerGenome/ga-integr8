#Testing of the Annotator script

from annotator import Annotator

#Example region that has all features
annotator = Annotator()
region = dict()
region['chromosome'] = 'chr1'
region['chromosome2'] = 'chr1'
region['start'] = '3541566'
region['end'] = '3541586'

annotator.annotate(region)

