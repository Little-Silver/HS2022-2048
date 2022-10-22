# Strategy ideas

- Use move that does the most combinations

- What if nothing can be combined?

- Should one direction be preferred (Left over Right)?

- Prefer combinations with high numbers?

- What defines a good move?
- patternmatching -> move depending on pattern
-> Multi-Combination (2, 2, 4, 8)
-> Try to align numbers (in row or column)

1. Combine as many numbers as possible
2. Combine high numbers preferrably (log2 -> square)
3. What if nothing can be combined?

Performance measure:
- Time per move
- avg score

# Idea always move up or left if possible
- top row should always be full if possible
- left as long as possible
- if left is not possible go up
- right is allowed if top row is full and nothing will be combined
- before combining the first row, it would be awesome if the second row was full
--> if that is possible go left and then go up to fill the first row immediatly again
- in some edge cases certain rules may be ignored

Goal: [[biggest number, 2nd biggest, some number, some number], 
        [...,...,...,...],
        [...,...,...,...],
        [...,...,...,...],]


1. Find best move (UP, LEFT, RIGHT)
        1.1 LEFT and UP always allowed
        1.2 RIGHT if LEFT and UP are not possible
        1.3 RIGHT allowed if first row is full
3. Repeat 1. and 2. until impossible
4. RIGHT if possible
        4.1 UP if good combinations in first row possible 4.2 back to 1.
5. DOWN
        5.1 UP
        5.2 back to 1.

## searchai
- smoothness (calculate difference between adjacent tiles)
- use expectimax
- use expectimax (only with 3 directions)