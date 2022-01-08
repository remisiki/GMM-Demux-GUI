API
===

Classifying Drops
-----------------

.. currentmodule:: gmmd.classifier
.. autosummary::
	:toctree: generated/

	obtain_arrays
	classify_drops
	read_full_classify_result
	store_full_classify_result
	store_simplified_classify_result
	purify_droplets
	count_bad_droplets
	obtain_SSD_list
	obtain_MSM_list
	count_by_class
	get_SSD_count_ary

Estimating Multiplet rates
--------------------------

.. currentmodule:: gmmd.estimator
.. autosummary::
	:toctree: generated/

	compute_multiplet_rates_asymp
	compute_relative_SSM_rate_asymp
	compute_relative_SSM_rate
	get_min_hto_num
	cell_num_estimator
	drop_num_estimator
	compute_shared_num
	compute_mix_rate
	compute_SSM_rate_with_cell_num
	compute_SSD_num
	compute_GEM_prob
	phony_cluster_MSM_rate
	get_tau_cell_num
	pure_cluster_MSM_rate
	test_phony_hypothesis
	test_pure_hypothesis
	compute_observation_probability

Computing Tools
---------------

.. currentmodule:: gmmd.compute
.. autosummary::
	:toctree: generated/

	obtain_base_bv_array
	get_empty_bv
	check_set_bit
	init_mask
	set_bit
	gather_multiplet_rates
	obtain_HTO_GEM_num
	experiment_params_wrapper
	param_scaling
	compute_scaler
	obtain_experiment_params
	obtain_HTO_cell_n_drop_num