# Description
Get the flag from the service running at xx.xx.xx.xx:xxxxx

# Solution
Reading the provided source code reveals a hash table implementation of exceptionally poor quality.
Crucially, only the hash of the key is stored and not the key itself. Additionally, the lousy
homegrown hash function is sure to create tons of collisions. Combining those two insights,
contestants should realize that they can substitute one key for another (as long their hashes are
equal).
The command-line interface exposed to clients allows to insert key-value pairs and get the value
corresponding to some key. The flag is stored in the bucket corresponding to the key "flag",
however, the interface does not allow a client to read the value of the key "flag"!
The solution is to perform a second-preimage attack on the hash function.
In fact, symbolic execution of the hash function using a tool such as Z3 can generate preimages in
a matter of seconds (see the Python script solution.py).