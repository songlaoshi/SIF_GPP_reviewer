function [irrad_cor,rad_cor,ref_cor]=atmos_cor(irradiance,radiance,wl,obs_time,H,obs_angle,sza,Date,Tem_press_all_data)
%%
% 参数说明
% irradiance: 太阳下行入射辐射,单位 mW/(m2/nm), n*1
% radiance: 冠层反射辐射，单位 mW/(m2/nm/sr), n*1
% wl： 观测数据的波长
% obs_time: 观测时间，格式：小时数
% H: 光纤探头距离冠层的距离
% obs_angle: 朝冠层观测光纤与竖直方向夹角,单位 °
% sza: 太阳天顶角，单位 °
% Date: 日期，输入格式如 20190308，字符串类型
% Tem_press_all_data: 站点年月日，小时数（如12/24=0.5），温度（℃）、气压数据（hPa）
%    e.g. 20190308 0.5 25 1000

%%
% 光学传播路径长度
L_up=(H/1000)/cosd(obs_angle);
L_down=(H/1000)/cosd(sza);
% 不同海拔标准气压与温度，这里 altitude=0.100 km, P=1001.309 hPa, T=293.75 K
P_zero=1001.309;
T_zero=293.750;
% 等效路径
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
% 在查找表中查找上下行透过率
[Up_tra]=LUT_Up_Tra_without_Eratio(RTPL_up,0.2,wl);
[Down_tra] = LUT_Down_Tra_without_Eratio(RTPL_down,0.2,wl);
%将TOA（传感器处）数值转化为TOC（冠层处）数值
%校正地物数值：
rad_cor = radiance ./Up_tra;
%校正入照数值：
irrad_cor = irradiance .*Down_tra;
% 校正反射率：
ref_cor=rad_cor *pi ./irrad_cor;

end