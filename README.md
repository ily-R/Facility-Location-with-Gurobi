# Facility-Location-MOGPL

**Introduction and Objectives:**
The facility localization problem models a real problem of locating services (hospital, administration, fire station, library, swimming pool) on a geographic area in a way to fairly share access to these resources by the people in that area.Depending on the case, the notion of "fairly" can be distance, time or more generally the cost of access of potential users (customers) to the resource that has been assigned to them.
In this repo I will work on a simplifed problem where we optimize the localization of one resource (library) in k locations. The same approach can be used to a more generalized situation.
let I = {1,...,n} be the set of cities in the geographic area, and population(i) be the population of each city ![](https://latex.codecogs.com/gif.latex?i%5Cepsilon%20I). We will choose a set J of cities that contain the resources such that ![](https://latex.codecogs.com/gif.latex?J%5Csubseteq%20I) and ![](https://latex.codecogs.com/gif.latex?%5Cleft%20%7C%20J%20%5Cright%20%7C%20%3D%20k) (K<n).
let ![](https://latex.codecogs.com/gif.latex?x_%7Bij%7D%5E%7B%7D) indicates whethere city i is connected to a resource in city j.
let ![](https://latex.codecogs.com/gif.latex?d_%7Bij%7D%5E%7B%7D) denotes the distance between city i and city j.

**Solution.py**:
*objective function* :
![](https://latex.codecogs.com/gif.latex?min%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%5Csum_%7Bj%3D1%7D%5E%7Bk%7D%20d_%7Bij%7D*x_%7Bij%7D)

