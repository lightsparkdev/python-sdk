# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.utils.crypto import decrypt_private_key, encrypt


class TestCrypto:
    def test_encrypt_decrypt(self):
        header, encrypted = encrypt(b"testtest", "password")
        decrypted = decrypt_private_key(header, encrypted, "password")
        assert decrypted == b"testtest"

    def test_decrypt_sample_v0(self):
        sample = "U2FsdGVkX18d2yysCotcO4uqqed6xNcrb3zF/3lSxLo="
        header = "AES_256_CBC_PBKDF2_5000_SHA256"
        assert decrypt_private_key(header, sample, "password") == b"testtest"

    def test_decrypt_sample_v1(self):
        sample = "8dX7K3BAUM4LFuL8qcau2LT2NFEPP/Vb"
        header = '{"v": 1, "i": 500000}'
        decrypted = decrypt_private_key(header, sample, "password")
        assert decrypted == b"testtest"

    def test_decrypt_sample_v2(self):
        sample = "PxscHMUeWUQnHp2eURMjDRcY2BB6I+MP/asNyBhVfCI="
        header = '{"v": 2, "i": 500000}'
        decrypted = decrypt_private_key(header, sample, "password")
        assert decrypted == b"testtest"

    def test_decrypt_sample_v2lsv2(self):
        sample = "X7lDIfxMsCj1HDKk9hjF4OUAAoZZPQOsA6xaMJCk7rsciI1VvPWTbi8axRI="
        header = '{"v": 2, "lsv": 2, "i": 500000}'
        decrypted = decrypt_private_key(header, sample, "password")
        assert decrypted == b"testtest"

    def test_decrypt_sample_v3(self):
        sample = "X7lDIfxMsCj1HDKk9hjF4OUAAoZZPQOsA6xaMJCk7rsciI1VvPWTbi8axRI="
        header = '{"v": 3, "i": 500000}'
        decrypted = decrypt_private_key(header, sample, "password")
        assert decrypted == b"testtest"

    def test_decrypt_sample_v4(self):
        sample = "HMo/irU7oTQj5GhkUurcZwi+uNeeBMaKirsNOtjj6kFubm74Apa1zA=="
        header = '{"v": 4, "i": 500000}'
        decrypted = decrypt_private_key(header, sample, "password")
        assert decrypted == b"testtest"
