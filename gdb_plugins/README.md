# belong.py
inside gdb (or .gdbinit):
`source belong.py`

## commands
`belong <expression>`  
returns mapping of address according to proc maps

`belongc <expression>`  
if mapping found in proc maps, prints proc maps with relevant
row marked.
