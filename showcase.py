from loop_magic import Loop


@Loop.enable
def function_with_magic_loops() -> None:
    with Loop(range(5)) as (i, loop_i):
        with Loop(range(5)) as (j, loop_j):
            if j - i > 2:
                loop_j.continue_()
            with Loop(range(5)) as (k, loop_k):
                print(f"{i=} {j=} {k=}")
                if k == j:
                    loop_j.continue_()
                if i * j * k > 20:
                    loop_i.break_()


if __name__ == "__main__":
    function_with_magic_loops()
