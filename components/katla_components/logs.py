from .constants import Literal
from datetime import datetime
from warnings import warn

LogTypes = Literal['warn', 'license', 'error', 'info']
MessageProperty = Literal['message', 'type', 'time']

class Logs:

    def __init__(self) -> None:
        self.messages: list[dict[MessageProperty, str]] = []

    def log(self, message: str, type: LogTypes = 'info', format_print: str = '[<time>] [<type>] <message>') -> None:
        current_time = datetime.now().strftime(r'%d/%m/%Y - %H:%M:%S')

        match type:

            case 'info':
                print(format_print.replace('<time>', current_time, 1)
                                  .replace('<type>', type.upper(), 1)
                                  .replace('<message>', message, 1)
                )

            case 'license':
                print(f'\033[36m{message}\033[0m')

            case 'warn':
                warn(message)

            case 'error':
                print(f'\033[31m{format_print}\033[0m'.replace('<time>', current_time, 1)
                                                      .replace('<type>', type.upper(), 1)
                                                      .replace('<message>', message, 1)
                )

            case _:
                raise TypeError('type:', type)

        self.messages.append({
            'message': message,
            'type': type,
            'time': current_time
        })