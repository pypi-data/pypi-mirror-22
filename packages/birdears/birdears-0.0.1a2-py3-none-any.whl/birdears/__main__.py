"__Main__ docs are here."

from . import click

from . import _Getch
from . import INTERVALS
from . import DEBUG
# this is for debugging


def print_stuff(question):
    padd = "─" * 30  # vim: insert mode, ^vu2500
    print("""
{}

Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
Is Note Chromatic: {} |
Scale: {}, Octave: {}
Resolution: ,
Chromatic: {}
Concrete Scale: {} | Chroma Concrete: {}
{}
""".format(
        padd,
        question.concrete_tonic,
        question.interval.note_and_octave,
        "─".join(INTERVALS[question.interval.semitones][1:]),
        question.interval.semitones,
        question.interval.is_chromatic,
        "─".join(question.scales['diatonic'].scale),
        "{}-{}".format(question.octave, question.octave + 1),
        "─".join(question.scales['chromatic'].scale),
        "─".join(question.scales['diatonic_pitch'].scale),
        "─".join(question.scales['chromatic_pitch'].scale),
        padd,
    ))


def print_stuff_dictation(question):
    padd = "─" * 30  # vim: insert mode, ^vu2500
    print("""
{}

Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
Scale: {}, Octave: {}
Chromatic: {}
Concrete Scale: {} | Chroma Concrete: {}
{}
""".format(
        padd,
        question.concrete_tonic,
        "─".join(map(str, question.question_phrase)),
        "─".join([INTERVALS[n][1] for n in question.question_phrase]),
        "─".join([str(n) for n in question.question_phrase]),
        "─".join(question.scales['diatonic'].scale),
        "{}-{}".format(question.octave, question.octave + 1),
        "─".join(question.scales['chromatic'].scale),
        "─".join(question.scales['diatonic_pitch'].scale),
        "─".join(question.scales['chromatic_pitch'].scale),
        padd,
    ))


@click.group()
def cli():
    pass


@cli.command()
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']), default='major')
@click.option('-t', '--tonic', type=str, default=None)
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None)
@click.option('-d', '--descending', is_flag=True)
@click.option('-c', '--chromatic', is_flag=True)
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None)
def melodic(*args, **kwargs):
    kwargs.update({'exercise': 'melodic'})
    ear(**kwargs)


@cli.command()
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']), default='major')
@click.option('-t', '--tonic', type=str, default=None)
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None)
@click.option('-d', '--descending', is_flag=True)
@click.option('-c', '--chromatic', is_flag=True)
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None)
def harmonic(*args, **kwargs):
    kwargs.update({'exercise': 'harmonic'})
    ear(**kwargs)


@cli.command()
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']), default='major')
@click.option('-i', '--max_intervals', type=click.IntRange(2, 12), default=3)
@click.option('-x', '--n_notes', type=click.IntRange(3, 10), default=4)
@click.option('-t', '--tonic', type=str, default=None)
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None)
@click.option('-d', '--descending', is_flag=True)
@click.option('-c', '--chromatic', is_flag=True)
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None)
def dictation(*args, **kwargs):
    kwargs.update({'exercise': 'dictation'})
    ear(**kwargs)


#def ear(exercise,mode,tonic,octave,descending,chromatic,n_octaves):
def ear(exercise, **kwargs):
    #print(exercise)
    #print(kwargs)

    if exercise == 'dictation':
        from .questions.melodicdictation import MelodicDictationQuestion
        #dictate_notes = 4
        dictate_notes = kwargs['n_notes']
        MYCLASS = MelodicDictationQuestion
        MYPRINT = print_stuff_dictation

    elif exercise == 'melodic':
        from .questions.melodicinterval import MelodicIntervalQuestion
        MYCLASS = MelodicIntervalQuestion
        dictate_notes = 1
        MYPRINT = print_stuff

    elif exercise == 'harmonic':
        from .questions.harmonicinterval import HarmonicIntervalQuestion
        MYCLASS = HarmonicIntervalQuestion
        dictate_notes = 1
        MYPRINT = print_stuff

    getch = _Getch()

    new_question_bit = True

    while True:
        if new_question_bit is True:

            new_question_bit = False

            input_keys = []
            # question = MelodicDictateQuestion(mode='major',descending=True)
            question = MYCLASS(**kwargs)
            # question = HarmonicIntervalQuestion(mode='major')
            # question = HarmonicIntervalQuestion(mode='major')

            # debug
            if DEBUG:
                MYPRINT(question)

            question.question.play()

        user_input = getch()

        # any response input interval from valid keys
        if user_input in question.keyboard_index and user_input != ' ':  # spc

            input_keys.append(user_input)
            print(user_input, end='')

            if len(input_keys) == dictate_notes:
                response = question.check_question(input_keys)

                if response['is_correct']:
                    print("Correct! It is {}".
                          format(response['correct_response_str']))
                else:
                    print("It is incorrect..."
                          "You replied {} but the correct is {}"
                          .format(response['user_response_str'],
                                  response['correct_response_str']))

                question.resolution.play()

                new_question_bit = True

        # q - quit
        elif user_input == 'q':
            exit(0)

        # r - repeat interval
        elif user_input == 'r':
            question.question.play()


if __name__ == "__main__":
    # well it is..

    cli()
