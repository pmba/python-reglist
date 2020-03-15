class RegSyntax:
    L_DELIMITER = "["
    R_DELIMITER = "]"
    RANGE_TOKEN = "-"
    IGNORE_TOKEN = "^"


class RegSyntaxError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class _RegAnalyser:
    def __init__(self, syntax: RegSyntax):
        self._syntax = syntax

    def analyse(self, sentence: str):
        self._sentence = sentence
        self._finalpos = len(sentence)
        self._position = 0

        self._prev_tk = ""

        self._to_ignore = False
        self._tokens = []
        self._ignoreds = []

        self._base_sentence()

        return self._tokens, self._ignoreds

    def _to_output(self, element: list):
        if self._to_ignore:
            self._ignoreds.append(element)
        else:
            self._tokens.append(element)

    def _error(self, message: str):
        raise SyntaxError(
            "\n"
            + message
            + f" at [:{self._position}]"
            + f"\n\n  {self._sentence}"
            + f"\n  {'^':>{self._position + 1}}"
        )

    def _ctoken(self) -> str:
        return self._sentence[self._position]

    def _next(self):
        self._position += 1

    def _eof(self):
        return self._position == self._finalpos

    def _base_sentence(self):
        if self._ctoken() == self._syntax.L_DELIMITER:
            self._next()
            self._sentence_list()
            if self._ctoken() == self._syntax.R_DELIMITER:
                self._next()
            else:
                self._error(f"'{self._syntax.R_DELIMITER}' Expected")
        else:
            self._error(f"'{self._syntax.L_DELIMITER}' Expected")

    def _sentence_list(self):
        if self._ctoken() == self._syntax.IGNORE_TOKEN:
            self._to_ignore = True
            self._next()
            if self._ctoken() == self._syntax.L_DELIMITER:
                self._next()
                if self._ctoken().isalnum():
                    self._prev_tk = self._ctoken()
                    self._next()
                    self._right_side()
                    if self._ctoken() == self._syntax.R_DELIMITER:
                        self._to_ignore = False
                        self._next()
                        self._sentence_list()
                    else:
                        self._error(f"'{self._syntax.R_DELIMITER}' Expected")
                else:
                    self._error(
                        f"'Ignored tokens block ({self._syntax.IGNORE_TOKEN}{self._syntax.L_DELIMITER}{self._syntax.R_DELIMITER}), must not be empty"
                    )
            else:
                raise Exception("[ expected")
        elif self._ctoken().isalnum():
            self._prev_tk = self._ctoken()
            self._next()
            self._right_side()
            self._sentence_list()

    def _right_side(self):
        if self._ctoken() == self._syntax.RANGE_TOKEN:
            self._next()
            if self._ctoken().isalnum():
                self._to_output(
                    [self._sentence[self._position - 2], self._sentence[self._position]]
                )
                self._prev_tk = ""
                self._next()
                self._right_side()
            else:
                self._error(f"An alphanumerical token [a-zA-z0-9] was expected")
        elif self._ctoken().isalnum():
            self._to_output(
                [
                    self._prev_tk
                    if self._prev_tk != ""
                    else self._sentence[self._position]
                ]
            )
            self._prev_tk = ""
            self._next()
            self._right_side()

        if self._prev_tk != "":
            self._to_output([self._prev_tk])
            self._prev_tk = ""


def _interval_range(interval: list):
    ini, end = interval
    ini = ord(ini)
    end = ord(end)

    return (ini, end + 1, 1) if ini <= end else (ini, end - 1, -1)


def reglist(sentence: str, syntax: RegSyntax = RegSyntax()) -> list:
    analyser = _RegAnalyser(syntax=syntax)
    result_list = []

    valid_tk = []
    invalid_tk = []
    intervals, ignoreds = analyser.analyse(sentence)

    for interval in intervals:
        if len(interval) == 1:
            valid_tk += interval[0]
        else:
            interval_range = _interval_range(interval)
            valid_tk += [chr(element) for element in range(*interval_range)]

    for ignored in ignoreds:
        if len(ignored) == 1:
            invalid_tk += ignored[0]
        else:
            ignored_range = _interval_range(ignored)
            invalid_tk += [chr(element) for element in range(*ignored_range)]

    return [token for token in valid_tk if token not in invalid_tk]

