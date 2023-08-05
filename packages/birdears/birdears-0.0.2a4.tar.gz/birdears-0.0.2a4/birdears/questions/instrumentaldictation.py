from random import choice

from ..questionbase import QuestionBase

from ..interval import DiatonicInterval
from ..interval import ChromaticInterval

from .. import DIATONIC_MODES
from .. import MAX_SEMITONES_RESOLVE_BELOW
from .. import INTERVALS

from ..scale import DiatonicScale
from ..scale import ChromaticScale

from ..sequence import Sequence
from ..resolution import Resolution

from ..interfaces.commandline import COLS
from ..interfaces.commandline import center_text


class InstrumentalDictationQuestion(QuestionBase):
    """Implements an instrumental dictation test.
    """

    def __init__(self, mode='major', wait_time=11, n_repeats=1,
                 max_intervals=3, n_notes=4, tonic=None, octave=None,
                 descending=None, chromatic=None, n_octaves=None,
                 *args, **kwargs):
        """Inits the class.

        Args:
            mode (str): A string representing the mode of the question.
                Eg., 'major' or 'minor'.
            wait_time (float): Wait time in seconds for the next question or
                repeat.
            n_repeats (int): Number of times the same dictation will be
                repeated before the end of the exercise.
            max_intervals (int): The maximum number of random intervals the
                question will have.
            n_notes (int): The number of notes the melodic dictation will have.
            tonic (str): A string representing the tonic of the question,
                eg.: 'C'; if omitted, it will be selected randomly.
            octave (int): A scienfic octave notation, for example, 4 for 'C4';
                if not present, it will be randomly chosen.
            descending (bool): Is the question direction in descending, ie.,
                intervals have lower pitch than the tonic.
            chromatic (bool): If the question can have (True) or not (False)
                chromatic intervals, ie., intervals not in the diatonic scale
                of tonic/mode.
            n_octaves (int): Maximum number of octaves of the question.
        """

        super(InstrumentalDictationQuestion, self).\
            __init__(mode=mode, tonic=tonic, octave=octave,
                     descending=descending, chromatic=chromatic,
                     n_octaves=n_octaves, *args, **kwargs)

        self.wait_time = wait_time
        self.n_repeats = n_repeats

        self.question_duration = 0.5
        self.question_delay = 0.5
        self.question_pos_delay = 0

        self.resolution_duration = 2.5
        self.resolution_delay = 0.5
        self.resolution_pos_delay = 1

        # FIXME: for chromatics
        if not chromatic:
            INTERVAL_CLASS = DiatonicInterval
        else:
            INTERVAL_CLASS = ChromaticInterval

        question_intervals = [INTERVAL_CLASS(mode=mode, tonic=self.tonic,
                              octave=self.octave, n_octaves=n_octaves,
                              descending=descending)
                              for _ in range(max_intervals)]

        self.question_phrase_intervals = [choice(question_intervals)
                                          for _ in range(n_notes-1)]

        self.question_phrase = [0]

        self.question_phrase.extend([interval.semitones
                                     for interval
                                     in self.question_phrase_intervals])

        self.question = self.make_question(self.question_phrase)

        # self.resolution = Sequence(self.question.elements,
        #                           duration=self.resolution_duration,
        #                           delay=self.resolution_delay,
        #                           pos_delay=self.resolution_pos_delay)

        resolve = Resolution(method='resolve_to_nearest_tonic',
                             duration=self.resolution_duration,
                             delay=self.resolution_delay,
                             pos_delay=self.resolution_pos_delay)

        # self.resolution = resolve.resolve_to_nearest_tonic(chromatic,
        # self.mode,
        self.resolution =\
            resolve.resolve(chromatic=chromatic, mode=self.mode,
                            tonic=self.tonic,
                            intervals=self.question_phrase_intervals,
                            descending=descending)

    def make_question(self, phrase_semitones):
        return Sequence([self.scales['chromatic_pitch'].scale[n]
                        for n in phrase_semitones],
                        duration=self.question_duration,
                        delay=self.question_delay,
                        pos_delay=self.question_pos_delay)

    def play_question(self):

        for r in range(self.n_repeats):
            self.question.play()

            for i in range(self.wait_time):
                time_left = str(self.wait_time - i).rjust(3)
                text = '{} seconds remaining...'.format(time_left)
                print(center_text(text, sep=False), end='')
                self.question._wait(1)

    def play_resolution(self):

        for sequence in self.resolution:
            sequence.play()

    def check_question(self):
        """Checks whether the given answer is correct.

        This currently doesn't applies to instrumental dictation questions.

        """

        global INTERVALS

        intervals_str = "".join([INTERVALS[s][1].center(7)
                                for s in self.question_phrase])
        notes_str = "".join([self.scales['chromatic_pitch'].scale[s].center(7)
                            for s in self.question_phrase])

        correct_response_str = """\
The intervals and notes of this question:

{intervals}
{notes}
""".format(**dict(intervals=intervals_str, notes=notes_str))
        response = {
            'correct_semitones': self.question_phrase,
            'correct_response_str': correct_response_str
        }

        return response
