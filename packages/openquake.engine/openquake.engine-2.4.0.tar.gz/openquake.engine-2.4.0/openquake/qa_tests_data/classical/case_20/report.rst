Classical Hazard QA Test, Case 20
=================================

================================================ ========================
tstation.gem.lan:/mnt/ssd/oqdata/calc_21331.hdf5 Fri May 12 10:45:54 2017
engine_version                                   2.4.0-git59713b5        
hazardlib_version                                0.24.0-git0596dd3       
================================================ ========================

num_sites = 1, sitecol = 809 B

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            2.0               
complex_fault_mesh_spacing      2.0               
width_of_mfd_bin                1.0               
area_source_discretization      10.0              
ground_motion_correlation_model None              
random_seed                     106               
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source                  `source_model.xml <source_model.xml>`_                      
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========================= ====== ====================================== =============== ================
smlt_path                 weight source_model_file                      gsim_logic_tree num_realizations
========================= ====== ====================================== =============== ================
sm1_sg1_cog1_char_complex 0.070  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg1_cog1_char_plane   0.105  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg1_cog1_char_simple  0.175  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg1_cog2_char_complex 0.070  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg1_cog2_char_plane   0.105  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg1_cog2_char_simple  0.175  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg2_cog1_char_complex 0.030  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg2_cog1_char_plane   0.045  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg2_cog1_char_simple  0.075  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg2_cog2_char_complex 0.030  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg2_cog2_char_plane   0.045  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
sm1_sg2_cog2_char_simple  0.075  `source_model.xml <source_model.xml>`_ trivial(1)      1/1             
========================= ====== ====================================== =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ================ ========= ========== ==========
grp_id gsims            distances siteparams ruptparams
====== ================ ========= ========== ==========
0      SadighEtAl1997() rrup      vs30       mag rake  
1      SadighEtAl1997() rrup      vs30       mag rake  
2      SadighEtAl1997() rrup      vs30       mag rake  
3      SadighEtAl1997() rrup      vs30       mag rake  
4      SadighEtAl1997() rrup      vs30       mag rake  
5      SadighEtAl1997() rrup      vs30       mag rake  
6      SadighEtAl1997() rrup      vs30       mag rake  
7      SadighEtAl1997() rrup      vs30       mag rake  
8      SadighEtAl1997() rrup      vs30       mag rake  
9      SadighEtAl1997() rrup      vs30       mag rake  
10     SadighEtAl1997() rrup      vs30       mag rake  
11     SadighEtAl1997() rrup      vs30       mag rake  
====== ================ ========= ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=12, rlzs=12)
  0,SadighEtAl1997(): ['<0,sm1_sg1_cog1_char_complex~Sad1997,w=0.07000000029802322>']
  1,SadighEtAl1997(): ['<1,sm1_sg1_cog1_char_plane~Sad1997,w=0.10499999672174454>']
  2,SadighEtAl1997(): ['<2,sm1_sg1_cog1_char_simple~Sad1997,w=0.17499999701976776>']
  3,SadighEtAl1997(): ['<3,sm1_sg1_cog2_char_complex~Sad1997,w=0.07000000029802322>']
  4,SadighEtAl1997(): ['<4,sm1_sg1_cog2_char_plane~Sad1997,w=0.10499999672174454>']
  5,SadighEtAl1997(): ['<5,sm1_sg1_cog2_char_simple~Sad1997,w=0.17499999701976776>']
  6,SadighEtAl1997(): ['<6,sm1_sg2_cog1_char_complex~Sad1997,w=0.029999999329447746>']
  7,SadighEtAl1997(): ['<7,sm1_sg2_cog1_char_plane~Sad1997,w=0.04500000178813934>']
  8,SadighEtAl1997(): ['<8,sm1_sg2_cog1_char_simple~Sad1997,w=0.07500000298023224>']
  9,SadighEtAl1997(): ['<9,sm1_sg2_cog2_char_complex~Sad1997,w=0.029999999329447746>']
  10,SadighEtAl1997(): ['<10,sm1_sg2_cog2_char_plane~Sad1997,w=0.04500000178813934>']
  11,SadighEtAl1997(): ['<11,sm1_sg2_cog2_char_simple~Sad1997,w=0.07500000298023224>']>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== =========== ============ ============
source_model     grp_id trt                  num_sources eff_ruptures tot_ruptures
================ ====== ==================== =========== ============ ============
source_model.xml 0      Active Shallow Crust 3           86           86          
source_model.xml 1      Active Shallow Crust 3           86           86          
source_model.xml 2      Active Shallow Crust 3           86           86          
source_model.xml 3      Active Shallow Crust 3           119          119         
source_model.xml 4      Active Shallow Crust 3           119          119         
source_model.xml 5      Active Shallow Crust 3           119          119         
source_model.xml 6      Active Shallow Crust 3           88           88          
source_model.xml 7      Active Shallow Crust 3           88           88          
source_model.xml 8      Active Shallow Crust 3           88           88          
source_model.xml 9      Active Shallow Crust 3           121          121         
source_model.xml 10     Active Shallow Crust 3           121          121         
source_model.xml 11     Active Shallow Crust 3           121          121         
================ ====== ==================== =========== ============ ============

============= =====
#TRT models   12   
#sources      36   
#eff_ruptures 1,242
#tot_ruptures 1,242
#tot_weight   2,880
============= =====

Informational data
------------------
============================== =====================================================================================
count_eff_ruptures.received    tot 26.15 KB, max_per_task 1.12 KB                                                   
count_eff_ruptures.sent        sources 101.75 KB, monitor 20.16 KB, srcfilter 16.03 KB, gsims 2.13 KB, param 1.52 KB
hazard.input_weight            2,880                                                                                
hazard.n_imts                  1 B                                                                                  
hazard.n_levels                4 B                                                                                  
hazard.n_realizations          12 B                                                                                 
hazard.n_sites                 1 B                                                                                  
hazard.n_sources               36 B                                                                                 
hazard.output_weight           4.000                                                                                
hostname                       tstation.gem.lan                                                                     
require_epsilons               0 B                                                                                  
============================== =====================================================================================

Slowest sources
---------------
====== ========= ========================= ============ ========= ========= =========
grp_id source_id source_class              num_ruptures calc_time num_sites num_split
====== ========= ========================= ============ ========= ========= =========
4      SFLT1     SimpleFaultSource         56           0.003     1         1        
5      SFLT1     SimpleFaultSource         56           0.003     1         1        
4      CHAR1     CharacteristicFaultSource 1            0.003     1         1        
3      SFLT1     SimpleFaultSource         56           0.003     1         1        
0      SFLT1     SimpleFaultSource         56           0.003     1         1        
1      SFLT1     SimpleFaultSource         56           0.003     1         1        
2      SFLT1     SimpleFaultSource         56           0.003     1         1        
8      SFLT1     SimpleFaultSource         58           0.003     1         1        
10     SFLT1     SimpleFaultSource         58           0.003     1         1        
5      CHAR1     CharacteristicFaultSource 1            0.003     1         1        
11     SFLT1     SimpleFaultSource         58           0.003     1         1        
9      SFLT1     SimpleFaultSource         58           0.003     1         1        
0      COMFLT1   ComplexFaultSource        29           0.003     1         1        
0      CHAR1     CharacteristicFaultSource 1            0.003     1         1        
8      CHAR1     CharacteristicFaultSource 1            0.003     1         1        
6      CHAR1     CharacteristicFaultSource 1            0.003     1         1        
3      CHAR1     CharacteristicFaultSource 1            0.003     1         1        
9      CHAR1     CharacteristicFaultSource 1            0.003     1         1        
10     CHAR1     CharacteristicFaultSource 1            0.003     1         1        
10     COMFLT1   ComplexFaultSource        62           0.002     1         1        
====== ========= ========================= ============ ========= ========= =========

Computation times by source typology
------------------------------------
========================= ========= ======
source_class              calc_time counts
========================= ========= ======
CharacteristicFaultSource 0.029     12    
ComplexFaultSource        0.025     12    
SimpleFaultSource         0.033     12    
========================= ========= ======

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
count_eff_ruptures 0.004 0.002  0.002 0.009 24       
================== ===== ====== ===== ===== =========

Slowest operations
------------------
================================ ========= ========= ======
operation                        time_sec  memory_mb counts
================================ ========= ========= ======
reading composite source model   0.596     0.0       1     
total count_eff_ruptures         0.106     0.0       24    
managing sources                 0.028     0.0       1     
store source_info                0.001     0.0       1     
aggregate curves                 7.544E-04 0.0       24    
filtering composite source model 8.488E-05 0.0       1     
saving probability maps          3.695E-05 0.0       1     
reading site collection          3.219E-05 0.0       1     
================================ ========= ========= ======