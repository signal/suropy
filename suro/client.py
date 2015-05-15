from logging import getLogger
import struct
import zlib

from suro.thriftgen import SuroServer
from suro.thriftgen.ttypes import TMessageSet

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

logger = getLogger(__name__)

APP_NAME = "suropy-client"

def write_messages_into(write_buffer, routing_key, *payloads):
  for payload in payloads:
    key_length = len(routing_key)
    payload_length = len(payload)
    # modified UTF 8 + payload length + payload
    fmt = '!H%dsi%ds' % (key_length, payload_length)
    map(write_buffer.append, struct.pack(fmt, key_length, routing_key, payload_length, payload))

def generate_crc(read_only_buffer):
  return zlib.crc32(read_only_buffer) & 0xffffffff

def create_message_set(app_name, routing_key, *messages):
  """Creates a single TMessageSet for all the messages passed in.

  TODO: support LZF compression for the message set.
  """

  write_buffer = bytearray()
  write_messages_into(write_buffer, routing_key, *messages)
  read_only_buffer = buffer(write_buffer)
  return TMessageSet(app=app_name, compression=0, numMessages=len(messages),
    crc=generate_crc(read_only_buffer), messages=read_only_buffer)

class SuroClient(object):
  """A synchronous client for a suro-server, that sends messages sets one at a time.

  This class is written as a context manager, to automatically close the socket, which
  is opened automatically.
  """

  def __init__(self, hostname="localhost", port=7101, app_name=APP_NAME):
    self.transport = TTransport.TFramedTransport(TSocket.TSocket(hostname, port))
    self.client = SuroServer.Client(TBinaryProtocol.TBinaryProtocol(self.transport))
    self.app_name = app_name

  def send_messages(self, routing_key, *messages):
    try:
      self.client.process(create_message_set(self.app_name, routing_key, *messages))
    except:
      logger.exception("Unable to send messages")

  def __enter__(self):
    self.transport.open()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.transport.close()
