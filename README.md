# seminar-wise21-deltaslim

Group 3: Delta-slim triangles

This is a project which originated as part of a seminar on hyperbolic geometry. The aim is to visualise the delta hypernbolicity of the hyperbolic space by triangles in the Poincaré disk and half-plane model.\
These visuilasations rely on the python package [hyperbolic](https://github.com/cduck/hyperbolic) by Casey Duckering. 

## Deltahyperbolicity and delta-slim triangles

It is easy to imagine how spheric triangles are “fatter” than Euclidian ones. 
Just like this, hyperbolic triangles look slimmer in comparison. 
Gromov used this property to generalize hyperbolic spaces.
Imagine delta-neighborhoods of the sides of a triangle. 
If every edge of a triangle is covered by the delta neighborhoods of the two other edges, the triangle is called delta-slim.
If every triangle on a space has this property, then the space is also delta-slim.
A metric space is hyperbolic, if there is a delta so that every triangle is delta-slim 
This implies the existence of a global delta in hyperbolic spaces. \
Our project had the aim to visualize the delta neighborhoods for different triangles in the Poincaré disk model,
to compute the minimal delta for different triangles, 
and to show how these minimal deltas interplay with the global solution.
In particular we implemented a function that returns whether a given triangle is delta slim for a given delta.
It uses lines of constant distance to the edges -so called Hypercycles- and their intersection points with the other edges of the triangle.

![Triangle with inner Hypercycles](https://github.com/hegl-lab/proseminar-wise21-deltaslim/blob/main/examples/images/poincare_triangle_2_inneroffsetEdge.png)

This enables us to approximate the minimal delta for which a given triangle is still delta slim using the mentioned function and nested intervals.

![triangle approximated neigbourhood](https://github.com/hegl-lab/proseminar-wise21-deltaslim/blob/main/examples/images/poincare_triangle_2_nbh_approx.png)

Taking an experimental approach, we created a random sample of points uniformly distibuted in the euclidian unit circle.

![uniform sample](https://github.com/hegl-lab/proseminar-wise21-deltaslim/blob/main/examples/images/poincare_sample_points.png)

From this sample we created random triangles with different amount of ideal points as vertices and plotted their minimal deltas.

![Histogram step](https://github.com/hegl-lab/proseminar-wise21-deltaslim/blob/main/examples/images/histo_3000_64_3_step_30.png)

For more ideal points, more triangles have a greater minimal delta. 
Also we find a maximum of the minimal deltas, the global delta, which is the same value that all of the ideal triangles yield.
This result confirmes our expectations. 
It is quite easy to show that every non ideal triangle is surrounded by an ideal triangle, 
and therefore if the ideal triangle is delta-slim the non ideal is as well. 

![Triangle with surrounding Triangle](https://github.com/hegl-lab/proseminar-wise21-deltaslim/blob/main/examples/images/poincare_triangle_2_surroundingIdealTriangle.png)

It is well established by the earlier mathematical work that all ideal triangles are congruent. 
So in conclusion, the minimal delta of any ideal triangle already is the global delta.\
As we know the upper half plane and poincare disk models are isomorphic, 
so we extended our code to the upper half plane model as well.

![Triangle in halfplane](https://github.com/hegl-lab/proseminar-wise21-deltaslim/blob/main/examples/images/halfplane_triangle_nbh3.png)

## Setup

hyperbolic is available on PyPI:
```
$ pip3 install hyperbolic>=1.4.0
```

Install drawSvg also to display the hyperbolic geometry:
```
$ pip3 install drawSvg
```

## Examples

Choose points interactively in this [widget](https://github.com/hegl-lab/proseminar-wise21-deltaslim/blob/main/examples/widget.ipynb) and explore deltaslim triangles in the Poincaré disk model.\

See these [examples](https://github.com/hegl-lab/proseminar-wise21-deltaslim/tree/main/examples) for a better understanding:

- [Poincaré disk](https://github.com/hegl-lab/proseminar-wise21-deltaslim/blob/main/examples/poincaredisk.ipynb)
- [Half-plane](https://github.com/hegl-lab/proseminar-wise21-deltaslim/blob/main/examples/halfplane.ipynb)