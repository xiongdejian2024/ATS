# -*- coding: utf-8 -*-
"""
@File        : exception_error.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/09/22 22:55
@Description : 自定义各种异常
@Examples    :
"""
from contextlib import contextmanager
from typing import Generator, Type, Union

from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.logger import logger


class CustomException(Exception):
    def __init__(self, message):
        self.message = message


class IOSystemError(CustomException):
    pass


class SetVlanError(CustomException):
    pass


class NucAppError(CustomException):
    pass


class ObdIpError(CustomException):
    pass


class IpduError(CustomException):
    pass


class BusAppError(CustomException):
    pass


class LogManageError(CustomException):
    pass


class ConfigError(CustomException):
    pass


class SoaError(CustomException):
    pass


class DeploySoaPartnerError(CustomException):
    pass


class DOIPError(CustomException):
    pass


class DOCANError(CustomException):
    pass


class TosunError(CustomException):
    pass


class ToomossError(CustomException):
    pass


class CmdExecuteError(CustomException):
    pass


class AllureError(CustomException):
    pass


class WillowError(CustomException):
    pass


# 自定义http请求的异常类
class UnauthorizedError(CustomException):
    pass


class ClientError(CustomException):
    pass


class ServerError(CustomException):
    pass


class ExecutionFailError(CustomException):
    pass


class NoDataError(CustomException):
    pass


@contextmanager
def error_check(
        error_message: Union[StatusCode, str] = None,
        exception_type: Type[CustomException] = CustomException,
        callback: callable = None,
        *args,
        **kwargs
) -> Generator[None, None, None]:
    """Catches any exceptions and turns them into the new type while preserving the stack trace."""
    try:
        yield
    except Exception as error:  # pylint: disable=broad-except
        if error_message is None:
            raise exception_type(str(error)) from error
        else:
            if isinstance(error_message, StatusCode):
                call_error_msg = ''
                if callback:
                    try:
                        call_error_msg = callback(error_message=error_message, *args, **kwargs)
                    except Exception as e:
                        logger.debug(f"回调函数出现异常: {str(e)}", exc_info=True)
                error_message = f"{call_error_msg}{error_message.format_err_msg}"
                logger.exception(error_message)
            raise exception_type(error_message) from error
