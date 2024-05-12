include "globals.mzn";

% Using partial symmetric matrices: improves solving the inputs from 1-10
% Set data parameters
int: m; % Number of couriers
int: n; % Number of items

array[1..m] of int: capacity; % Courier capacities
array[1..n] of int: itemSize; % Item sizes
array[1..n+1, 1..n+1] of int: distanceMatrix; % Distance matrix
bool: is_symmetric; % true if the distance matrix is symmetric
array[1..m] of int: min_used_capacities; % minimum possible used capacity of each courier
array[1..m] of int: max_used_capacities; % maximum possible used capacity of each courier
array[1..m] of int: min_durations; % minimum possible duration of each courier
array[1..m] of int: max_durations; % maximum possible duration of each courier

% Decision Variables
array[1..n] of var 1..n: assignment;
array[1..m] of var 1..n: start;
array[1..m] of var 1..n: end;
array[1..m] of var 1..n: duration;
array[1..m] of var int: used_capacity;
array[1..m] of var int: distance_traveled;

% Constraint: Ensure the number of couriers does not exceed the number of items
constraint assert(n >= m,"Invalid datafile: " ++ "Number of couriers should not exceed Number of items");

% Constraint: Capacities and durations for each courier
constraint forall(i in 1..m)
    (min_used_capacities[i] <= used_capacity[i] /\
    max_used_capacities[i] >= used_capacity[i]);
    

constraint forall(i in 1..m) 
    (
    min_durations[i] <= duration[i] /\
    duration[i] <= max_durations[i]
    );

% Constraint: Ensure each item is assigned to a unique courier
constraint alldifferent(start) /\ alldifferent(end) /\ alldifferent(assignment);

% Constraint: Ensure ordered assignments if distance matrix is symmetric
constraint symmetry_breaking_constraint(
    is_symmetric ->
%     forall(i in 1..m) (forall(j in start[i]..end[i]-1) 
%       (assignment[j] = distanceMatrix[assignment[j], k])));
    forall(i in 1..m) (forall(j in start[i]..end[i]-1) (assignment[j] > assignment[j+1])));
%     forall(i in 1..m) (forall(j in start[i]..end[i]-1) (
%           distanceMatrix[assignment[j], assignment[j+1]] <= 
%           distanceMatrix[assignment[j+1], assignment[j+2]])));

% Constraint: Ensure used capacity does not exceed courier capacity
constraint forall(i in 1..m) (used_capacity[i] <= capacity[i]);

% Constraint: Ensure total duration equals the number of items
constraint sum(duration) = n;

% Constraint: Define start and end points for each courier
constraint start[1] = 1 /\
    forall(i in 1..m) (start[i]>=i) /\ 
    forall(i in 1..m) (end[i]<=n-(m-i)) /\
    forall(i in 2..m) (start[i]>end[i-1]);

% Constraint: Calculate durations based on start and end points
constraint duration = [ start[i] - start[i-1] | i in 2..m ] ++ [n+1-start[m]];
constraint end = [ start[i] + duration[i] - 1 | i in 1..m ];
constraint end[m] = n;

% Constraint: Ensure used capacity matches item sizes
constraint forall(i in 1..m)(used_capacity[i] = sum(j in start[i]..end[i]) (itemSize[assignment[j]]));

% Constraint: Calculate distance traveled for each courier
constraint distance_traveled = [ 
    distanceMatrix[n+1, assignment[start[i]]] + 
    sum(j in start[i]..end[i]-1) (distanceMatrix[assignment[j], assignment[j+1]]) + 
    distanceMatrix[assignment[end[i]], n+1]
    | i in 1..m ];

constraint symmetry_breaking_constraint(
    forall(i in 2..m) (
      used_capacity[i-1] >= used_capacity[i] /\
      duration[i-1] >= duration[i]
));


solve 
::
restart_luby(50)
% restart_geometric(50, 2)
% restart_constant(50)
minimize max(distance_traveled);
% + sum([duration[i-1] - duration[i] | i in 2..m]);
% satisfy;
% output ["\(max(distance_traveled))"]
