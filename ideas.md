# Task 4 (heuristicai)

## Strategies

### #1

Our initial strategy was to use the move that results in the most immediate merges.

### #2

Another strategy was to define patterns that we could use to base our next move on. However, we did not end up going with this strategy because it turned out to be way too time consuming and more complex than expected.

- patternmatching -> move depending on pattern
-> Multi-Combination (2, 2, 4, 8)

### #3

Another strategy was to keep the highest tiles in the top / left corner.

Here are some ideas on how to implement this strategy

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

## General thoughts

- What if nothing can be combined?

Should one direction be preferred (Left over Right)?

- When playing the game manually we noticed that it is best to keep the highest numbers in a corner. Therefore it was usually best to move in two directions (e.g. top / left) to keep the highest tile there.

What defines a good move?

- Number of merges
- The higher the merged number the better

What defines a bad move?

- Moves the highest tile out of a corner



## Heuristics

I may be useful to use square functions to increase the weight of a heuristic exponentionally or use the logarithm to achieve the opposite effect. We played around with this a little.

### Empty fields

The Number of zeros on the board (the more zeros the better)

- This heuristic becomes even more relevant when having very few empty tiles

### Smootheness (Gradient Ascent)

The difference between adjacent tiles should be as small as possible.

### Highest number

The higher the value of a tile the better.

- Prefer combinations with high numbers?

### Snake board

The board should look like a snake (highest to lowest number).

## Performance measure

- Average time spent per move
- Average score

# Task 5 (searchai)

Expectimax implementation attempts

1. Using a tree
2. Using recursion (better solution because there is no need to save anything)

Since it is usually best to move into one of three directions the Expectimax algorithm may perform better when only regarding 3 directions, since that improves performance or allowes to use a higher depth.

## Other optimizations

Multithreading

- Multiple branches can be calculated at the same time in parallel using multithreading

Depth

- The depth of the tree can be adjusted depending on the number of zeros left on the board. The more zeros left the more time it takes (exponentially) to dive deeper. Therefore the depth can be increased if there are less zeros left on the board.

Simple starting strategy

- At the start of the game it is very simple to get good results. Therefore one potential optimization is to use a very simple algorithm for the first X moves.

Hash table

- Use hash table to save calculated boards

Zero score

- Use zero score as optimal score.