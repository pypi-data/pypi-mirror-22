"__Main__ docs are here."

from . import click

from . import _Getch

from . import INTERVALS
from . import DIATONIC_MODES

from . import DEBUG

from .interfaces.commandline import CommandLine

CTX_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)


main_epilog = """
You can use '<command> --help' to show options for a specific command.

More info at https://github.com/iacchus/birdears
"""


@click.group(options_metavar='', subcommand_metavar='<command> [options]',
             epilog=main_epilog,
             context_settings=CTX_SETTINGS)
def cli():
    """birdears ─ Functional Ear Training for Musicians!"""

    pass

melodic_epilog = """
In this exercise birdears will play two notes, the tonic and the interval
melodically, ie., one after the other and you should reply which is the correct
distance between the two.
"""


@cli.command(options_metavar='[options]', epilog=melodic_epilog)
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']),
              default='major', help="Mode of the question.")
@click.option('-t', '--tonic', type=str, default=None, metavar='<note>',
              help='Tonic of the question.')
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None,
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Whether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=1,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=None,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
def melodic(*args, **kwargs):
    """Melodic interval recognition
    """

    print(kwargs['valid_intervals'])
    kwargs.update({'exercise': 'melodic'})
    CommandLine(**kwargs)

harmonic_epilog = """
In this exercise birdears will play two notes, the tonic and the interval
harmonically, ie., both on the same time and you should reply which is the
correct distance between the two.
"""


@cli.command(options_metavar='[options]', epilog=harmonic_epilog)
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']),
              default='major', help="Mode of the question.")
@click.option('-t', '--tonic', type=str, default=None, metavar='<note>',
              help='Tonic of the question.')
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None,
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Whether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=None,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
def harmonic(*args, **kwargs):
    """Harmonic interval recognition
    """

    kwargs.update({'exercise': 'harmonic'})
    CommandLine(**kwargs)


dictation_epilog = """
In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should reply the correct intervals of the
melodic dictation.
"""


@cli.command(options_metavar='[options]', epilog=dictation_epilog)
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']),
              default='major', help="Mode of the question.")
@click.option('-i', '--max_intervals', type=click.IntRange(2, 12), default=3,
              metavar='<n max>',
              help='Max random intervals for the dictation.')
@click.option('-x', '--n_notes', type=click.IntRange(3, 10), default=4,
              metavar='<n notes>',
              help='Number of notes for the dictation.')
@click.option('-t', '--tonic', type=str, default=None, metavar='<note>',
              help='Tonic of the question.')
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None,
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Wether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=None,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
def dictation(*args, **kwargs):
    """Melodic dictation
    """

    kwargs.update({'exercise': 'dictation'})
    CommandLine(**kwargs)


instrumental_epilog = """
In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should play the correct melody in you musical
instrument.
"""


@cli.command(options_metavar='[options]', epilog=instrumental_epilog)
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']),
              default='major', help="Mode of the question.")
@click.option('-w', '--wait_time', type=click.IntRange(1, 60), default=7,
              metavar='<seconds>',
              help='Time in seconds for next question/repeat.')
@click.option('-u', '--n_repeats', type=click.IntRange(1, 10), default=1,
              metavar='<times>', help='Times to repeat question.')
@click.option('-i', '--max_intervals', type=click.IntRange(2, 12), default=3,
              metavar='<n max>',
              help='Max random intervals for the dictation.')
@click.option('-x', '--n_notes', type=click.IntRange(3, 10), default=4,
              metavar='<n notes>',
              help='Number of notes for the dictation.')
@click.option('-t', '--tonic', type=str, default=None, metavar='<note>',
              help='Tonic of the question.')
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None,
              metavar='<octave>', help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Wether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=None,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
def instrumental(*args, **kwargs):
    """Instrumental melodic time-based dictation
    """

    kwargs.update({'exercise': 'instrumental'})
    CommandLine(**kwargs)

load_epilog = """
Loads exercise from file.
"""


@cli.command(options_metavar='', epilog=load_epilog)
@click.argument('filename', type=click.File(), metavar='<filename>')
def load(filename, *args, **kwargs):
    """Loads exercise from .toml config file <filename>.
    """

    from .toml import toml

    toml_file_str = filename.read()
    config_dict = toml.loads(toml_file_str)

    CommandLine(**config_dict)

if __name__ == "__main__":

    cli()
