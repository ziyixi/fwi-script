# Extract new region from Dr. Tao Kai's FWEA18

# workflow

1. Create the "specfem" directory with the following models:

   - tao: model FWEA18, the region should be the same with Dr. Tao's region.
   - s362ani_bad_gll: model s362ani+crust1.0 not fixed
   - s362ani_good_gll: model s362ani+crust1.0 that has been fixed.
   - s362ani_tao_gll: model s362ani+crust1.0 not fixed, with Dr. Tao's region.

2. using "specfem" to generate the working directory.

3. Calculate the perturbation.

   - per_tao by tao/s362_tao_gll
   - per_bad by s362ani_bad_gll/s362ani_bad_gll

4. Interpolate the model.

   - per_bad + per_tao -> per_s362ani_tao

5. Retrive the model.
   - per_s362ani_tao \* s362ani_good_gll -> s362ani_tao
