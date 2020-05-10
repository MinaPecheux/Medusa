from medusa import Medusa


class TestAlgo():

    def test_shift(self):
        text = 'hello world'

        processor = Medusa(algo='shift',
                           params=dict(shift=1))
        encoded = processor.encode(text)

        assert encoded == 'ifmmp!xpsme'

        decoded = processor.decode(encoded)
        assert decoded == text

    def test_vigenere(self):
        text = 'hello world'

        processor = Medusa(algo='vigenere',
                           params=dict(key='key',
                                       complement_key='complement_key'))
        encoded = processor.encode(text)

        assert encoded == 'ÓÐ×ÑèÜèÝ×Ý'

        decoded = processor.decode(encoded)
        assert decoded == text
