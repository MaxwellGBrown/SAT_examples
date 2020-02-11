# SAT Examples

This repo outlines some SAT Solver problem examples.

[Raymond Hettinger - Modern solvers: Problems well-defined are problems solved - PyCon 2019](https://www.youtube.com/watch?v=_GP9OpZPUYc)

[hettinger_solvers.zip](https://www.dropbox.com/s/q3yi69d033v03pi/hettinger_solvers.zip?dl=0)


```
$ python examples/ <puzzle_name>
```

# Learnings

## CNF is an AND of ORs!

This is the most easy thing to forget while composing SAT problems!

You have to train yourself to think how to logically deduce the logic you're providing by combining CNF statements.

I've found that thinking of the logic using a [clique graph](https://en.wikipedia.org/wiki/Clique_problem#NP-completeness) helps. 

**Only one clause in any given CNF statement needs to be true.** The combination of several statements allow us to limit the possibilities.

They key to composing good CNF statements is, inside of the clique, think about what scenarios you want to be true if every other statement is _unsatisfied_.

For example, if I'm codifying the rule "The flier with the shamrock will leave sometime after Rudy" then I want to start by figuring out what cases will force that statement to actually filter down potential solutions.

So, start by saying "Brandi has the Shamrock and is leaving in May"; what clique do I produce to begin to filter out what months Rudy is capabile of leaving in?

The answer tends to lean towards negating the cases that we know:
```
  ~Brandi is leaving in May => ~(True) => False
    OR
  ~Brandi is traveling w/ shamrock => ~(True) => False
    OR
  Rudy is leaving in April
    OR
  Rudy is leaving in March
    OR
  Rudy is leaving in February
    OR
  Rudy is leaving in January
```


### "Something happens a fixed against some criteria"

This is a straightforward clique combination that uses three different negations to filter the case through.

```python
"""The aerophobe going to Wyoming will leave 2 months before Peggy."""
for index in range(0, len(MONTHS) - 2):
    two_months_before, month = MONTHS[index], MONTHS[index + 2]
    for name in (f for f in FLIERS if f != "Peggy"):
        statement += [
            (
                _flew_to(name, "Wyoming"),
                sat_utils.neg(_flew_in(name, two_months_before)),
                sat_utils.neg(_flew_in("Peggy", month)),
            ),
            (
                sat_utils.neg(_flew_to(name, "Wyoming")),
                _flew_in(name, two_months_before),
                sat_utils.neg(_flew_in("Peggy", month)),
            ),
            (
                sat_utils.neg(_flew_to(name, "Wyoming")),
                sat_utils.neg(_flew_in(name, two_months_before)),
                _flew_in("Peggy", month),
            ),
        ]
```



### "N number of possibilities depend on some criteria"

This problem is complex because there's no fixed if -> then. The "then" depends on how many available options there are to pull from. 

```python
def clue_7(statement):
    """The flier with the shamrock will leave sometime after Rudy."""
    for index in range(1, len(MONTHS)):
        rudy_months, shamrock_month = MONTHS[:index], MONTHS[index]
        for name in (f for f in FLIERS if f != "Rudy"):
            new_statement = [
                (
                    # Somebody both traveling this month with shamrock...
                    sat_utils.neg(_flew_with(name, "shamrock")),
                    sat_utils.neg(_flew_in(name, shamrock_month)),
                    # ...then Rudy has to be traveling one of these months
                    *(_flew_in("Rudy", m) for m in rudy_months),  # noqa
                ),
            ]
            statement += new_statement
```


## DNF -> CNF is slow & overcomplicates the puzzle

While using `sat_utils.from_dnf` to convert Disjunctive Normal Form into Conjunctive Normal Form may seem logically easier to compose, it explodes exponentially for statements with many clauses.

Even just the conversion from CNF -> DNF takes a deal of time, and that's before the puzzle is even being solved!

Whenever possible, defer to raw CNF.


Below is a statement written using `sat_utils.from_dnf`:
```python
def clue_5(statement):
    """Lee will leave 1 month after Peggy."""
    dnf = list()
    for index in range(1, len(MONTHS)):
        month, month_after = MONTHS[index - 1], MONTHS[index]
        dnf += [
            (
                _flew_in("Peggy", month),
                _flew_in("Lee", month_after),
            )
        ]
    statement += sat_utils.from_dnf(dnf)
```

...and below is the statement written using pure CNF:

```python
def clue_5(statement):
    """Lee will leave 1 month after Peggy."""
    for index in range(len(MONTHS) - 1, 0, -1):
        month_before, month = MONTHS[index - 1], MONTHS[index]
        statement += [
            (
                _flew_in("Peggy", month_before),
                sat_utils.neg(_flew_in("Lee", month)),
            ),
            (
                sat_utils.neg(_flew_in("Peggy", month_before)),
                _flew_in("Lee", month),
            ),
        ]

    # We can logically infer this case, but IT IS NOT NECESSARY!
    # statement += [  # This case goes uncaught
    #     (sat_utils.neg(_flew_in("Peggy", "May")),)
    # ]
```

## You need to catch the outside cases of the logic

Catching the broken/null cases in your logic is manditory, even though it may seem like providing extra logic to the clique generators.

For example, if you have a statement that says "James leaves two days before Jessica", _you should program the deduction that Jessica cannot leave on the two earliest days_.
