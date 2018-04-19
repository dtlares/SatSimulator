""" command_encoding module provides functions to encode and decode data"""
import pickle


class CommandEncoding:
    """ Functions for encoding and decoding data"""

    @staticmethod
    def command_encoder(obj):
        """Encodes the provided data"""
        return pickle.dumps(obj)

    @staticmethod
    def command_decoder(obj):
        """Decodes de provided data"""
        return pickle.loads(obj)
