This Python implementation is based on, and duplicates much of the functionality of,
 the reference C implementation available in the liboqs repository:
 https://github.com/open-quantum-safe/liboqs/tree/master/src/kex_rlwe_newhope

This implementation is designed to be used natively in Python applications,
without the need for wrappers or other means of incorporating the C implementation
 into production software.

A testing harness is available in test.py, and documentation is provided as
 code comments. The code should be readable and usable.

Python 3.6 must be installed for this implementation to work, as it relies
 on hashlib.shake_128(), which is only available in version 3.6 and later.

Once you have Python 3.6 and Git installed, open a terminal and enter the following commands:

python3 test.py
