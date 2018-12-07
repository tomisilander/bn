#!/usr/bin/python
import coliche, os
from bn_picture import bn2pic

def main(bnfile, format="gif", viewer="display", vdfile=None, 
         loners=False, center=None, awfile=None):
    picfile = "/tmp/%d.%s" % (os.getpid(), format)
    bn2pic(bnfile, picfile, format, vdfile, loners, center, awfile)
    os.system("%s %s" % (viewer, picfile))
    os.unlink(picfile)

if __name__ == "__main__":
    coliche.che(main,
                """bnfile
                -f --format format : (default gif)
                -v --viewer viewer : (default display)
                -n --vdfile vdfile : to add names to the picture
                -l --loners        : show orphan nodes too
                --mb center         : draw only markov blanket of center
                -w --arcweights awfile : draw arcweights
                """)
