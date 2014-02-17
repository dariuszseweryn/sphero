# coding: utf-8
import struct


class Response(object):
    SOP1 = 0
    SOP2 = 1
    MRSP = 2
    SEQ = 3
    DLEN = 4

    CODE_OK = 0

    def __init__(self, header, data):
        self.header = header
        self.data = data

    @property
    def fmt(self):
        return '%sB' % len(self.data)

    def empty(self):
        return self.header[self.DLEN] == 1

    @property
    def success(self):
        return self.header[self.MRSP] == self.CODE_OK

    def seq(self):
        return self.header[self.SEQ]

    @property
    def body(self):
        return struct.unpack(self.fmt, self.data)


class GetRGB(Response):
    def __init__(self, header, body):
        super(GetRGB, self).__init__(header, body)
        # TODO: these values seem incorrect
        self.r = body[0]
        self.g = body[1]
        self.b = body[2]


class GetVersion(Response):
    def __init__(self, header, body):
        super(GetVersion, self).__init__(header, body)
        self.recv = body[0]
        self.mdl = body[1]
        self.hw = body[2]
        self.msa_ver = body[3]
        self.msa_rev = body[4]
        self.bl = body[5]
        self.bas = body[6]
        self.macro = body[7]
        self.api_maj = body[8]
        # TODO: Sphero_API_1.50.pdf says that there should be 10 bytes of data, but apparently there are only 9... who knows if these are correct...
        # self.api_min = body[9]


class GetChassisId(Response):
    def __init__(self, header, body):
        super(GetChassisId, self).__init__(header, body)
        self.chassis_id = ''.join(body)


class GetBluetoothInfo(Response):
    def __init__(self, header, body):
        super(GetBluetoothInfo, self).__init__(header, body)
        # TODO: len(name) == 16 then bta is appended - technically name can have len up to 48 chars, but... ?s
        self.name = self.data.split('\x00', 1)[0]
        self.bta = self.data[16:].split('\x00', 1)[0]
