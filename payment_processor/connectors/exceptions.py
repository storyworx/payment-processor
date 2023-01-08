class ClientException(Exception):
    pass


class SolanaClientException(ClientException):
    pass


class ProcessorException(Exception):
    pass


class SolanaProcessorException(ProcessorException):
    pass
