function [Down_tra_best_interp]=LUT_Up_Tra_without_Eratio(RTPL_down,AOD_value,wl)
%%
% 通过查找表的方式，计算得到下行透过率
% (这里由于730-780的QE光谱仪没有E790/E660,因此选择固定AOD值（默认0.2）来查找)

%参数说明
% RTPL_down: 等效辐射传输路径长度,“equvalent ” radiative transfer path length,(RTPL),ERTPL.
% AOD_value: 气溶胶光学厚度, aerosol optical depth, AOD
% wl: 观测波长数据, 纬度 :n*1
%% 设置AOD默认值为0.2
if nargin<2
    AOD_value=0.2;
end
%% 读取E比值_Tdir的模拟数据
load('ZYG_Ground_0100_SR_030_LUT_Tot_Tower_15.mat');          % 各列说明：RTPL,AOD,VZA,?,?,透过率.....                         
AOD_00_90 = ZYG_Ground_0100_SR_030_LUT_Tot_Tower_15(:,2);
Table_up_raw = ZYG_Ground_0100_SR_030_LUT_Tot_Tower_15;
%% 提取出对应AOD值的模拟数据
idx=Table_up_raw(:,2)==AOD_value;
Table_up_accorto_AOD=Table_up_raw(idx,:);
%% 根据RTPL值进行插值
L_min=min(Table_up_accorto_AOD(:,1));
L_max=max(Table_up_accorto_AOD(:,1));
if RTPL_down>=L_min & RTPL_down<=L_max
    Up_value_interpt=interp1(Table_up_accorto_AOD(:,1),Table_up_accorto_AOD(:,6:end),RTPL_down,'linear');
elseif RTPL_down<L_min
    RTPL_down_min = L_min;
    Up_value_interpt = interp1(Table_up_accorto_AOD(:,1),Table_up_accorto_AOD(:,6:end),RTPL_down_min,'linear');
elseif (RTPL_down > L_max)
    RTPL_down_max = L_max;
    Up_value_interpt= interp1(Table_up_accorto_AOD(:,1),Table_up_accorto_AOD(:,6:end),RTPL_down_max,'linear');
end
%% 根据波长对模拟透过率进行插值
Norm_wl= importdata('wl_pro.txt');%% 标准波长文件（模拟的透过率是这个波长下的透过率）
Down_tra_best_interp=interp1(Norm_wl,Up_value_interpt,wl,'spline');
end
