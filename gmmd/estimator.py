from gmmd import compute, classifier
from math import pow
from math import log
from scipy.stats import binom
from scipy.stats import binom_test
from scipy.special import comb
import traceback
import pandas as pd
from tabulate import tabulate
import os

def compute_multiplet_rates_asymp(cell_num, sample_num, drop_num):
    no_drop_rate = (1 - 1 / drop_num)
    cells_per_sample = round(cell_num / sample_num)
    drop_with_cells = (1 - pow(no_drop_rate, cell_num)) * drop_num
    single_sample_drops = sample_num * (1 - pow(no_drop_rate, cells_per_sample) ) * drop_num * pow(no_drop_rate, (sample_num - 1) * cells_per_sample)
    singlet_drops = cell_num * pow(no_drop_rate, cell_num - 1)

    singlet_rate = singlet_drops / drop_with_cells
    single_sample_rate = single_sample_drops / drop_with_cells
    MSM_rate = 1 - single_sample_rate
    SSM_rate = single_sample_rate - singlet_rate
    return MSM_rate, SSM_rate, singlet_rate, drop_with_cells


def compute_relative_SSM_rate_asymp(cell_num, drop_num):
    no_drop_rate = (1 - 1 / drop_num)
    drop_with_cells = (1 - pow(no_drop_rate, cell_num)) * drop_num
    singlet_drops = cell_num * pow(no_drop_rate, cell_num - 1)

    return 1 - singlet_drops / drop_with_cells


def compute_relative_SSM_rate(SSM_rate, singlet_rate):
    """Compute relative SSM rate over singlet rate.

    :param SSM_rate: SSM rate.
    :type SSM_rate: :class:`float`
    :param singlet_rate: Singlet rate.
    :type singlet_rate: :class:`float`

    :return: Relative SSM rate.
    :rtype: :class:`float`

    """
    return SSM_rate / singlet_rate


def get_min_hto_num(cell_num, drop_num, SSM_threshold, sample_num = 1):
    sample_num = 1
    while True:
        #(MSM_rate, SSM_rate, singlet_rate) = compute_multiplet_rates(cell_num, sample_num, drop_num)
        (MSM_rate, SSM_rate, singlet_rate, drop_with_cells) = compute_multiplet_rates_asymp(cell_num, sample_num, drop_num)
        relative_SSM_rate = compute_relative_SSM_rate(SSM_rate, singlet_rate)
        #print(relative_SSM_rate)
        if (relative_SSM_rate <= SSM_threshold):
            break;
        else:
            sample_num += 1

    return sample_num


def cell_num_estimator(a_num, captured_drop_num, capture_rate):
    estimated_drop_num = captured_drop_num / capture_rate
    base = 1 - 1 / estimated_drop_num
    power = 1 - a_num / captured_drop_num
    #print("power:", power)
    #print("base:", base)
    cell_num = log(power, base)
    return cell_num


def drop_num_estimator(a_num, b_num, shared_num):
    drop_num = a_num * b_num / shared_num 
    return drop_num 


def compute_shared_num(drop_num, A_num, B_num):
    A_rate = compute_mix_rate(drop_num, B_num) 
    #print("A_rate: ", A_rate)
    shared_num = A_rate *  A_num
    return shared_num


# Computes the rate of drops that have certain cells in them.
def compute_mix_rate(drop_num, cell_num):
    no_drop_rate = (1 - 1 / drop_num)
    cell_in_rate = 1 - pow(no_drop_rate, cell_num)
    return cell_in_rate


def compute_SSM_rate_with_cell_num(cell_num, drop_num):
    """Compute SSM rate with cell numbers.

    :param cell_num: Number of cells.
    :type cell_num: :class:`float`
    :param drop_num: Number of droplets.
    :type drop_num: :class:`int`

    :return: Rate of SSM.
    :rtype: :class:`float`

    """
    no_drop_rate = (1 - 1 / drop_num)
    singlet_drops = cell_num * pow(no_drop_rate, cell_num - 1)
    drop_with_cells = (1 - pow(no_drop_rate, cell_num)) * drop_num
    SSM_rate = 1 - singlet_drops / drop_with_cells
    return SSM_rate


def compute_SSD_num(drop_num, subject_cell_num, total_cell_num, ambiguous_rate = 0):
    """Compute SSM rate with cell numbers.

    :param drop_num: Number of droplets.
    :type drop_num: :class:`int`
    :param subject_cell_num: Number of subject cells.
    :type subject_cell_num: :class:`int`
    :param total_cell_num: Number of all cells.
    :type total_cell_num: :class:`int`
    :param ambiguous_rate: Ambiguous rate.
    :type ambiguous_rate: :class:`float`, Default = ``0``

    :return: SSD number.
    :rtype: :class:`int`

    """
    no_drop_rate = (1 - 1 / drop_num)
    non_subject_num = total_cell_num - subject_cell_num
    SSD_prob = (1 - pow(no_drop_rate, subject_cell_num)) \
            * pow(no_drop_rate, int(non_subject_num * (1 - ambiguous_rate)))

    return int(SSD_prob * drop_num)


def compute_GEM_prob(drop_num, cell_num):
    return 1 - binom.pmf(0, cell_num, 1 / drop_num)


def phony_cluster_MSM_rate(cell_num_ary, cell_type_num = 2):
    """Estimate phony cluster MSM rate with cell numbers.

    :param cell_num_ary: List of cell numbers.
    :type cell_num_ary: :class:`list`
    :param cell_type_num: Number of MSMs (≥2).
    :type cell_type_num: :class:`int`, Default = ``2`` 

    :return: MSM rate.
    :rtype: :class:`float`

    """
    assert(cell_type_num >= 2)

    total_cell_num = sum(cell_num_ary)
    sample_prob_ary = [cell_num / total_cell_num for cell_num in cell_num_ary]
    
    return 1 - sum([pow(sample_prob, cell_type_num) for sample_prob in sample_prob_ary])


def get_tau_cell_num(drop_num, total_cell_num, cluster_GEM_num, ambiguous_rate = 0.0):
    """Get tau cell number.

    :param drop_num: Number of droplets.
    :type drop_num: :class:`int`
    :param total_cell_num: Number of all cells.
    :type total_cell_num: :class:`int`
    :param cluster_GEM_num: Number of GEMs.
    :type cluster_GEM_num: :class:`int`
    :param ambiguous_rate: Ambiguous rate.
    :type ambiguous_rate: :class:`float`, Default = ``0``

    :return: Tau cell number.
    :rtype: :class:`int`

    """
    SSD_prob = cluster_GEM_num / drop_num 
    no_drop_rate = 1 - 1 / drop_num
    certain_rate = 1 - ambiguous_rate
    
    tau_cell_num = total_cell_num - int(log(SSD_prob \
            + pow(no_drop_rate, total_cell_num * certain_rate + cluster_GEM_num * ambiguous_rate) \
            , no_drop_rate) / certain_rate)

    return tau_cell_num


def pure_cluster_MSM_rate(drop_num, cluster_GEM_num, cell_num_ary, capture_rate, ambiguous_rate = 0):
    """Estimate pure cluster MSM rate.

    :param drop_num: Number of droplets.
    :type drop_num: :class:`int`
    :param cluster_GEM_num: Number of GEMs.
    :type cluster_GEM_num: :class:`int`
    :param cell_num_ary: List of cell numbers.
    :type cell_num_ary: :class:`list`
    :param capture_rate: Capture rate.
    :type capture_rate: :class:`float`
    :param ambiguous_rate: Ambiguous rate.
    :type ambiguous_rate: :class:`float`, Default = ``0``

    :return: MSM rate.
    :rtype: :class:`float`

    """
    #print("==================")

    total_cell_num = sum(cell_num_ary)
    sample_prob_ary = [cell_num / total_cell_num for cell_num in cell_num_ary]

    cluster_GEM_num = cluster_GEM_num / capture_rate

    #print(cluster_GEM_num) 

    mix_cell_num = get_tau_cell_num(drop_num, total_cell_num, cluster_GEM_num)
    tau_cell_num = mix_cell_num 
    #tau_cell_num = (mix_cell_num - total_cell_num * ambiguous_rate) / (1 - ambiguous_rate)
    #tau_cell_num = get_tau_cell_num(drop_num, total_cell_num, cluster_GEM_num)

    #print("initial tau_cell_num: ", tau_cell_num)

    pure_type_GEM_num = compute_SSD_num(drop_num, tau_cell_num + (total_cell_num - tau_cell_num) * ambiguous_rate, total_cell_num, ambiguous_rate)
    while (pure_type_GEM_num > cluster_GEM_num):
        tau_cell_num -= 1
        pure_type_GEM_num = compute_SSD_num(drop_num, tau_cell_num + (total_cell_num - tau_cell_num) * ambiguous_rate, total_cell_num, ambiguous_rate)

    #print("final tau_cell_num: ", tau_cell_num)

    tau_num_ary = [int((tau_cell_num + (total_cell_num - tau_cell_num) * ambiguous_rate) * sample_prob) for sample_prob in sample_prob_ary]
    SSD_num_ary = [compute_SSD_num(drop_num, tau_num, total_cell_num) for tau_num in tau_num_ary]
    total_SSD_num = sum(SSD_num_ary)

    #print("tau GEM num: ", pure_type_GEM_num)
    #print("total num: ", compute_SSD_num(drop_num, total_cell_num, total_cell_num))

    return 1 - (total_SSD_num / pure_type_GEM_num)


def test_phony_hypothesis(cluster_MSM_num, cluster_GEM_num, cell_num_ary, capture_rate):
    """Test phony-type hypothesis.

    :param cluster_MSM_num: Number of MSMs.
    :type cluster_MSM_num: :class:`int`
    :param cluster_GEM_num: Number of GEMs.
    :type cluster_GEM_num: :class:`int`
    :param cell_num_ary: List of cell numbers.
    :type cell_num_ary: :class:`list`
    :param capture_rate: Capture rate.
    :type capture_rate: :class:`float`

    :return: P-value.
    :rtype: :class:`float`

    """
    MSM_rate = phony_cluster_MSM_rate(cell_num_ary)
    return binom_test(cluster_MSM_num / capture_rate, cluster_GEM_num / capture_rate, MSM_rate, "less")


def test_pure_hypothesis(cluster_MSM_num, drop_num, cluster_GEM_num, cell_num_ary, capture_rate, ambiguous_rate = 0):
    """Test pure-type hypothesis.

    :param cluster_MSM_num: Number of MSMs.
    :type cluster_MSM_num: :class:`int`
    :param drop_num: Number of droplets.
    :type drop_num: :class:`int`
    :param cluster_GEM_num: Number of GEMs.
    :type cluster_GEM_num: :class:`int`
    :param cell_num_ary: List of cell numbers.
    :type cell_num_ary: :class:`list`
    :param capture_rate: Capture rate.
    :type capture_rate: :class:`float`
    :param ambiguous_rate: Ambiguous rate.
    :type ambiguous_rate: :class:`float`, Default = ``0``

    :return: P-value.
    :rtype: :class:`float`

    """
    MSM_rate = pure_cluster_MSM_rate(drop_num, cluster_GEM_num, cell_num_ary, capture_rate, ambiguous_rate)
    return binom_test(cluster_MSM_num / capture_rate, cluster_GEM_num / capture_rate, MSM_rate, "greater")


####Debuging Functions####
def debug_get_cell_num(drop_num, GEM_num, capture_rate):
    no_drop_rate = (1 - 1 / drop_num)
    return log(1 - GEM_num / (drop_num * capture_rate), no_drop_rate)


def debug_compute_doublet_num(drop_num, type_a_num, type_b_num):
    no_drop_rate = (1 - 1 / drop_num)
    SSD_prob = (1 - pow(no_drop_rate, type_a_num)) * (1 - pow(no_drop_rate, type_b_num))

    return int(SSD_prob * drop_num)


def debug_pure_cluster_MSM_rate(drop_num, tau_cell_num, sample_num_ary, capture_rate, ambiguous_rate = 0):
    total_cell_num = sum(sample_num_ary)
    sample_prob_ary = [sample_num / total_cell_num for sample_num in sample_num_ary]

    tau_num_ary = [int((tau_cell_num + (total_cell_num - tau_cell_num) * ambiguous_rate) * sample_prob) for sample_prob in sample_prob_ary]

    print(tau_num_ary)

    SSD_num_ary = [compute_SSD_num(drop_num, tau_num, total_cell_num) for tau_num in tau_num_ary]

    print(SSD_num_ary)

    total_SSD_num = sum(SSD_num_ary)

    print(total_SSD_num)

    pure_type_GEM_num = compute_SSD_num(drop_num, tau_cell_num + (total_cell_num - tau_cell_num) * ambiguous_rate, total_cell_num)
    #pure_type_GEM_num = compute_SSD_num(drop_num, tau_cell_num + (total_cell_num - tau_cell_num) * ambiguous_rate, total_cell_num * (1 - ambiguous_rate))

    print("Pure type num: ", int(pure_type_GEM_num * capture_rate))

    return 1 - (total_SSD_num / pure_type_GEM_num)
####End of Debuging Functions####


def compute_observation_probability(drop_num, capture_rate, cell_num_ary, HTO_GEM_ary, base_bv_array, sample_num):
    log_probability = 0

    GEM_prob_ary = []

    #print(drop_num, capture_rate, cell_num_ary, HTO_GEM_ary)
    
    for sample_idx in range(sample_num):
        ori_GEM_num = round(HTO_GEM_ary[sample_idx] / capture_rate)
        GEM_formation_prob = compute_GEM_prob(drop_num, cell_num_ary[sample_idx])
        GEM_prob_ary.append(GEM_formation_prob)

    for i in range(len(HTO_GEM_ary)):
        bv_idx = i + 1
        GEM_formation_prob = 1

        for sample_idx in range(sample_num):
            if compute.check_set_bit(base_bv_array[bv_idx], sample_idx):
                GEM_formation_prob *= GEM_prob_ary[sample_idx]

        ori_GEM_num = round(HTO_GEM_ary[i] / capture_rate)
        sample_binom_prob = binom.pmf(ori_GEM_num, drop_num, GEM_formation_prob)
        #print("***ori_GEM_num:", ori_GEM_num)
        #print("***GEM_formation_prob:", GEM_formation_prob)
        #print("***sample_binom_prob:", sample_binom_prob)
        #print("***log sample_binom_prob:", log(sample_binom_prob))
        #print("***log sample_binom_prob, corrected:", log(sample_binom_prob) * ((1/sample_num) ** (base_bv_array[bv_idx].count_bits() - 1)))
        log_probability += log(sample_binom_prob) * ((1/sample_num) ** (base_bv_array[bv_idx].count_bits() - 1))
        #probability *= sample_binom_prob

    return log_probability


def estimator(GMM_full_df, purified_df, sample_num, base_bv_array, confidence_threshold, estimated_total_cell_num, SSD_idx, sample_names, examine_cell_path = None, ambiguous_rate = 0.05, class_name_ary = None):
    negative_num, unclear_num = classifier.count_bad_droplets(GMM_full_df, confidence_threshold)
    HTO_GEM_ary = compute.obtain_HTO_GEM_num(purified_df, base_bv_array)
    params0 = [80000, 0.5]

    for i in range(sample_num):
        params0.append(round(HTO_GEM_ary[i] * estimated_total_cell_num / sum(HTO_GEM_ary[:sample_num])))

    combination_counter = 0
    try:
        for i in range(1, sample_num + 1):
            combination_counter += comb(sample_num, i, True)
            HTO_GEM_ary_main = HTO_GEM_ary[0:combination_counter]
            params0 = compute.obtain_experiment_params(base_bv_array, HTO_GEM_ary_main, sample_num, estimated_total_cell_num, params0)
    except:
        traceback.print_exc()
        return -1

    (drop_num, capture_rate, *cell_num_ary) = params0

    # SSD_idx = classifier.obtain_SSD_list(purified_df, sample_num, extract_id_ary)

    SSM_rate_ary = [compute_SSM_rate_with_cell_num(cell_num_ary[i], drop_num) for i in range(sample_num)]
    rounded_cell_num_ary = [round(cell_num) for cell_num in cell_num_ary]
    SSD_count_ary = classifier.get_SSD_count_ary(purified_df, SSD_idx, sample_num)
    count_ary = classifier.count_by_class(purified_df, base_bv_array)
    MSM_rate, SSM_rate, singlet_rate = compute.gather_multiplet_rates(count_ary, SSM_rate_ary, sample_num)

    full_report_dict = {
            "droplet_num": round(drop_num),
            "capture_rate": "%5.2f" % (capture_rate * 100),
            "cell_num": sum(rounded_cell_num_ary),
            "singlet_rate": "%5.2f" % (singlet_rate * 100),
            "msm_rate": "%5.2f" % (MSM_rate * 100),
            "ssm_rate": "%5.2f" % (SSM_rate * 100),
            # "RSSM": "%5.2f" % (compute_relative_SSM_rate(SSM_rate, singlet_rate) * 100),
            "negative_rate": "%5.2f" % (negative_num / GMM_full_df.shape[0] * 100),
            "unclear_rate": "%5.2f" % (unclear_num / GMM_full_df.shape[0] * 100)
            }

    full_report_columns = [
            "#Drops",
            "Capture rate",
            "#Cells",
            "Singlet",
            "MSM",
            "SSM",
            # "RSSM",
            "Negative",
            "Unclear"
            ]

    full_report_df = pd.DataFrame([full_report_dict.values()], index = ["Total"], columns=full_report_columns)

    sample_df = pd.DataFrame(data=[
            ["%d" % num for num in rounded_cell_num_ary],
            ["%d" % num for num in SSD_count_ary],
            ["%5.2f" % (num * 100) for num in SSM_rate_ary]
            ],
            columns = sample_names, index = ["Cell count", "SSD count", "Relative SSM rate"])

    if (examine_cell_path):
        examine_result = examine_cluster_type(ambiguous_rate, sample_num, drop_num, capture_rate, rounded_cell_num_ary, purified_df, class_name_ary, confidence_threshold, examine_cell_path)
    else:
        examine_result = None

    return full_report_df, sample_df, full_report_dict, examine_result

def store_summary_result(path, full_report_df, sample_df):
    with open(path, "w") as f:
        f.write("==============================Full Report==============================\n")
    with open(path, "a") as f:
        f.write(tabulate(full_report_df, headers='keys', tablefmt='psql'))
    with open(path, "a") as f:
        f.write("\n\n")
        f.write("==============================Per Sample Report==============================\n")
    with open(path, "a") as f:
        f.write(tabulate(sample_df, headers='keys', tablefmt='psql'))

def examine_cluster_type(ambiguous_rate, sample_num, drop_num, capture_rate, rounded_cell_num_ary, purified_df, class_name_ary, confidence_threshold, cell_list_path):

    simplified_df = classifier.store_simplified_classify_result(purified_df, class_name_ary, None, sample_num, confidence_threshold)

    cell_list = [line.rstrip('\n') for line in open(cell_list_path)]
    cell_list = list(set(cell_list).intersection(simplified_df.index.tolist()))

    MSM_list = classifier.obtain_MSM_list(simplified_df, sample_num, cell_list)

    GEM_num = len(cell_list)
    MSM_num = len(MSM_list)

    phony_test_pvalue = test_phony_hypothesis(MSM_num, GEM_num, rounded_cell_num_ary, capture_rate)
    pure_test_pvalue = test_pure_hypothesis(MSM_num, drop_num, GEM_num, rounded_cell_num_ary, capture_rate, ambiguous_rate)
    # print(pure_test_pvalue)

    if phony_test_pvalue < 0.01 and pure_test_pvalue > 0.01:
        cluster_type = "pure"
    elif pure_test_pvalue < 0.01 and phony_test_pvalue > 0.01:
        cluster_type = "phony"
    else:
        cluster_type = "unclear"

    return GEM_num, MSM_num, phony_test_pvalue, pure_test_pvalue, cluster_type