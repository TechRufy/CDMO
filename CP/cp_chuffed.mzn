include "globals.mzn";
include "chuffed.mzn";

% variable definition
int: m; % number of couriers
int: n; % number of items to distribute
int: k = ceil((n/m) + 2 + n mod m); % max path length
array[1..m] of int: l; % courier load capacities
array[1..n] of int: s; % items' size
array[1..n+1, 1..n+1] of int: D; % distribution points distances
array[1..m, 1..k] of var 1..n+1: P; % couriers paths
array[1..m] of var int: d;  % total distance for each courier

% constraints definition
constraint forall(i in 1..m) (P[i,1] = n+1); % ensures the courier starts from the origin
constraint forall(i in 1..m) (P[i,k] = n+1); % ensures the courier end at the origin
constraint count_eq(P, n+1, k*m-n); % ensures that all the items are distributed
constraint all_different_except(P, {n+1}); % ensures that all items are distributed only once
constraint forall(i in 1..m) (sum(j in 1..k where P[i,j] != n+1) (s[P[i,j]]) <= l[i]); % avoid courriers overload
constraint forall(i in 1..m) (d[i] = sum(j in 1..k-1) (D[P[i,j],P[i,j+1]])); % computes the total distance for each courier

% other constraints
constraint forall(i in 1..m) (P[i,2] != n+1); % each courrier has to distribute at least one item

% objective function
var int: path_length = max(d);

solve
 :: int_search(P, first_fail, indomain_median)
 :: restart_luby(50) 
minimize path_length;
%solve minimize path_length;

% print output 
output [
    "Paths = ", show2d(P), "\n",
    "Max Path Length = ", show(path_length)
];