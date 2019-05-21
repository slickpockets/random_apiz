import gnupg
from escpos import config
c = config.Config()
printer = c.printer()

gpg = gnupg.GPG(binary='/usr/bin/gpg', homedir='./keys', keyring='pubring.gpg', secring='secring.gpg')


batch_key_input = gpg.gen_key_input( key_type='RSA', key_length=4096)

key = gpg.gen_key(batch_key_input)

