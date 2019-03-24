function [Down_tra_best_interp]=LUT_Up_Tra_without_Eratio(RTPL_down,AOD_value,wl)
%%
% ͨ�����ұ�ķ�ʽ������õ�����͸����
% (��������730-780��QE������û��E790/E660,���ѡ��̶�AODֵ��Ĭ��0.2��������)

%����˵��
% RTPL_down: ��Ч���䴫��·������,��equvalent �� radiative transfer path length,(RTPL),ERTPL.
% AOD_value: ���ܽ���ѧ���, aerosol optical depth, AOD
% wl: �۲Ⲩ������, γ�� :n*1
%% ����AODĬ��ֵΪ0.2
if nargin<2
    AOD_value=0.2;
end
%% ��ȡE��ֵ_Tdir��ģ������
load('ZYG_Ground_0100_SR_030_LUT_Tot_Tower_15.mat');          % ����˵����RTPL,AOD,VZA,?,?,͸����.....                         
AOD_00_90 = ZYG_Ground_0100_SR_030_LUT_Tot_Tower_15(:,2);
Table_up_raw = ZYG_Ground_0100_SR_030_LUT_Tot_Tower_15;
%% ��ȡ����ӦAODֵ��ģ������
idx=Table_up_raw(:,2)==AOD_value;
Table_up_accorto_AOD=Table_up_raw(idx,:);
%% ����RTPLֵ���в�ֵ
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
%% ���ݲ�����ģ��͸���ʽ��в�ֵ
Norm_wl= importdata('wl_pro.txt');%% ��׼�����ļ���ģ���͸��������������µ�͸���ʣ�
Down_tra_best_interp=interp1(Norm_wl,Up_value_interpt,wl,'spline');
end
