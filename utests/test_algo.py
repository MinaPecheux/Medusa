from medusa import Medusa


class TestAlgo():

    def test_vigenere(self):
        text = 'hello world'

        processor = Medusa(algo='vigenere',
                           params=dict(key='key',
                                       complement_key='complement_key'))
        encoded = processor.encode(text)

        assert encoded == 'ÓÐ×ÑèÜèÝ×Ý'

        decoded = processor.decode(encoded)
        assert decoded == text
