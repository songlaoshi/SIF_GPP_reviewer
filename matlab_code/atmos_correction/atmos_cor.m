function [irrad_cor,rad_cor,ref_cor]=atmos_cor(irradiance,radiance,wl,obs_time,H,obs_angle,sza,Date,Tem_press_all_data)
%%
% ����˵��
% irradiance: ̫�������������,��λ mW/(m2/nm), n*1
% radiance: �ڲ㷴����䣬��λ mW/(m2/nm/sr), n*1
% wl�� �۲����ݵĲ���
% obs_time: �۲�ʱ�䣬��ʽ��Сʱ��
% H: ����̽ͷ����ڲ�ľ���
% obs_angle: ���ڲ�۲��������ֱ����н�,��λ ��
% sza: ̫���춥�ǣ���λ ��
% Date: ���ڣ������ʽ�� 20190308���ַ�������
% Tem_press_all_data: վ�������գ�Сʱ������12/24=0.5�����¶ȣ��棩����ѹ���ݣ�hPa��
%    e.g. 20190308 0.5 25 1000

%%
% ��ѧ����·������
L_up=(H/1000)/cosd(obs_angle);
L_down=(H/1000)/cosd(sza);
% ��ͬ���α�׼��ѹ���¶ȣ����� altitude=0.100 km, P=1001.309 hPa, T=293.75 K
P_zero=1001.309;
T_zero=293.750;
% ��Ч·��
Date_Num=find(Tem_press_all_data(:,1)==str2double(Date));
Date_size=size(Date_Num,1);
if Date_size==0
    RTPL_up=real(L_up*(P_zero/P_zero)^0.9353*(T_zero/T_zero)^0.1936);
    RTPL_down=real(L_down*(P_zero/P_zero)^0.9353*(T_zero/T_zero)^0.1936);
elseif Date_size~=0
    Tem_interp = interp1(Tem_press_all_data(Date_Num(1,1):Date_Num(end,1),2),Tem_press_all_data(Date_Num(1,1):Date_Num(end,1),3),obs_time,'nearest');
    Pre_interp = interp1(Tem_press_all_data(Date_Num(1,1):Date_Num(end,1),2),Tem_press_all_data(Date_Num(1,1):Date_Num(end,1),4),obs_time,'nearest');
    RTPL_up =  real(L_up * (Pre_interp./P_zero).^0.9353 * ((T_zero-273.15)./Tem_interp).^0.1936);
    RTPL_down =  real(L_down * (Pre_interp./P_zero).^0.9353 * ((T_zero-273.15)./Tem_interp).^0.1936);
end
% 
% �ڲ��ұ��в���������͸����
[Up_tra]=LUT_Up_Tra_without_Eratio(RTPL_up,0.2,wl);
[Down_tra] = LUT_Down_Tra_without_Eratio(RTPL_down,0.2,wl);
%��TOA��������������ֵת��ΪTOC���ڲ㴦����ֵ
%У��������ֵ��
rad_cor = radiance ./Up_tra;
%У��������ֵ��
irrad_cor = irradiance .*Down_tra;
% У�������ʣ�
ref_cor=rad_cor *pi ./irrad_cor;

end