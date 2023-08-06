Psycopg2 Range Overlaps
========================

This module overrides the Range.__and__ function, so that it returns a boolean value
based on if the two objects overlap.

The rationale behind this is that it mirrors the `range && range` operator in postgres.


There is also an improved equality operator, and a function for normalising ranges (if possible).