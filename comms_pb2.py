# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: comms.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x63omms.proto\"&\n\x13sendCommandToDevice\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\"#\n\x0freceiveResponse\x12\x10\n\x08response\x18\x01 \x01(\t2G\n\x10SmartHomeService\x12\x33\n\x07\x43ommand\x12\x14.sendCommandToDevice\x1a\x10.receiveResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'comms_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SENDCOMMANDTODEVICE._serialized_start=15
  _SENDCOMMANDTODEVICE._serialized_end=53
  _RECEIVERESPONSE._serialized_start=55
  _RECEIVERESPONSE._serialized_end=90
  _SMARTHOMESERVICE._serialized_start=92
  _SMARTHOMESERVICE._serialized_end=163
# @@protoc_insertion_point(module_scope)