# coding: utf-8
import sys
from struct import unpack

class metacls(type):

    def __new__(cls, name, bases, attr):
        new__ = type.__new__(cls, name, bases, attr)
        print(attr)
        if 'code' in attr:
            new_name = "response_" + str(attr['code'])
            response_handler_class = type(new_name, (ResponseHandler, ), {'parse_handler': new__})
            setattr(sys.modules[__name__], new_name, response_handler_class)
            new__.response_handler = response_handler_class
        return new__


class ResponseHandler(object):
    listeners = set()
    parse_handler = None

    @classmethod
    def registerListener(cls, listener):
        cls.listeners.add(listener)

    @classmethod
    def unregisterListener(cls, listener):
        cls.listeners.remove(listener)

    @classmethod
    def notifyListeners(cls, body):
        for listener in cls.listeners:
            listener.receivedResponse(cls.parse_handler.parse(body))

def parse_response(async_response):
    code = ord(async_response[2:3])
    response_class_name = 'response_' + str(code)
    response_class = getattr(sys.modules[__name__], response_class_name)
    response_class.notifyListeners(async_response[5:])

class AsyncMessage(object):
    SOP1 = 0xFF
    SOP2 = 0xFE
    did = None
    cid = None
    code = 0x00
    DLEN = 0
    response_handler = None

    # TODO mapping of response codes to classes and callbacks
    # first idea:
    #   set_[code] -> response class -> callbacks
    #
    # for instance:
    #   user wants to listen for PowerNotification, they register
    #   PowerNotification creates static set with name set_01 in some class
    #   when asyc message arrives the code is checked and if there is a set for
    #   that code (in this case set_01) if exists we check for a proper class
    #   -> PowerNotification and make it parse the response data which will
    #   then be distributed among listeners contained within set_01

    __metaclass__ = metacls

    @classmethod
    def parse(cls, body):
        return body

    @classmethod
    def registerListener(cls, listener):
        cls.response_handler.registerListener(listener)

    @classmethod
    def unregisterListener(cls, listener):
        cls.response_handler.unregisterListener(listener)


class PreSleepWarning(AsyncMessage):
    code = 0x05

class MacroMarker(AsyncMessage):
    code = 0x06

class BasicPrintMessage(AsyncMessage):
    code = 0x08

class ErrorMessageAscii(AsyncMessage):
    code = 0x09

class ErrorMessageBinary(AsyncMessage):
    code = 0x0A

class GyroAxisLimitExceeded(AsyncMessage):
    code = 0x0C

class LevelUpNotification(AsyncMessage):
    code = 0x0E

class ShieldDamageNotification(AsyncMessage):
    code = 0x0F

class XPUpdateNotification(AsyncMessage):
    code = 0x10

class BoostUpdateNotification(AsyncMessage):
    code = 0x11



class Core(AsyncMessage):
    did = 0x00

class PowerNotification(Core):
    cid = 0x21
    code = 0x01

class Level1Diagnostic(Core):
    cid = 0x40
    code = 0x02



class Sphero(AsyncMessage):
    did = 0x02

class SensorData(Sphero):
    cid = 0x11
    code = 0x03

class ConfigBlock(Sphero):
    cid = 0x40
    code = 0x04

class CollisionDetected(Sphero):
    cid = 0x12
    code = 0x07

    @classmethod
    def parse(cls, body):
        return unpack("3hb2hBL", body)

class SelfLevelResult(Sphero):
    cid = 0x09
    code = 0x0B

class SoulData(Sphero):
    cid = 0x43
    code = 0x0D
