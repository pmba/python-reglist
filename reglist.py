from functools import wraps

class _Analyser:
  def __init__(self, debug=False):
    self._debug = debug

  def debug(func):
    @wraps(func)
    def wrap(*args, **kw):
      if (args[0]._debug):
        print(f'Running {func.__name__}')
      return func(*args, **kw)
    return wrap

  def _current_token(self) -> str:
    return self._token_list[self._current_position]


  def _next_token(self):
    self._current_position += 1


  def _raise_error(self):
    print(f'Exception: Invalid Syntax at [{self._current_position}]')
    print(f'  {self._original}')
    print(f'  {"^":>{self._current_position + 1}}')

  @debug
  def analyse(self, sentence:str) -> list:
    self._original = sentence
    self._token_list = [char for char in sentence]
    self._current_position = 0
    self._final_tokens = []

    try:
      self._expression()
      return self._final_tokens
    except:
      self._raise_error()
      exit(1)

  @debug
  def _interval(self):
    if (self._current_token() == '-'):
      self._next_token()
      self._sentence(partial_interval=True)

    if (self._current_token() == ']'):
      # EOF
      return

    self._sentence()
  
  @debug
  def _sentence(self, partial_interval=False):
    if (self._current_token().isalnum()):
      self._next_token()

      if (partial_interval):
        init = self._original[self._current_position-3]
        end = self._original[self._current_position-1]
        self._final_tokens.append([init, end])
      else:
        if (self._original[self._current_position] != '-'):
          unique = self._original[self._current_position-1]
          self._final_tokens.append([unique])

      self._interval()
      self._expression()
    else:
      self._raise_error()

  @debug
  def _expression(self) -> bool:
    if (self._current_position < len(self._token_list)):
      if (self._current_token() == '['):
        self._next_token()
        self._sentence()
        if (self._current_token() == ']'):
          self._next_token()
        else:
          self._raise_error()
      elif (self._current_token().isalnum()):
        self._next_token()
        unique = self._original[self._current_position-1]
        self._final_tokens.append([unique])
        self._expression()


class reglist:
  @staticmethod
  def build(regex):
    analyser = _Analyser(debug=False)
    result = analyser.analyse(regex)
    final_list = []

    for element in result:
      if (len(element) == 2):
        final_list += [chr(char) for char in range(ord(element[0]), ord(element[1]) + 1)]
      else:
        final_list += element

    return final_list
