class ClientException(Exception):
    pass


class StripeClientException(ClientException):
    pass


class BraintreeClientException(ClientException):
    pass


class ProcessorException(Exception):
    pass


class StripeProcessorException(ProcessorException):
    pass


class BraintreeProcessorException(ProcessorException):
    pass
