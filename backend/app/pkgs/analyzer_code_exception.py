class AnalyzerCodeException(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class AnalyzerCodeProcessException(Exception):
    def __init__(self, message, error_code, task_no, repo):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.task_no = task_no
        self.repo = repo
