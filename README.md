```
from loop_magic import Loop


@Loop.enable
def function_with_magic_loops() -> None:
    with Loop(range(5)) as (i, loop_i):
        with Loop(range(5)) as (j, loop_j):
            with Loop(range(5)) as (k, loop_k):
                print(f"{i=} {j=} {k=}")
                if k == j:
                    loop_j.continue_()
                if i * j * k > 20:
                    loop_i.break_()
```

prints

```
i=0 j=0 k=0
i=0 j=1 k=0
i=0 j=1 k=1
i=0 j=2 k=0
i=0 j=2 k=1
i=0 j=2 k=2
i=1 j=0 k=0
i=1 j=1 k=0
i=1 j=1 k=1
i=1 j=2 k=0
i=1 j=2 k=1
i=1 j=2 k=2
i=1 j=3 k=0                                  
i=1 j=3 k=1
i=1 j=3 k=2
i=1 j=3 k=3
i=2 j=0 k=0                                  
i=2 j=1 k=0
i=2 j=1 k=1
i=2 j=2 k=0                                  
i=2 j=2 k=1
i=2 j=2 k=2                                  
i=2 j=3 k=0
i=2 j=3 k=1
i=2 j=3 k=2
i=2 j=3 k=3
i=2 j=4 k=0
i=2 j=4 k=1
i=2 j=4 k=2
i=2 j=4 k=3
```