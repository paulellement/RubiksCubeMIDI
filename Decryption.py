from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class GanGen2CubeEncrypter:
    #key = None
    #iv = None
    def __init__(self, key, iv):
        
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes (128-bit) long")
        if len(iv) != 16:
            raise ValueError("IV must be 16 bytes (128-bit) long")
        # Apply salt to key and iv
        salt = ([0x06, 0x3A, 0x02, 0x34, 0x12, 0xAB])
        tempkey = bytearray(key)
        tempiv = bytearray(iv)
        for i in range(6):
            tempkey[i] = (key[i] + salt[i]) % 0xFF
            tempiv[i] = (iv[i] + salt[i]) % 0xFF
        self._key = bytearray(tempkey)
        self._iv = bytearray(tempiv)

    def _encrypt_chunk(self, data):
        cipher = Cipher(algorithms.AES(self._key), modes.CBC(self._iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    def _decrypt_chunk(self, data):
        
        cipher = Cipher(algorithms.AES(self._key), modes.CBC(self._iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(data) + decryptor.finalize()

    def encrypt(self, data):
        if len(data) < 16:
            raise ValueError('Data must be at least 16 bytes long')
        encrypted_data = bytearray(data)
        # Encrypt 16-byte chunk aligned to message start
        encrypted_data[:16] = self._encrypt_chunk(encrypted_data[:16])
        # Encrypt 16-byte chunk aligned to message end
        if len(encrypted_data) > 16:
            encrypted_data[-16:] = self._encrypt_chunk(encrypted_data[-16:])
        return encrypted_data

    def decrypt(self, data):
        if len(data) < 16:
            raise ValueError('Data must be at least 16 bytes long')
        decrypted_data = bytearray(data)
        #print("data:", decrypted_data)
        # Decrypt 16-byte chunk aligned to message end
        if len(decrypted_data) > 16:
            decrypted_data[-16:] = self._decrypt_chunk(decrypted_data[-16:])
            #print("last 16 decrypted: ", decrypted_data[-16:])
        # Decrypt 16-byte chunk aligned to message start
        decrypted_data[:16] = self._decrypt_chunk(decrypted_data[:16])
        #print("first 16 decrypted: ", decrypted_data[:16])
        return decrypted_data


# IGNORE EVERYTHING BELOW, JUST USED TO TEST THE DECRYPTION
def main():
    lines = [
        '51e283c805867fea6e421b6cd864a42a4ed4d742',
        '6ab331cba51742d3b1206a7537a467f52e760bd9',
        '39f959c40bda49f8e0f94b994d2e8feb4a7e4dc1',
        '56895a9deffd266edeab2bd9a9e52ddddab35426',
        'a33ed0be08d52516ce0f49ae5d8f6798651ebafd',
        '1698c1f0ce523476c25e047adf9d3b0d09b775a3',
        '10dae8f2096356ccb30b4661db88e72e492a374e',
        '760316ea80829cb69192580d908a19a5ec159438',
        '8ed26e8d4aaa903ac328e66456572c27d01eea5c',
        '6cf19025d587746e5e65ee965f02e40b878a7fc1',
        'fa05a96307aa0394f62d19d21be49c327da12e46',
        '19f424f39fc42ed280f11a98b9393b26952f1726',
        'fca9008853125c9c51266b2d7cc4ec74ba21d0e4',
        'ab783acd9bcabe6b50d42db450c0dcddbddad7cb',
        '49a9f611a7a98ec8f0de34041a3cc686645f761c',
        '121a5bdb84cb9a8ca7cc8a0dbc7786d5e0de26a3',
        '990ce859786eecce33dce07018df93ccf2578395',
        '621a5582da87f13ce4f38786e7a8e31029db4d7b',
        '6a31bd16d4888a64cb2e62da20730f6ef1438bca',
        'ffa449c607e552f923d31a00d195aea37d172c7a',
        '8310363b286115a8ee1adebe0988fe2e20857aff',
        '0c0f70f1637325d2ef95cf8cf6ac279d67ec88d0',
        '4ae41f65f0c4e310eca5ecfc58f3d213f1eb73bc',
        'd6ebd7907c2ccd7ae84fecbf02c11f62d847b799',
        '970b9020fb51638cbdd3a37e0f6b315384e95986',
        'dfcdf9be9e7205322060c08de32a4d7acc493149',
        '98853ff3efbffd31ee9551a153abb37d4827855e',
        '4a23b9df9e165d21921a3351b20b32c35ae04fe2',
        '94e5b3b58ee1a34a24d6233caf60f70e78f14e40',
        '184901e42666f5b75e868a6de9ce6cef49d8d3bc',
        '22e91ae332c5b72257763a6a2d2231cb9e3c4e8d',
        '7d5de25f46e928298f8039479827db69342fe688',
        '75384f355a9b8fb3b27bd59d93423da882cfa922',
        '702eaa1002034b020d0f494b289a01a626a70c6e',
        'c7c9d57edf6af9fa5f92cee86dca1c6b25898ee9',
        'd4c1995907d0b2b70167063474e05d23a04b072e',
        'a673bc20666b75b3f3474a820a6394704b314fdb',
        'a8d56b265d4e0197cc07f06708dc25e442ed4417',
        'e6f71f892b5b97b8744b07b0c3d2bdc94ec93f30',
        'd1f7cb221dc90af87ec198933e6d6c3488a2b265',
        'bd22d0ffa8fed56a8e82c1c9a35e6d8df0efb66b',
        '2f0877482f6ce85e140f204739548f1ccc2cc049',
        '410e3f3d7ba928733680c71fe98bc0f315e9b7c1',
        'e56c7fda0fa7937b7a5e0cededfc4bde6920bf97',
        'ee97e1cb036b15c7122f02e9e96df8737354c644',
        'b1c1ec44f2b3610f378a2119dd31a7556b7df400',
        '720bca0b4598e8be416a3597bec15551c4e6f18d',
        '8f8d3f0b5cdb83cdfcd66015f1df1b17692ba1df',
        'bb8412a8b0d6d9ae0ffe4d9ab5a980efff17aa83',
        'fa1b39d73529fd75b168f6053aeef70d4343954b',
        '363f85c413364b1ceed2b565f636150c6c464537',
        '1df0ce6b92e3ce503116d5c50d17a6715add057e',
        'c7804faee8751965e5caef5a092da1f6fb09c2eb',
        'a9de51ac62689fc43758d44dacfaf336d93c00c7',
        'bb852a3affe8216af64e61aa1cd0ebcabb647014',
        '38aef362392c67db8046688b4d8f4a9ba1a82771',
        '9e16328ee63b5e5cd9e8f5aaab63639cd07668d6',
        '49b0eb7f01c24b2db16a7e491119bc8e4aaea59b',
        '62154f88290fcde94cd45cc45ab70de4681e6088',
        '475474ec64297dbf3769c88582cc3b74b3ce82e3',
        'f1697ffea7db10aea1985e1d356d0821b647fbc4',
        '5e3316d51cb0e4d1e96565731556dfc95cadca7d',
        'fa23b23d9cea74e5dc1530e5f39e831158020a4d',
        'e838d36425aa0a5190948a7cb2f6ae5405cbd4d9',
        '7dd0f50e1ab74e4cc9b2c503d591cd97670924c9',
        'ca8091524e8ea54f3417e143ef6cd5a9352dd6d3',
        '680cf80d1c03ecfb8ffef91073083c2ee5ea6ee7',
        '6cf0f01859a99b46a9d24830d84d0cfd778ed367',
        '0a768ad8a60b2a3c077b2029124343c4490c17fb',
        '3a63794747b95e0b1c6ffeaf4508f5bb23d31d39',
        '40dbc4abe624d28e53166afdb4d850f0804e7788',
        '30e2827635c3b7822c08e2e87104ab55dc5bc727',
        '80f758a7c6efb0800e413e2bf22dd867844867aa',
        '234ed5e4b734af692cfe4a8fa64b254c97874b1a',
        '7b0fc66a7b98bb8f3b0dd443a54f3026d6b5eb94',
        '99906e9a321b54c483a1a286c097690018272131',
        'b1e25906033edcb5e39af244acd374bb10fccb4e',
        'de1c67321292900a9c062d26dedfc03d1cb3e0ef',
        '973d8cf7409c28888aaf12ba580368cd9e0a5e0d',
        '3aabe14067292fea4504bb650b1b9fb60b218c00',
        '4ad8d7d69240439fc5ea09af3563ea00772a748a',
        '33ff72ad660b399aec12ac1f83c104823e1c4037',
        '3f16046bca2354034a4f04bdbbe33db150535d53',
        'dee5585452d33ce6f6e595ecd0f8b16bdc7233f3',
        '0f255b96689da975952ed060d46018268fb81c77',
        'c2e1d2fd2473ac9bffa3551d5d1a1ed4db79e3c7',
        '58af70679b44b85416bbc04357e69c675825fe23',
        '9d05e7c0eac636a4c36a2f25e00de4e6b257dd18',
        'eafbb8b0a8dcf03b1fb65ddb7d655ca1c400cb0a',
        '88e46e86556cb546a27125e554bcc10fdac8a1e4',
        'c66d73da8508ac1cf2273762619330a351319521',
        '387417f9a6a3e459ae0563b04080f8d61887c989',
        '65d857e4d10de7c7deaadb152d697c750a1cd13b',
        '77e7b8183974555d1679b9b44aeec756bb97a1ee',
        '9efbfb3cfbc8efa440acff18ac9465ff708c630e',
        '63440d17bcae94c08090a5a623393fcd42818cbe',
        '8833d39d397438cf167e6f68a6c14a5d3ea28a3f',
        '0de301df8305dfdebf9c0553900b8ce24d73d711',
        'abf3f7502b94b8aac70e15a1dd322000147624b5'
        
    ] 

    # Usage
    key = [0x01, 0x02, 0x42, 0x28, 0x31, 0x91, 0x16, 0x07, 0x20, 0x05, 0x18, 0x54, 0x42, 0x11, 0x12, 0x53]
    iv = [0x11, 0x03, 0x32, 0x28, 0x21, 0x01, 0x76, 0x27, 0x20, 0x95, 0x78, 0x14, 0x32, 0x12, 0x02, 0x43]
    print(key, iv)
    mac_address = "AB:12:34:02:3A:06"
    
 
    encrypter = GanGen2CubeEncrypter(key, iv)

    # Assuming 'data' is the encrypted data received from the BLE device
    for line in lines:

        line_bytes = bytes.fromhex(line)
        #print(bytearray(line_bytes))
    # Convert the bytes to a bytearray
        decrypted_data = encrypter.decrypt(line_bytes)
        print(decrypted_data.hex())




if __name__ == "__main__":
    main()

