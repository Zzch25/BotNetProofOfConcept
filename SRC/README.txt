What does it do? The innocent botnet is intended to allow a bunch of varied
computers to utilize byte code to distribute code to networked computers at
which they are prompted how to communicate by manifests and a server side
which manages the client, tasking them and accumulating the end result. This
would then come back to the tasker. This relies on arrays of functions and the
manifests guiding interactions in between and before or after their calls.

This project could be made very overcomplicated so I decided to merely
generate a proof of concept.

If I were to put this into action, first off I would use a much faster
language ihowever the source would become very large and complicated to create.

Given this is a proof of concept, all I needed to prove the viability is a
rough framework that would allow me to run functions on various machines which
would be given information of where to offload intermediate and final results.
This allowed me to hard code a situtation with two clients performing a serial
operation on some basic data. It is not indicative of anything other than
providing the framework for making something efficient for large sets of data.
NOTE: The server does NOT receieve an array of functions. For proof of concept
one simple function is used and the code does not reflect this intended
design.

----------------------------------------------------------------------------
============================================================================
How the proof of concept functions, again the final would use an array of
functions and a manifest to dictate operations of both the server and client
however this is a hard coded situation.
============================================================================

The server is informed that it is to send the same function with two sets of
data to two clients. The server is told to wait for data from both clients.

Client one of two is told to count the number most frequent in an array. It
then must report this to the counterpart client the server has informed the
client of.

Client two of two is told to count the number most frequent in an array. It
then must report this to the counterpart client the server has informed the
client of.

Client one of two must then zero the received and its sent number when it
occurs in its array. It then must send the modified array back to the server.

Client two of two must then zero the received and its sent number when it
occurs in its array. It then must send the modified array back to the server.

The server receives data back from both clients, pass the data to its
function. The funtion returns and the server prints the data.
