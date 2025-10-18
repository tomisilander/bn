from argparse import ArgumentParser


def get_arg_adder(parser:ArgumentParser, exceptions):

    def add_arg(*argnames, **argkwargs):
        in_exceptions = any(argname in exceptions for argname in argnames)
        if not in_exceptions:
            parser.add_argument(*argnames, **argkwargs)

    return add_arg
    
def add_learning_args(parser:ArgumentParser, exceptions=[]):

    add = get_arg_adder(parser, exceptions  )

    add('bdtfile')
    add('-g', '--score_type', default='BDeu')
    add('-e', '--ess', type=float, default=1.0)
    add('-t', '--time', help='like -t \"4d 3h 5m 5[s]\" (default till SIGUSR2)')
    add('-i', '--iters', type=int, default=None)
    add('-c', '--constraint_file')
    add('-o', '--outfile', help='Can be a directory')
    add('-s', '--startbn', help='file to start search from')
    add('-m', '--cachefile')    
    

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    add_learning_args(parser)
    args = parser.parse_args()
    print(args)

