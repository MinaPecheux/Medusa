from medusa import Medusa


class TestAlgo():

    def test_caesar(self):
        text = 'hello world'

        processor = Medusa(algo='caesar',
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

    def test_aes(self):
        text = 'hello world'

        processor = Medusa(algo='aes',
                           params=dict(password='password'))
        encoded = processor.encode(text)
        ctx = processor.get_context()

        decoded = processor.decode(encoded, iv=ctx['iv'], salt=ctx['salt'])

        assert decoded == text
        assert encoded != text
