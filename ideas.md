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
