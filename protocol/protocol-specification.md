# Common Header

## Sender Identification.

A 16 bit value. Randomly generated
or set by user. Must make sure that
the ID is not identical. If the configuration
process is not able to generate a unique ID
that the Extended Sender Identification Header can
be enabled. This header is 24 bit long and can be
randomly filled. The space is likely large enough
that no collisions occure.

If the extended Sender Identification Header is available
then the Sender Identification MUST be combined with the
Extended Sender Identification Header to form one logical
representation:

```
string id = "";
       id += SE;
       id += ESIH;
```



## Static Length Extension Header

### Extended Sender Identification Header

A unique, static ideentifier. Only used
if v4 AND v6 is enabled to differnetiate
packets and drop the later received
packet with the identical information.

24 bit plus 8 bit next header



## Dynamic Length Extension Header

