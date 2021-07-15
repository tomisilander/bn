import types
import score
import bdeuscore
import pen_ml_score
import data

def getscorer(bdt, scoretype, param, 
              do_cache=True, do_storage=True, cachefile=None):
    # So that one does not need to load the data just to get scorer

    if isinstance(bdt, types.StringTypes):
        bdt = data.Data(bdt)
 
    if scoretype == 'BDeu':
        return bdeuscore.BDeuScore(bdt, param, 
                                   do_cache, do_storage, cachefile)
    elif scoretype in score.cscorefuncs:
        return pen_ml_score.PenMLScore(bdt,score.cscorefuncs[scoretype],
                                       do_cache, do_storage, cachefile)
    else:
        print 'Unknown scoretype', scoretype
