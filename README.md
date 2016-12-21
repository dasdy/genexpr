# genexpr
customizable arithmetic problem generator

Simple expr generator mostly works now. it is naive and allows to 
 * control depth of expression 
 * limiting used number range
 * control length of chains (multiplication, addition etc)
 * custom rules for exponential parameters generation
 
 However, results are more often than not are either too simple, or too complicated for 7-grader to do without calculator
 
 
 Planning to do a more robust system that generates actual AST, with traversal functions, which
 probably will allow controlling generated expressions easier
