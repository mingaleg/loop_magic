from loop_magic import Loop


@Loop.enable
def test_func() -> None:
    with Loop(range(5)) as (i, loop_i):
        with Loop(range(5)) as (j, loop_j):
            with Loop(range(5)) as (k, loop_k):
                print(f"{i=} {j=} {k=}")
                if k == j:
                    loop_j.continue_()
                if i * j * k > 20:
                    loop_i.break_()


test_func()
