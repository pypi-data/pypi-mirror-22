--
-- Multi Calculation I/x
--
m.move_action     =   0 -- rotate
m.arm_length      =    ${model.get('lfe')*1e3}
m.num_pol_pair    =    m.num_poles/2
m.skew_angle      =    ${model.get('skew_angle',0)}
m.nu_skew_steps   =    ${model.get('num_skew_steps',0)}
m.fc_radius1      =    m.fc_radius
m.fc_radius2      =    0.0
m.nu_force_pat    =    0.0
m.num_par_wdgs    =    ${model.get('num_par_wdgs',1)}
m.current         =    ${model.get('current')}*math.sqrt(2.0)/m.num_par_wdgs
m.angl_i_up       =    ${model.get('angl_i_up')}
m.cur_control     =  0 -- 0: range, 1: poc, 6
m.max_current     = 100.0 -- %
m.num_cur_steps   =    ${model['num_cur_steps']}
m.phi_start       =    0.0 --  
m.range_phi       =    720./m.num_poles
m.nu_move_steps   =    ${model.get('num_move_steps')}
m.speed           =    ${model.get('speed')*60}
m.fc_mult_move_type =  1.0 --  Type of move path in air gap
m.fc_force_points   =  0.0 --    number move points in air gap
m.loss_funct    = 0     -- loss functon 0: own 1: ext
m.loss_fact     = 1.0   -- loss multiplication factor

m.pocfilename    = model..'_'..m.num_poles..'p.poc'

run_models("mult_cal_fast")
