Documentation: http://pybinding.site/

v0.9.2 | 2017-05-26

##### New KPM features and improvements

* Added a method for calculating spatial LDOS using KPM. See the "Kernel Polynomial Method"
  tutorial page and the `KPM.calc_spatial_ldos` API reference.

* Improved single-threaded performance of `KPM.calc_dos` by ~2x by switching to a more efficient
  vectorization method. (Multiple random starter vectors are now computed simultaneously and
  accelerated using SIMD intrinsics.)

* Various KPM methods now take advantage of multiple threads. This improves performance depending
  on the number of cores on the target machine. (However, for large systems performance is limited
  by RAM bandwidth, not necessarily core count.)

* LDOS calculations for multiple orbitals also take advantage of the same vectorization and
  multi-threading improvements. Single-orbital LDOS does not benefit from this but it has received
  its own modest performance tweaks.

* Long running KPM calculation now have a progress indicator and estimated completion time.

##### General improvements and bug fixes

* `StructureMap` can now be sliced using a shape. E.g. `s = pb.rectangle(5, 5); smap2 = smap[s]`
  which returns a smaller structure map cut down to the given shape.

* Plotting the structure of large or periodic systems is slightly faster now.

* Added 2D periodic supercells to the "Shape and symmetry" section of the tutorial.

* Added a few more examples to the "Plotting guide" (view rotation, separating sites and hoppings
  and composing multiple plots).

* Fixed broken documentation links when using the online search function.

* Fixed slow Hamiltonian build when hopping generators are used.



