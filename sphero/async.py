# coding: utf-8
import struct

class metacls(type):
    def __new__(mcs, name, bases, dicta):
        print('metaclass create ' + name)
        return type.__new__(mcs, name, bases, dicta)

class AsyncMessage(object):
    __metaclass__ = metacls

    SOP1 = 0xFF
    SOP2 = 0xFE
    did = None
    cid = None
    code = 0x00
    DLEN = 0

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

    def __new__(cls):
        print('aaa')

        return super.__new__(super)


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

class SelfLevelResult(Sphero):
    cid = 0x09
    code = 0x0B

class SoulData(Sphero):
    cid = 0x43
    code = 0x0D
