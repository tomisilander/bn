#!/usr/bin/python
import coliche, os
import bn2dot

def bn2pic(bnfile, picfile, 
           format="gif", vdfile=None, loners=False, center=None, awfile=None):
    dotfile = "/tmp/%d" % os.getpid()
    bn2dot.bn2dot(bnfile,dotfile,vdfile,loners,center,awfile)
    os.system("dot -T%s -o%s %s" % (format, picfile, dotfile))
    os.unlink(dotfile)

if __name__ == "__main__":
    coliche.che(bn2pic,
                """bnfile; picfile
                -f --format format : (default gif)
                -n --vdfile vdfile : to add names to the picture
                -l --loners        : show orphan nodes too
                --mb center         : draw only markov blanket of center
                -w --arcweights awfile : draw arcweights
                """)
