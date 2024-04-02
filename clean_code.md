## Best practices I (Flo) suggest:

1. Use tabs for indentation.
2. Always update the README file. We have to make a documentation anyway.
3. Keep functions and loops as simple as possible.
4. Only publish the "source material". Everything else like outputs and plots should not be uploaded. Use the .gitignore for this.
5. Longer variable names are better than shorter ones that are less clear.
6. Update the requierements.txt when necessary. 
7. Lot of small commits are better than one big commit.
8. Always explain your code. 
    * Small comment above every code snippet. with<br>
    \# very brief explanation
    * give a brief explanation of the script at the very beginning of your code with<br>
    '''<br>
    explanation<br>
    '''
    * when using .py instead of .ipynb seperate bigger code segments with<br>
    ############################################<br>
    \# segment title<br>
    ############################################<br>

9. If your code gets very long (>>150 lines), split into different files. You can import files like regular python modules and use its functions.


_____________________________________

this is a condensed guide for clean (better) coding I found.

Code is clean if it can be understood easily – by everyone on the team. Clean code can be read and enhanced by a developer other than its original author. With understandability comes readability, changeability, extensibility and maintainability.
_____________________________________

## General rules
1. Follow standard conventions.
2. Keep it simple stupid. Simpler is always better. Reduce complexity as much as possible.
3. Boy scout rule. Leave the campground cleaner than you found it.
4. Always find root cause. Always look for the root cause of a problem.

## Design rules
1. Keep configurable data at high levels.
2. Prevent over-configurability.

## Understandability tips
1. Be consistent. If you do something a certain way, do all similar things in the same way.
2. Use explanatory variables.
3. Encapsulate boundary conditions. Boundary conditions are hard to keep track of. Put the processing for them in one place.
4. Avoid negative conditionals.

## Names rules
1. Choose descriptive and unambiguous names.
2. Make meaningful distinction.
3. Use pronounceable names.
4. Use searchable names.
5. Replace magic numbers with named constants.
6. Avoid encodings. Don't append prefixes or type information.

## Functions rules
1. Small.
2. Do one thing.
3. Use descriptive names.
4. Prefer fewer arguments.
5. Have no side effects.

## Comments rules
1. Always try to explain yourself in code.
2. Don't be redundant.
3. Don't add obvious noise.
4. Don't use closing brace comments.
5. Don't comment out code. Just remove.
6. Use as explanation of intent.
7. Use as clarification of code.
8. Use as warning of consequences.
