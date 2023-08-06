import telethon.helpers as utils
from telethon.utils import BinaryReader, BinaryWriter


class AuthKey:
    def __init__(self, data):
        self.key = data

        with BinaryReader(utils.sha1(self.key)) as reader:
            self.aux_hash = reader.read_long(signed=False)
            reader.read(4)
            self.key_id = reader.read_long(signed=False)

    def calc_new_nonce_hash(self, new_nonce, number):
        """Calculates the new nonce hash based on the current class fields' values"""
        with BinaryWriter() as writer:
            writer.write(new_nonce)
            writer.write_byte(number)
            writer.write_long(self.aux_hash, signed=False)

            new_nonce_hash = utils.calc_msg_key(writer.get_bytes())
            return new_nonce_hash
