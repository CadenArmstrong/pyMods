# pyMods
A python wrapper of islandora CRUD to update MODS records.
Updating a MODS file would require a script, so to contain calling the CRUD functions in the same script simplifies things.

Functionality of CRUD is implemented in all the functions, with MODS assumed to be the only datastream that is worked on.

h2. Basic functionality

1. Get the pids of items
2. Gets the MODS from pids
3. Modify the MODS
4. Push the new MODS
